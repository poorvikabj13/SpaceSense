# SpaceSense 🚨
**AI-Powered Pedestrian Anomaly Detection System**

Built for TechSprint Hackathon by GDG VVIET

## 🌟 Overview
SpaceSense is an intelligent surveillance system that uses computer vision and Google Gemini AI to detect and analyze crowd anomalies in real-time. Perfect for public spaces, events, and security monitoring.

## ✨ Features

### 🎯 Core Capabilities
- **Real-time Person Detection** - HOG-based pedestrian detection with bounding boxes
- **Anomaly Detection** - Automatic crowd density analysis and alert system
- **AI-Powered Analysis** - Google Gemini integration for intelligent scene understanding
- **Multi-Video Support** - Monitor multiple camera feeds
- **Live Dashboard** - Real-time status updates and confidence scoring

### 🤖 Google Technologies Used
- **Google Gemini API** (gemini-1.5-flash) - AI-powered scene analysis and anomaly description
- **Python** - Backend processing
- **OpenCV** - Computer vision and person detection

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Webcam or video files
- Google Gemini API key

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd SpaceSense
```

2. **Install dependencies**
```bash
pip install flask opencv-python google-generativeai pillow
```

3. **Set up Gemini API Key**
   - Get your free API key from: https://makersuite.google.com/app/apikey
   - Create a `.env` file or set environment variable:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

4. **Run the application**
```bash
python app.py
```

5. **Open in browser**
```
http://localhost:8080
```

## 📖 How It Works

1. **Video Processing** - Captures frames from video feed
2. **Person Detection** - Uses HOG descriptor to detect pedestrians
3. **Anomaly Trigger** - Flags when crowd threshold exceeded (2+ people)
4. **AI Analysis** - Click "Analyze with AI" to get Gemini's intelligent scene description
5. **Real-time Updates** - Dashboard shows live status, confidence, and anomaly count

## 🎨 Tech Stack

- **Backend**: Flask (Python)
- **Computer Vision**: OpenCV (HOG Person Detector)
- **AI**: Google Gemini 1.5 Flash
- **Frontend**: HTML, CSS, JavaScript
- **Real-time**: MJPEG streaming

## 📊 Project Structure

```
SpaceSense/
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Frontend dashboard
├── static/
│   └── videos/           # Demo video files
├── .env.example          # Environment variables template
└── README.md             # This file
```

## 🎯 Use Cases

- 🏢 **Office Buildings** - Monitor lobby and entrance areas
- 🏫 **Educational Institutions** - Track crowd density in hallways
- 🏪 **Retail Stores** - Analyze customer flow and congestion
- 🎪 **Events** - Ensure safe crowd levels
- 🚇 **Public Transport** - Monitor station platforms

## 🏆 Hackathon Submission

**TechSprint 2026** - GDG VVIET × Google Developer Groups

### Innovation Highlights
✅ Real-time AI-powered anomaly detection  
✅ Google Gemini integration for intelligent analysis  
✅ User-friendly dashboard with live updates  
✅ Scalable architecture for multiple cameras  
✅ Practical solution for real-world security needs  

## 📝 License
MIT License

## 👥 Team
**Team Posh**

## 🙏 Acknowledgments
- Google Developer Groups
- GDG VVIET
- TechSprint Organizers
