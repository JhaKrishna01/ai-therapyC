# AI Therapy System - Emotion & Risk Detection Therapeutic AI

A comprehensive, professional-grade AI therapy system designed for emotion detection, therapeutic intervention, and research data collection. This system implements the NURSE framework for therapeutic responses and includes robust crisis detection and safety guardrails.

## 🎯 Project Overview

This capstone research project provides a complete therapeutic AI system that combines real-time emotion detection with evidence-based therapeutic interventions. The system is designed to serve both as a functional therapeutic tool and a robust research platform for studying human-AI therapeutic interactions.

### Key Features

- **Real-time Emotion Detection**: Webcam-based emotion recognition using OpenCV and TensorFlow
- **NURSE Framework Implementation**: Naming, Understanding, Respecting, Supporting, Exploring therapeutic responses
- **Crisis Detection & Safety Guardrails**: Automated risk assessment and crisis intervention protocols
- **Therapeutic Exercises**: Guided breathing, mindfulness, journaling, and mood-lifting activities
- **Professional GUI**: Modern CustomTkinter interface with integrated camera feed
- **Research Data Collection**: Comprehensive logging and export capabilities
- **Real-time Analytics**: Live visualization of emotional states and therapeutic progress

## 🏗️ System Architecture

### Core Components

1. **Emotion Detection Module** (`emotion_detection/`)
   - Real-time facial emotion recognition
   - Confidence scoring and calibration
   - Camera integration and frame processing

2. **Therapeutic System** (`therapeutic_system/`)
   - NURSE framework implementation
   - Context-aware empathetic responses
   - Sentiment analysis and conversation tracking

3. **Crisis Detection** (`crisis_detection/`)
   - Risk assessment algorithms
   - Crisis intervention protocols
   - Safety manager with helpline integration

4. **Database Management** (`database/`)
   - SQLite database for session storage
   - Comprehensive data logging
   - Research data export capabilities

5. **GUI Interface** (`gui/`)
   - Professional CustomTkinter interface
   - Real-time camera feed display
   - Session management and analytics

6. **Therapeutic Exercises** (`exercises/`)
   - Breathing exercises and guided meditation
   - Journaling prompts and mood-lifting activities
   - Progressive muscle relaxation

7. **Data Visualization** (`visualization/`)
   - Real-time emotion charts and analytics
   - Session summaries and progress tracking
   - Export-ready research visualizations

8. **Export System** (`export/`)
   - Multi-format data export (CSV, JSON, Excel)
   - Research report generation
   - Statistical analysis tools

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Webcam access
- Windows 10/11, macOS, or Linux

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-therapy-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

### First Run Setup

1. **Start the camera** - Click "Start Camera" in the main interface
2. **Calibrate emotion detection** - Go to Tools > Camera Calibration
3. **Start a session** - Click "Start Session" to begin therapy
4. **Begin conversation** - Type messages and receive therapeutic responses

## 📋 Detailed Setup Instructions

### System Requirements

#### Hardware Requirements
- **CPU**: Intel i5 or AMD Ryzen 5 (minimum)
- **RAM**: 8GB (16GB recommended)
- **Storage**: 2GB free space
- **Camera**: USB webcam or built-in camera
- **Display**: 1920x1080 resolution (minimum)

#### Software Requirements
- **Operating System**: Windows 10/11, macOS 10.15+, or Ubuntu 18.04+
- **Python**: 3.8 or higher
- **Webcam drivers**: Latest version for your camera

### Installation Steps

#### 1. Python Environment Setup

```bash
# Create virtual environment (recommended)
python -m venv therapy_env

# Activate virtual environment
# Windows:
therapy_env\Scripts\activate
# macOS/Linux:
source therapy_env/bin/activate

# Upgrade pip
python -m pip install --upgrade pip
```

