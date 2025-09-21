# AI Therapy System - Research Data Collection Guide

This guide provides comprehensive information about the research data collection capabilities of the AI Therapy System, including data types, collection methods, and analysis approaches.

## 📊 Data Collection Overview

The AI Therapy System is designed as a comprehensive research platform that automatically collects detailed data about human-AI therapeutic interactions. All data is stored locally and can be exported in multiple formats for research analysis.

### Research Data Categories

#### 1. Session Data
- **Session Metadata**: Start/end times, duration, user ID, session type
- **Session Outcomes**: Completion status, therapeutic goals, user feedback
- **Risk Assessment**: Maximum risk level reached, crisis interventions used
- **Therapeutic Interventions**: Types of interventions, effectiveness ratings

#### 2. Emotion Detection Data
- **Real-time Emotions**: Detected emotions with timestamps and confidence scores
- **Face Detection**: Face detection status and bounding box coordinates
- **Calibration Data**: User-specific calibration results and baseline emotions
- **Accuracy Metrics**: Detection accuracy and confidence trends over time

#### 3. Conversation Data
- **User Messages**: Complete conversation history with timestamps
- **AI Responses**: System responses using NURSE framework
- **Sentiment Analysis**: Sentiment scores for user messages
- **Therapeutic Approaches**: Which NURSE components were used
- **Response Effectiveness**: Ratings of therapeutic response effectiveness

#### 4. Risk Assessment Data
- **Risk Scores**: Calculated risk scores with timestamps
- **Risk Factors**: Specific factors that contributed to risk assessment
- **Crisis Indicators**: Keywords and patterns that triggered crisis detection
- **Interventions**: Crisis interventions taken and escalation levels
- **Safety Protocols**: Safety protocol activations and outcomes

#### 5. Therapeutic Exercise Data
- **Exercise Usage**: Types of exercises used and completion rates
- **Exercise Effectiveness**: User ratings and completion statistics
- **Exercise Recommendations**: Personalized exercise suggestions
- **Progress Tracking**: Exercise progress and duration data

#### 6. System Performance Data
- **Detection Accuracy**: Emotion detection accuracy metrics
- **Response Times**: System response times for therapeutic interactions
- **System Load**: CPU and memory usage during sessions
- **Error Tracking**: System errors and recovery actions

## 🗄️ Database Schema

### Sessions Table
```sql
CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    user_id TEXT,
    session_type TEXT,
    status TEXT DEFAULT 'active',
    notes TEXT,
    risk_level INTEGER DEFAULT 0,
    therapeutic_interventions TEXT,
    session_outcome TEXT
);
```

### Emotion Detections Table
```sql
CREATE TABLE emotion_detections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    emotion TEXT NOT NULL,
    confidence REAL NOT NULL,
    face_detected BOOLEAN DEFAULT TRUE,
    frame_data TEXT,
    FOREIGN KEY (session_id) REFERENCES sessions (session_id)
);
```

### Conversations Table
```sql
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_message TEXT NOT NULL,
    system_response TEXT NOT NULL,
    sentiment_score REAL,
    emotion_context TEXT,
    therapeutic_approach TEXT,
    response_effectiveness INTEGER,
    FOREIGN KEY (session_id) REFERENCES sessions (session_id)
);
```

### Risk Assessments Table
```sql
CREATE TABLE risk_assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    risk_score INTEGER NOT NULL,
    risk_factors TEXT,
    crisis_indicators TEXT,
    intervention_taken TEXT,
    escalation_level INTEGER DEFAULT 0,
    notes TEXT,
    FOREIGN KEY (session_id) REFERENCES sessions (session_id)
);
```

### Interventions Table
```sql
CREATE TABLE interventions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    intervention_type TEXT NOT NULL,
    intervention_data TEXT,
    user_response TEXT,
    effectiveness_score INTEGER,
    duration_seconds INTEGER,
    FOREIGN KEY (session_id) REFERENCES sessions (session_id)
);
```

### User Feedback Table
```sql
CREATE TABLE user_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    feedback_type TEXT,
    rating INTEGER,
    comments TEXT,
    improvement_suggestions TEXT,
    FOREIGN KEY (session_id) REFERENCES sessions (session_id)
);
```

