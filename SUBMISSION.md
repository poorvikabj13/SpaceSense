# SpaceSense - TechSprint 2026 Submission

## Team Information
- **Team Name**: Posh
- **Project Name**: SpaceSense
- **GitHub Repository**: https://github.com/Poorvikabj13/SpaceSense

## 100-Word Project Description

SpaceSense is an AI-powered pedestrian anomaly detection system designed for real-time crowd monitoring in public spaces. Using OpenCV's HOG descriptor for person detection and Google Gemini AI for intelligent scene analysis, the system automatically identifies crowd density anomalies and provides natural language insights about security concerns. The web-based dashboard displays live video feeds with bounding boxes around detected individuals, real-time anomaly alerts, and confidence scoring. When anomalies are detected, users can trigger Google Gemini's advanced AI to generate detailed scene assessments. SpaceSense addresses critical safety needs in offices, educational institutions, retail stores, events, and public transport stations.

## Google Technologies Used

### Primary Technology
- **Google Gemini API (gemini-2.0-flash-exp)** - AI-powered scene analysis and anomaly description
  - Analyzes surveillance footage frames
  - Generates natural language security assessments
  - Provides intelligent crowd density analysis
  - Identifies unusual behaviors and potential concerns

### Implementation Details
- **API Integration**: google-genai Python SDK
- **Model**: gemini-2.0-flash-exp (latest multimodal model)
- **Features Used**: 
  - Vision capabilities for image analysis
  - Text generation for professional security reports
  - Real-time inference for immediate insights

## Technical Stack

### Backend
- **Flask** - Web framework
- **Python 3.8+** - Core language
- **OpenCV** - Computer vision and HOG person detection
- **Google Gemini AI** - Scene analysis

### Frontend
- **HTML5** - Structure
- **CSS3** - Modern gradient design with animations
- **JavaScript** - Real-time updates and AJAX

### Computer Vision
- **HOG Descriptor** - Pedestrian detection
- **Frame Processing** - Real-time video analysis
- **Bounding Box Visualization** - Person tracking

## Key Features

1. **Real-time Person Detection** - HOG-based pedestrian detection with green bounding boxes
2. **Anomaly Detection** - Automatic alerts when crowd threshold exceeded (2+ people)
3. **AI-Powered Analysis** - Google Gemini integration for intelligent scene understanding
4. **Multi-Video Support** - Monitor multiple camera feeds
5. **Live Dashboard** - Real-time status updates, confidence scoring, and anomaly count
6. **Professional UI** - Modern gradient design with smooth animations

## Innovation Highlights

✅ **Intelligent Analysis** - Goes beyond simple detection with AI-powered insights  
✅ **Real-world Application** - Solves actual security and safety challenges  
✅ **Scalable Architecture** - Can extend to multiple cameras and locations  
✅ **User-Friendly** - Intuitive dashboard with visual feedback  
✅ **Google AI Integration** - Leverages cutting-edge Gemini technology  

## Use Cases

- 🏢 **Office Buildings** - Monitor lobby and entrance areas
- 🏫 **Educational Institutions** - Track crowd density in hallways
- 🏪 **Retail Stores** - Analyze customer flow and congestion
- 🎪 **Events** - Ensure safe crowd levels
- 🚇 **Public Transport** - Monitor station platforms

## Social Impact

SpaceSense addresses critical public safety needs by:
- **Preventing overcrowding** in public spaces
- **Early detection** of unusual crowd behaviors
- **Automated monitoring** reducing manual surveillance burden
- **Data-driven insights** for better security planning
- **Scalable solution** accessible to organizations of all sizes

## Feasibility & Scalability

### Current Implementation
- ✅ Working MVP with real-time detection
- ✅ Google Gemini AI integration
- ✅ Multi-video support
- ✅ Web-based accessible interface

### Future Enhancements
- 📱 **Mobile App** - Flutter-based mobile monitoring
- ☁️ **Firebase Integration** - Cloud storage and real-time alerts
- 📊 **Analytics Dashboard** - Historical data and trends
- 🔔 **Smart Notifications** - Email/SMS alerts via Firebase Cloud Messaging
- 🎥 **Multi-Camera Grid** - Simultaneous monitoring of multiple locations
- 🤖 **Advanced AI** - Behavior prediction and pattern recognition

## Demo Video
[Link to 3-minute demo video - to be uploaded]

## Project Deck/PPT
[Link to presentation - to be uploaded]

## Installation & Setup

### Prerequisites
- Python 3.8+
- Google Gemini API key

### Quick Start
```bash
# Clone repository
git clone https://github.com/Poorvikabj13/SpaceSense.git
cd SpaceSense

# Install dependencies
pip install -r requirements.txt

# Set API key
export GEMINI_API_KEY="your-api-key-here"

# Run application
python app.py

# Open browser
http://localhost:8080
```

## Project Structure
```
SpaceSense/
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Frontend dashboard
├── static/
│   └── videos/           # Demo video files
├── requirements.txt      # Python dependencies
├── README.md             # Documentation
└── .env.example          # Environment template
```

## Screenshots

### Main Dashboard
[Screenshot showing video feed with person detection and AI analysis panel]

### Anomaly Detection
[Screenshot showing multiple people detected with "ANOMALY DETECTED" alert]

### AI Analysis
[Screenshot showing Gemini AI's scene analysis output]

## Acknowledgments

- **Google Developer Groups** - For organizing TechSprint
- **GDG VVIET** - For hosting the hackathon
- **Google Gemini Team** - For the powerful AI API

---

**Submitted for TechSprint 2026 - Open Innovation Track**  
**Team Posh**  
**January 2026**
