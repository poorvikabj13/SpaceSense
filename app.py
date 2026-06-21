from flask import Flask, Response, render_template, jsonify, request
import cv2
from google import genai
from google.genai import types
import os
from PIL import Image
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Base directory for absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

VIDEO_FEEDS = {
    "video1": {
        "id": "CAM-01",
        "name": "Pedestrian Crossroad",
        "path": os.path.join(BASE_DIR, "static", "videos", "demo.mp4"),
        "type": "default"
    },
    "video2": {
        "id": "CAM-02",
        "name": "Lobby Entrance",
        "path": os.path.join(BASE_DIR, "static", "videos", "demo2.mp4"),
        "type": "default"
    },
    "video3": {
        "id": "CAM-03",
        "name": "Perimeter Lane",
        "path": os.path.join(BASE_DIR, "static", "videos", "demo3.mp4"),
        "type": "default"
    }
}

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDa4WbSnt3Ji5L_Zznp-gLjqWa5DLGPEhM")

# Validate API key
if GEMINI_API_KEY == "YOUR_API_KEY_HERE" or not GEMINI_API_KEY:
    print("[WARNING] GEMINI_API_KEY not set!")
    print("Get your key from: https://aistudio.google.com/app/apikey")
    
try:
    if GEMINI_API_KEY and GEMINI_API_KEY != "YOUR_API_KEY_HERE":
        client = genai.Client(api_key=GEMINI_API_KEY)
        print("[SUCCESS] Gemini API initialized successfully!")
    else:
        client = None
        print("[WARNING] Gemini API Client not initialized: key is missing or placeholder.")
except Exception as e:
    print(f"[WARNING] Gemini API initialization failed: {e}")
    client = None

# GLOBAL STATE - per video tracking
video_states = {}
current_video = "video1"
last_ai_analysis = ""
last_analysis_time = None

def get_or_create_state(video_key):
    """Get or initialize state for a specific video stream"""
    if video_key not in video_states:
        video_states[video_key] = {
            'anomaly_score': 0,
            'confidence': 0.0,
            'status': "NORMAL FLOW",
            'normal_frame_count': 0,
            'ai_analysis': "",
            'last_frame': None,
            'person_count': 0
        }
    return video_states[video_key]

def analyze_with_gemini(frame):
    """Use Gemini AI to analyze the scene for anomalies"""
    if client is None:
        return "⚠️ Gemini API Client is not initialized. Please configure a valid GEMINI_API_KEY in your environment or .env file."
        
    try:
        # Convert OpenCV frame (BGR) to PIL Image (RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_frame)
        
        # Use modern google-genai Client syntax
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                "You are an expert AI security analyst monitoring live CCTV feeds. "
                "Analyze this frame for anomalies, security concerns, crowd safety issues, or suspicious behaviors. "
                "Provide a brief, high-impact assessment with bullet points summarizing key findings.",
                pil_image
            ]
        )
        return response.text
    except Exception as e:
        print(f"Gemini API analysis failed: {e}")
        return f"❌ AI Analysis failed: {e}\n\nPlease check your API key and network connection."

# Initialize HOG person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Anomaly threshold - trigger when this many or more people detected
ANOMALY_THRESHOLD = 5