### System Performance Table
```sql
CREATE TABLE system_performance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    emotion_detection_accuracy REAL,
    response_time_ms INTEGER,
    system_load REAL,
    error_count INTEGER DEFAULT 0,
    FOREIGN KEY (session_id) REFERENCES sessions (session_id)
);
```

## 📈 Data Export Formats

### 1. JSON Export
```json
{
  "session": {
    "session_id": "session_1234567890",
    "start_time": "2024-01-15T10:30:00",
    "end_time": "2024-01-15T11:00:00",
    "user_id": "anonymous",
    "status": "completed"
  },
  "emotions": [
    {
      "timestamp": "2024-01-15T10:30:15",
      "emotion": "Sad",
      "confidence": 0.85,
      "face_detected": true
    }
  ],
  "conversations": [
    {
      "timestamp": "2024-01-15T10:30:20",
      "user_message": "I'm feeling really down today",
      "system_response": "I can see that you're feeling sad right now...",
      "sentiment_score": -0.6,
      "therapeutic_approach": "NURSE-Naming"
    }
  ],
  "risks": [
    {
      "timestamp": "2024-01-15T10:30:20",
      "risk_score": 3,
      "risk_factors": ["Negative sentiment", "Sad emotion"],
      "intervention_taken": "Supportive response"
    }
  ]
}
```

### 2. CSV Export
```csv
timestamp,emotion,confidence,face_detected,session_id
2024-01-15T10:30:15,Sad,0.85,true,session_1234567890
2024-01-15T10:30:20,Neutral,0.72,true,session_1234567890
2024-01-15T10:30:25,Happy,0.91,true,session_1234567890
```

### 3. Excel Export
Multi-sheet Excel files with:
- **Raw Data**: Complete session data
- **Emotion Summary**: Emotion statistics and distributions
- **Conversation Analysis**: Therapeutic approach effectiveness
- **Risk Assessment**: Risk progression and interventions
- **Session Summary**: Overall session metrics

## 🔬 Research Applications

### 1. Human-AI Interaction Studies

#### Research Questions
- How do users respond to AI therapeutic interventions?
- What factors influence user trust in AI therapy systems?
- How do users adapt their communication style with AI therapists?
- What are the patterns of therapeutic relationship development?

#### Data Analysis Approaches
- **Conversation Analysis**: Content analysis of user messages and AI responses
- **Sentiment Tracking**: Emotional progression throughout sessions
- **Engagement Metrics**: Session duration, message frequency, exercise completion
- **Trust Indicators**: User willingness to share personal information

#### Key Metrics
- Session duration and frequency
- Message length and complexity
- Sentiment score trends
- Therapeutic approach effectiveness ratings
- User feedback and satisfaction scores

### 2. Emotion Recognition Research

#### Research Questions
- How accurate is real-time emotion detection in therapeutic contexts?
- What factors affect emotion detection confidence?
- How do emotional states change during therapeutic interactions?
- What are the patterns of emotional regulation?

#### Data Analysis Approaches
- **Accuracy Analysis**: Detection accuracy vs. ground truth
- **Confidence Trends**: Confidence score patterns over time
- **Emotion Transitions**: State transition probabilities
- **Calibration Studies**: User-specific calibration effectiveness

#### Key Metrics
- Emotion detection accuracy
- Confidence score distributions
- Face detection success rates
- Emotional state transition frequencies
- Calibration effectiveness measures

### 3. Crisis Detection and Intervention Research

#### Research Questions
- How effective are automated crisis detection algorithms?
- What are the false positive and false negative rates?
- How do users respond to crisis interventions?
- What factors predict crisis situations?

#### Data Analysis Approaches
- **Risk Assessment Validation**: Comparing detected risks with outcomes
- **Intervention Effectiveness**: Measuring crisis intervention success
- **Pattern Recognition**: Identifying crisis prediction patterns
- **User Response Analysis**: How users respond to crisis alerts

#### Key Metrics
- Risk score accuracy
- Crisis detection sensitivity and specificity
- Intervention response rates
- False positive/negative rates
- Crisis resolution outcomes

### 4. Therapeutic Effectiveness Research

#### Research Questions
- Which therapeutic approaches are most effective?
- How do different NURSE framework components perform?
- What factors influence therapeutic success?
- How does AI therapy compare to human therapy?

#### Data Analysis Approaches
- **Effectiveness Comparison**: Comparing different therapeutic approaches
- **Outcome Prediction**: Predicting therapeutic success
- **Component Analysis**: Analyzing NURSE framework component effectiveness
- **Longitudinal Studies**: Tracking progress over multiple sessions