#### 2. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
python -c "import customtkinter, cv2, tensorflow; print('All packages installed successfully')"
```

#### 3. Database Initialization

The system will automatically create the SQLite database on first run. No manual setup required.

#### 4. Camera Configuration

1. Connect your webcam
2. Test camera access:
   ```python
   import cv2
   cap = cv2.VideoCapture(0)
   ret, frame = cap.read()
   print(f"Camera working: {ret}")
   cap.release()
   ```

#### 5. Configuration Setup

Edit `config/settings.json` to customize system settings:

```json
{
  "camera": {
    "default_index": 0,
    "resolution": {"width": 640, "height": 480}
  },
  "emotion_detection": {
    "confidence_threshold": 0.3
  },
  "crisis_detection": {
    "risk_threshold": 7,
    "enabled": true
  }
}
```

## 🎮 User Guide

### Main Interface

#### Therapy Session Tab
- **Camera Feed**: Real-time emotion detection display
- **Emotion Display**: Current detected emotion and confidence
- **Risk Indicator**: Real-time risk assessment
- **Chat Interface**: Therapeutic conversation area
- **Session Controls**: Start/stop session and camera

#### Session Management Tab
- **Session List**: View all therapy sessions
- **Session Details**: Detailed session information
- **Export Options**: Export session data for research

#### Therapeutic Exercises Tab
- **Exercise Categories**: Breathing, mindfulness, journaling, etc.
- **Exercise Display**: Step-by-step exercise instructions
- **Progress Tracking**: Real-time exercise progress

#### Analytics Tab
- **Real-time Charts**: Emotion trends and distributions
- **Session Reports**: Detailed analytics and statistics
- **Export Tools**: Generate research reports

#### Settings Tab
- **Camera Settings**: Configure camera parameters
- **Database Management**: Backup and maintenance
- **Export Settings**: Configure data export options

### Using the System

#### Starting a Therapy Session

1. **Launch the application**
2. **Start the camera** - Click "Start Camera"
3. **Calibrate detection** - Tools > Camera Calibration (optional)
4. **Start session** - Click "Start Session"
5. **Begin conversation** - Type your thoughts and feelings

#### Therapeutic Features

- **Emotion Recognition**: System detects emotions in real-time
- **NURSE Responses**: Context-aware therapeutic responses
- **Crisis Detection**: Automatic risk assessment and intervention
- **Exercise Recommendations**: Personalized therapeutic activities
- **Progress Tracking**: Session analytics and emotional trends

#### Crisis Intervention

If crisis indicators are detected:
1. **Automatic Alert**: System displays crisis intervention dialog
2. **Resource Provision**: Crisis hotlines and resources provided
3. **Safety Planning**: Guided safety plan creation
4. **Professional Referral**: Encouragement to seek professional help

## 🔬 Research Features

### Data Collection

The system automatically collects comprehensive data for research:

#### Session Data
- Session metadata (start/end times, duration, outcomes)
- User interactions and system responses
- Therapeutic interventions used
- Risk assessments and crisis interventions

#### Emotion Data
- Real-time emotion detection with timestamps
- Confidence scores and face detection status
- Emotional state transitions and patterns
- Calibration and accuracy metrics

#### Conversation Data
- User messages and AI responses
- Sentiment analysis scores
- Therapeutic approach used (NURSE framework)
- Response effectiveness ratings

#### Risk Assessment Data
- Risk scores and assessment factors
- Crisis indicators detected
- Interventions taken and escalation levels
- Safety protocol activations

### Export Capabilities

#### Data Formats
- **CSV**: Raw data for statistical analysis
- **JSON**: Structured data for programmatic analysis
- **Excel**: Multi-sheet reports with summaries
- **SQLite**: Direct database access

#### Export Types
- **Session Export**: Complete session data
- **Emotion Analysis**: Emotion detection statistics
- **Conversation Analysis**: Chat interaction analysis
- **Risk Assessment**: Crisis detection data
- **Research Reports**: Comprehensive analytics

### Statistical Analysis

The system provides built-in statistical analysis:

- **Emotion Distribution**: Frequency and patterns of emotions
- **Confidence Trends**: Detection accuracy over time
- **Risk Progression**: Risk level changes during sessions
- **Therapeutic Effectiveness**: Response success rates
- **Session Analytics**: Duration, outcomes, and patterns

## 🛡️ Safety & Ethics

### Crisis Intervention

#### Automatic Detection
- Keyword monitoring for crisis indicators
- Emotion pattern analysis for distress
- Risk scoring and escalation protocols
- Immediate intervention activation

#### Crisis Resources
- **National Suicide Prevention Lifeline**: 988
- **Crisis Text Line**: Text HOME to 741741
- **Emergency Services**: 911
- **Mental Health America**: 1-800-273-8255

#### Safety Protocols
- **Level 0-1**: Low risk - Standard monitoring
- **Level 2-3**: Moderate risk - Increased monitoring
- **Level 4**: High risk - Crisis intervention
- **Level 5**: Emergency - Immediate response

### Privacy & Confidentiality

#### Data Protection
- Local data storage (no cloud transmission)
- User consent for data collection
- Anonymization options for research
- Secure database encryption

#### Ethical Considerations
- Clear disclaimers about AI limitations
- Professional referral recommendations
- User control over data sharing
- Transparent crisis intervention protocols

## 🔧 Technical Documentation

### System Architecture

```
AI Therapy System
├── Main Application (main.py)
├── GUI Interface (gui/)
├── Emotion Detection (emotion_detection/)
├── Therapeutic System (therapeutic_system/)
├── Crisis Detection (crisis_detection/)
├── Database Management (database/)
├── Therapeutic Exercises (exercises/)
├── Data Visualization (visualization/)
├── Export System (export/)
└── Configuration (config/)
```

### Database Schema

#### Sessions Table
- `session_id`: Unique session identifier
- `start_time`, `end_time`: Session duration
- `user_id`: User identifier
- `status`: Session status (active/completed)
- `risk_level`: Maximum risk level reached
- `session_outcome`: Session completion status

#### Emotion Detections Table
- `id`: Auto-incrementing ID
- `session_id`: Foreign key to sessions
- `timestamp`: Detection timestamp
- `emotion`: Detected emotion
- `confidence`: Detection confidence score
- `face_detected`: Boolean face detection status

#### Conversations Table
- `id`: Auto-incrementing ID
- `session_id`: Foreign key to sessions
- `user_message`: User input text
- `system_response`: AI response text
- `sentiment_score`: Sentiment analysis score
- `therapeutic_approach`: NURSE framework component used

#### Risk Assessments Table
- `id`: Auto-incrementing ID
- `session_id`: Foreign key to sessions
- `risk_score`: Calculated risk score
- `risk_factors`: JSON array of risk factors
- `crisis_indicators`: JSON array of crisis indicators
- `intervention_taken`: Intervention action taken

### API Documentation

#### EmotionDetector Class
```python
class EmotionDetector:
    def start_camera(self, camera_index: int = 0) -> bool
    def stop_camera(self)
    def get_current_state(self) -> Dict
    def calibrate_detection(self, frames: int = 30) -> Dict
    def get_emotion_history(self, max_items: int = 10) -> List[Dict]