def generate(video_key):
    global current_video
    current_video = video_key
    
    state = get_or_create_state(video_key)
    
    cap = cv2.VideoCapture(VIDEO_FEEDS[video_key]["path"])
    
    # Reset state for fresh video stream
    state['anomaly_score'] = 0
    state['confidence'] = 0.0
    state['status'] = "NORMAL FLOW"
    state['normal_frame_count'] = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            # Loop the video by resetting frame position to 0
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()
            if not ret:
                break

        # Resize frame for faster detection
        height, width = frame.shape[:2]
        scale = 0.5
        resized = cv2.resize(frame, (int(width * scale), int(height * scale)))
        
        # Detect people using HOG
        boxes, weights = hog.detectMultiScale(
            resized,
            winStride=(8, 8),
            padding=(4, 4),
            scale=1.05,
            useMeanshiftGrouping=False
        )
        
        person_count = len(boxes)
        state['person_count'] = person_count
        
        # Draw bounding boxes on original frame
        for (x, y, w, h) in boxes:
            # Scale coordinates back to original size
            x, y, w, h = int(x/scale), int(y/scale), int(w/scale), int(h/scale)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Determine if anomaly based on person count
        if person_count >= ANOMALY_THRESHOLD:
            state['anomaly_score'] += 1
            state['status'] = "ANOMALY DETECTED"
            state['confidence'] = min(1.0, state['confidence'] + 0.1)
            state['normal_frame_count'] = 0
            
            # Store frame for AI analysis
            state['last_frame'] = frame.copy()
            
            # Display anomaly warning
            cv2.putText(frame, "ANOMALY DETECTED",
                        (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        3)
        else:
            state['status'] = "NORMAL FLOW"
            state['confidence'] = max(0.0, state['confidence'] - 0.05)
            state['normal_frame_count'] += 1
            
            # Decay anomaly score every 10 normal frames
            if state['normal_frame_count'] >= 10:
                state['anomaly_score'] = max(0, state['anomaly_score'] - 1)
                state['normal_frame_count'] = 0
        
        # Display person count
        cv2.putText(frame, f"People: {person_count}",
                    (20, height - 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2)

        ret, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()

        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

    cap.release()

@app.route("/")
def ui():
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    video_key = request.args.get("video", "video1")
    return Response(generate(video_key),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/detect")
def detect():
    video_key = request.args.get("video", current_video)
    state = get_or_create_state(video_key)
    return jsonify({
        "status": state['status'],
        "anomalies": state['anomaly_score'],
        "confidence": round(state['confidence'], 2),
        "ai_analysis": state.get('ai_analysis', ''),
        "person_count": state.get('person_count', 0)
    })

@app.route("/analyze_ai")
def analyze_ai():
    """Trigger AI analysis on the current anomaly frame"""
    global last_ai_analysis, last_analysis_time
    
    video_key = request.args.get("video", current_video)
    state = get_or_create_state(video_key)
    
    if state.get('last_frame') is not None:
        analysis = analyze_with_gemini(state['last_frame'])
        state['ai_analysis'] = analysis
        last_ai_analysis = analysis
        last_analysis_time = datetime.now()
        
        return jsonify({
            "success": True,
            "analysis": analysis,
            "timestamp": last_analysis_time.strftime("%Y-%m-%d %H:%M:%S")
        })
    else:
        return jsonify({
            "success": False,
            "message": "No anomaly frame available for analysis. Adjust threshold or run a feed with people."
        })

@app.route("/get_threshold")
def get_threshold():
    return jsonify({"threshold": ANOMALY_THRESHOLD})

@app.route("/update_threshold", methods=["POST"])
def update_threshold():
    global ANOMALY_THRESHOLD
    try:
        data = request.get_json()
        val = int(data.get("threshold", 2))
        if 1 <= val <= 10:
            ANOMALY_THRESHOLD = val
            return jsonify({"success": True, "threshold": ANOMALY_THRESHOLD})
        return jsonify({"success": False, "message": "Threshold must be between 1 and 10"}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route("/get_api_key_status")
def get_api_key_status():
    is_set = client is not None and GEMINI_API_KEY != "YOUR_API_KEY_HERE"
    masked_key = ""
    if GEMINI_API_KEY and GEMINI_API_KEY != "YOUR_API_KEY_HERE":
        masked_key = "..." + GEMINI_API_KEY[-4:]
    return jsonify({"is_configured": is_set, "key_preview": masked_key})

@app.route("/update_api_key", methods=["POST"])
def update_api_key():
    global GEMINI_API_KEY, client
    try:
        data = request.get_json()
        key = data.get("api_key", "").strip().strip("'\"")
        if not key:
            return jsonify({"success": False, "message": "API key cannot be empty"}), 400
            
        GEMINI_API_KEY = key
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        # Write to .env file for persistence
        env_path = os.path.join(BASE_DIR, ".env")
        with open(env_path, "w") as f:
            f.write(f"GEMINI_API_KEY={GEMINI_API_KEY}\n")
            
        return jsonify({"success": True, "message": "API key updated and saved successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

from werkzeug.utils import secure_filename
import time

UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "videos")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/get_feeds")
def get_feeds():
    feeds_list = []
    for key, info in VIDEO_FEEDS.items():
        feeds_list.append({
            "key": key,
            "id": info["id"],
            "name": info["name"],
            "type": info["type"]
        })
    return jsonify(feeds_list)

@app.route("/upload_video", methods=["POST"])
def upload_video():
    if 'video' not in request.files:
        return jsonify({"success": False, "message": "No video file provided"}), 400
    
    file = request.files['video']
    if file.filename == '':
        return jsonify({"success": False, "message": "No file selected"}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        base, ext = os.path.splitext(filename)
        unique_name = f"uploaded_{int(time.time())}{ext}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_name)
        
        file.save(filepath)
        
        new_key = f"uploaded_{len(VIDEO_FEEDS) + 1}"
        new_id = f"CAM-0{len(VIDEO_FEEDS) + 1}"
        display_name = request.form.get("name", "").strip() or base.replace("_", " ").title()
        
        VIDEO_FEEDS[new_key] = {
            "id": new_id,
            "name": display_name,
            "path": filepath,
            "type": "uploaded"
        }
        
        return jsonify({
            "success": True,
            "message": "Video uploaded successfully!",
            "feed": {
                "key": new_key,
                "id": new_id,
                "name": display_name,
                "type": "uploaded"
            }
        })
        
    return jsonify({"success": False, "message": "Invalid file format. Supported: mp4, avi, mov, mkv"}), 400

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