#### Key Metrics
- Therapeutic approach effectiveness ratings
- Session outcome measures
- User satisfaction scores
- Progress indicators
- Intervention success rates

## 📊 Statistical Analysis

### Descriptive Statistics

#### Emotion Analysis
```python
# Emotion distribution
emotion_counts = df['emotion'].value_counts()
emotion_percentages = df['emotion'].value_counts(normalize=True) * 100

# Confidence statistics
confidence_stats = df['confidence'].describe()
confidence_by_emotion = df.groupby('emotion')['confidence'].describe()
```

#### Session Analysis
```python
# Session duration analysis
session_durations = df.groupby('session_id')['timestamp'].agg(['min', 'max'])
session_durations['duration'] = session_durations['max'] - session_durations['min']

# Conversation analysis
message_lengths = df['user_message'].str.len()
response_lengths = df['system_response'].str.len()
```

#### Risk Assessment Analysis
```python
# Risk score distribution
risk_distribution = df['risk_score'].value_counts().sort_index()

# Risk progression
risk_progression = df.groupby('session_id')['risk_score'].agg(['min', 'max', 'mean'])
```

### Inferential Statistics

#### Correlation Analysis
```python
# Emotion-confidence correlation
emotion_confidence_corr = df[['emotion', 'confidence']].corr()

# Sentiment-risk correlation
sentiment_risk_corr = df[['sentiment_score', 'risk_score']].corr()
```

#### Regression Analysis
```python
# Predicting therapeutic effectiveness
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder

# Encode categorical variables
le = LabelEncoder()
df['emotion_encoded'] = le.fit_transform(df['emotion'])
df['approach_encoded'] = le.fit_transform(df['therapeutic_approach'])

# Fit regression model
X = df[['emotion_encoded', 'sentiment_score', 'confidence']]
y = df['response_effectiveness']
model = LinearRegression().fit(X, y)
```

#### Time Series Analysis
```python
# Emotion trends over time
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.set_index('timestamp', inplace=True)

# Resample by hour
hourly_emotions = df['emotion'].resample('H').value_counts()
```

### Machine Learning Applications

#### Emotion Prediction
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Features for emotion prediction
features = ['confidence', 'sentiment_score', 'message_length', 'hour']
X = df[features]
y = df['emotion']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate
accuracy = model.score(X_test, y_test)
```

#### Risk Prediction
```python
# Features for risk prediction
risk_features = ['sentiment_score', 'emotion', 'message_length', 'session_duration']
X_risk = df[risk_features]
y_risk = df['risk_score']

# Binary classification (high risk vs low risk)
y_risk_binary = (y_risk >= 7).astype(int)

# Train risk prediction model
risk_model = RandomForestClassifier()
risk_model.fit(X_risk, y_risk_binary)
```

## 🔍 Data Visualization

### Real-time Dashboards

#### Emotion Timeline
```python
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df['timestamp'],
    y=df['confidence'],
    mode='markers',
    marker=dict(
        color=df['emotion'],
        size=8
    ),
    text=df['emotion']
))
fig.update_layout(title='Emotion Detection Timeline')
fig.show()
```

#### Risk Assessment Chart
```python
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df['timestamp'],
    y=df['risk_score'],
    mode='lines+markers',
    line=dict(color='red', width=2)
))
fig.add_hline(y=7, line_dash="dash", line_color="orange")
fig.update_layout(title='Risk Assessment Over Time')
fig.show()
```

#### Therapeutic Effectiveness
```python
# Effectiveness by therapeutic approach
effectiveness_by_approach = df.groupby('therapeutic_approach')['response_effectiveness'].mean()