```

#### NURSEFramework Class
```python
class NURSEFramework:
    def generate_response(self, user_input: str, emotion: str, 
                         confidence: float, context: Dict) -> Dict
    def analyze_sentiment(self, text: str) -> float
    def assess_risk_level(self, text: str, emotion: str) -> Tuple[int, List[str]]
```

#### CrisisDetector Class
```python
class CrisisDetector:
    def analyze_text(self, text: str) -> Dict
    def analyze_emotion_pattern(self, emotion_history: List[Dict]) -> Dict
    def monitor_session(self, session_data: Dict) -> Dict
    def create_safety_plan(self, preferences: Dict = None) -> Dict
```

### Configuration Options

#### System Configuration
- `debug_mode`: Enable debug logging
- `log_level`: Logging verbosity level
- `data_retention_days`: Data cleanup interval

#### Camera Configuration
- `default_index`: Default camera device index
- `resolution`: Camera resolution settings
- `fps`: Frames per second
- `auto_start`: Automatically start camera

#### Emotion Detection Configuration
- `model_path`: Path to emotion detection model
- `confidence_threshold`: Minimum confidence for detection
- `update_interval`: Detection update frequency
- `calibration_frames`: Frames for calibration

#### Crisis Detection Configuration
- `enabled`: Enable crisis detection
- `risk_threshold`: Crisis intervention threshold
- `monitoring_active`: Enable continuous monitoring
- `auto_escalation`: Automatic escalation enabled

## 🐛 Troubleshooting

### Common Issues

#### Camera Not Working
1. **Check camera permissions**
2. **Verify camera is not used by another application**
3. **Try different camera index in settings**
4. **Update camera drivers**

#### Emotion Detection Issues
1. **Ensure good lighting**
2. **Position face clearly in camera view**
3. **Run camera calibration**
4. **Check confidence threshold settings**

#### Database Errors
1. **Check file permissions**
2. **Verify disk space**
3. **Run database backup/restore**
4. **Check SQLite installation**

#### GUI Issues
1. **Update graphics drivers**
2. **Check display scaling settings**
3. **Verify CustomTkinter installation**
4. **Try different theme settings**

### Performance Optimization

#### System Performance
- **Close unnecessary applications**
- **Increase system RAM if possible**
- **Use SSD storage for better I/O**
- **Update graphics drivers**

#### Application Performance
- **Reduce camera resolution if needed**
- **Lower emotion detection update frequency**
- **Disable real-time visualization if laggy**
- **Clean up old session data regularly**

### Error Logs

Check log files in the `logs/` directory:
- `therapy_system.log`: Main application log
- `crisis_events_YYYYMMDD.json`: Crisis intervention logs
- `error.log`: Error-specific logging

## 📊 Research Applications

### Capstone Project Usage

This system is designed for capstone research projects focusing on:

#### Human-AI Interaction Research
- **Therapeutic Relationship**: How users interact with AI therapists
- **Emotion Recognition**: Accuracy and effectiveness of emotion detection
- **Crisis Intervention**: Effectiveness of automated crisis detection
- **User Engagement**: Patterns of therapeutic engagement

#### Clinical Research Applications
- **Therapeutic Effectiveness**: Measuring therapeutic outcomes
- **Risk Assessment**: Validating crisis detection algorithms
- **User Experience**: Studying user comfort and trust
- **Ethical Considerations**: AI therapy ethics and limitations

#### Data Analysis Opportunities
- **Emotional Patterns**: Long-term emotional state analysis
- **Therapeutic Progress**: Measuring improvement over time
- **Crisis Prediction**: Early warning system development
- **Personalization**: Customizing therapeutic approaches

### Research Methodology

#### Data Collection Protocol
1. **Informed Consent**: Clear explanation of data collection
2. **Anonymization**: Optional data anonymization
3. **Ethics Approval**: Institutional review board approval
4. **Data Security**: Secure local storage and handling

#### Analysis Framework
1. **Quantitative Analysis**: Statistical analysis of emotions and responses
2. **Qualitative Analysis**: Content analysis of conversations
3. **Mixed Methods**: Combining quantitative and qualitative approaches
4. **Longitudinal Studies**: Tracking changes over time

#### Export for Analysis
- **Raw Data**: Complete session data for custom analysis
- **Processed Data**: Pre-processed statistics and summaries
- **Visualizations**: Ready-to-use charts and graphs
- **Reports**: Comprehensive research reports

## 🤝 Contributing

### Development Setup

1. **Fork the repository**
2. **Create feature branch**
3. **Make changes**
4. **Test thoroughly**
5. **Submit pull request**

### Code Standards

- **Python PEP 8**: Follow Python style guidelines
- **Type Hints**: Use type annotations
- **Documentation**: Document all functions and classes
- **Testing**: Include unit tests for new features
- **Logging**: Use appropriate logging levels

### Testing

```bash
# Run basic tests
python -m pytest tests/

# Test specific modules
python -m pytest tests/test_emotion_detection.py
python -m pytest tests/test_therapeutic_system.py
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

### Technical Support
- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check this README and code comments
- **Community**: Join discussions in GitHub Discussions

### Crisis Support
If you or someone you know is in crisis:
- **National Suicide Prevention Lifeline**: 988
- **Crisis Text Line**: Text HOME to 741741
- **Emergency Services**: 911

## 🙏 Acknowledgments

- **OpenCV Community**: For computer vision capabilities
- **TensorFlow Team**: For machine learning framework
- **CustomTkinter**: For modern GUI components
- **Mental Health Professionals**: For therapeutic guidance
- **Research Community**: For evidence-based approaches

---

**Disclaimer**: This AI therapy system is designed for research and educational purposes. It is not a replacement for professional mental health care. Always consult with qualified mental health professionals for clinical treatment.
