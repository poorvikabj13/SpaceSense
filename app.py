from flask import Flask, Response, render_template, jsonify, request
import cv2
from google import genai
from google.genai import types
import os
from PIL import Image
import io
import base64
from datetime import datetime

app = Flask(__name__)

VIDEO_MAP = {
    "video1": "static/videos/demo.mp4",
    "video2": "static/videos/demo2.mp4",
    "video3": "static/videos/demo3.mp4",
}

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
client = genai.Client(api_key=GEMINI_API_KEY)

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
            'last_frame': None
        }
    return video_states[video_key]

def analyze_with_gemini(frame):
    """Use Gemini AI to analyze the scene for anomalies"""
    try:
        # Convert frame to PIL Image
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_frame)
        
        # Save to bytes buffer
        img_byte_arr = io.BytesIO()
        pil_image.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        
        # Create prompt for Gemini
        prompt = """Analyze this surveillance footage frame. Describe:
1. Number of people visible
2. Any unusual activities or behaviors
3. Crowd density assessment
4. Potential security concerns

Provide a brief, professional analysis in 2-3 sentences."""
        
        # Generate analysis using new API
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=[
                types.Part.from_bytes(
                    data=img_byte_arr.read(),
                    mime_type='image/jpeg'
                ),
                prompt
            ]
        )
        return response.text
    except Exception as e:
        return f"AI Analysis unavailable: {str(e)}"

# Initialize HOG person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Anomaly threshold - trigger when this many or more people detected
ANOMALY_THRESHOLD = 2

def generate(video_key):
    global current_video
    current_video = video_key
    
    state = get_or_create_state(video_key)
    
    cap = cv2.VideoCapture(VIDEO_MAP[video_key])
    
    # Reset state for fresh video stream
    state['anomaly_score'] = 0
    state['confidence'] = 0.0
    state['status'] = "NORMAL FLOW"
    state['normal_frame_count'] = 0

    while True:
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
    state = get_or_create_state(current_video)
    return jsonify({
        "status": state['status'],
        "anomalies": state['anomaly_score'],
        "confidence": round(state['confidence'], 2),
        "ai_analysis": state.get('ai_analysis', '')
    })

@app.route("/analyze_ai")
def analyze_ai():
    """Trigger AI analysis on the current anomaly frame"""
    global last_ai_analysis, last_analysis_time
    
    state = get_or_create_state(current_video)
    
    if state.get('last_frame') is not None:
        # Perform AI analysis
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
            "message": "No anomaly frame available for analysis"
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