fig = go.Figure(data=[
    go.Bar(x=effectiveness_by_approach.index, y=effectiveness_by_approach.values)
])
fig.update_layout(title='Therapeutic Approach Effectiveness')
fig.show()
```

### Research Reports

#### Session Summary Report
```python
def generate_session_report(session_id):
    session_data = get_session_data(session_id)
    
    report = {
        'session_info': {
            'duration': session_data['end_time'] - session_data['start_time'],
            'message_count': len(session_data['conversations']),
            'emotion_count': len(session_data['emotions']),
            'max_risk_score': max([r['risk_score'] for r in session_data['risks']])
        },
        'emotion_analysis': {
            'dominant_emotion': most_common_emotion(session_data['emotions']),
            'emotion_transitions': count_emotion_transitions(session_data['emotions']),
            'confidence_trend': calculate_confidence_trend(session_data['emotions'])
        },
        'therapeutic_analysis': {
            'approaches_used': list(set([c['therapeutic_approach'] for c in session_data['conversations']])),
            'average_effectiveness': np.mean([c['response_effectiveness'] for c in session_data['conversations']]),
            'sentiment_progression': calculate_sentiment_progression(session_data['conversations'])
        }
    }
    
    return report
```

## 📋 Research Protocols

### Data Collection Protocol

#### 1. Informed Consent
- Clear explanation of data collection purposes
- Information about data storage and usage
- User rights and data control options
- Anonymization and privacy measures

#### 2. Data Collection Procedures
- Standardized session protocols
- Consistent data collection methods
- Quality control measures
- Error handling and validation

#### 3. Data Management
- Secure local storage
- Regular backups
- Data integrity checks
- Access control measures

### Analysis Protocol

#### 1. Data Preprocessing
- Data cleaning and validation
- Missing data handling
- Outlier detection and treatment
- Data transformation and normalization

#### 2. Statistical Analysis
- Descriptive statistics
- Inferential statistics
- Hypothesis testing
- Effect size calculations

#### 3. Machine Learning Analysis
- Feature engineering
- Model selection and validation
- Cross-validation procedures
- Performance evaluation

### Reporting Protocol

#### 1. Research Documentation
- Methodology documentation
- Data collection procedures
- Analysis methods and tools
- Results interpretation

#### 2. Ethical Considerations
- Privacy protection measures
- Data anonymization procedures
- User consent documentation
- Institutional review board approval

#### 3. Reproducibility
- Code documentation
- Data sharing protocols
- Analysis reproducibility
- Results validation

## 🛡️ Privacy and Ethics

### Data Privacy

#### Local Storage
- All data stored locally on user's device
- No cloud transmission or external storage
- User maintains full control over data
- Optional data anonymization features

#### Data Control
- User can export their own data
- User can delete their data
- User can opt out of data collection
- User can control data sharing

### Ethical Considerations

#### Informed Consent
- Clear explanation of research purposes
- Transparent data collection procedures
- User rights and control options
- Voluntary participation

#### Beneficence
- System designed to help users
- Crisis intervention capabilities
- Professional referral recommendations
- User safety prioritization

#### Non-maleficence
- Harm prevention measures
- Crisis detection and intervention
- Safety protocols and procedures
- Professional oversight recommendations

### Research Ethics

#### Institutional Review
- IRB approval recommended
- Ethical review procedures
- Informed consent protocols
- Data protection measures

#### Transparency
- Open source code
- Transparent algorithms
- Clear limitations disclosure
- Honest reporting of results

## 📚 Research Resources

### Statistical Software Integration

#### R Integration
```r
# Load data from CSV export
data <- read.csv("emotion_data.csv")

# Basic analysis
summary(data$confidence)
table(data$emotion)

# Advanced analysis
library(ggplot2)
ggplot(data, aes(x=emotion, y=confidence)) + 
  geom_boxplot() + 
  theme_minimal()
```

#### Python Integration
```python
# Load data
import pandas as pd
df = pd.read_csv('emotion_data.csv')

# Analysis
import scipy.stats as stats
from scipy.stats import chi2_contingency

# Chi-square test for emotion distribution
contingency_table = pd.crosstab(df['emotion'], df['session_id'])
chi2, p_value, dof, expected = chi2_contingency(contingency_table)
```

### Research Tools

#### Data Analysis Tools
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **SciPy**: Statistical analysis
- **Scikit-learn**: Machine learning
- **Statsmodels**: Statistical modeling

#### Visualization Tools
- **Matplotlib**: Basic plotting
- **Seaborn**: Statistical visualization
- **Plotly**: Interactive visualization
- **Bokeh**: Web-based visualization

#### Research Software
- **R**: Statistical computing
- **SPSS**: Statistical analysis
- **JASP**: Open-source statistics
- **Jupyter**: Interactive notebooks

---

**Note**: This research guide is designed to help researchers effectively use the AI Therapy System for academic and clinical research. Always ensure compliance with institutional ethics requirements and data protection regulations.
