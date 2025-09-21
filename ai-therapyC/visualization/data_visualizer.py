"""
Data Visualization and Analytics Dashboard
Provides real-time emotion visualization and comprehensive analytics for research
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Optional, Tuple
import datetime
import json
import threading
import time

class DataVisualizer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.emotion_data = []
        self.session_data = []
        self.is_real_time_active = False
        self.update_interval = 1.0  # seconds
        
        # Set up matplotlib style
        plt.style.use('seaborn-v0_8')
        
        # Color mapping for emotions
        self.emotion_colors = {
            'Happy': '#2E8B57',      # Sea Green
            'Sad': '#4169E1',        # Royal Blue
            'Angry': '#DC143C',      # Crimson
            'Fear': '#FF8C00',       # Dark Orange
            'Surprise': '#FFD700',   # Gold
            'Disgust': '#8B4513',    # Saddle Brown
            'Neutral': '#708090'     # Slate Gray
        }
        
        # Initialize real-time plotting
        self._setup_real_time_plotting()
    
    def _setup_real_time_plotting(self):
        """Setup real-time plotting components"""
        self.fig, self.axes = plt.subplots(2, 2, figsize=(12, 8))
        self.fig.suptitle('AI Therapy System - Real-time Analytics', fontsize=16)
        
        # Configure subplots
        self.axes[0, 0].set_title('Emotion Timeline')
        self.axes[0, 0].set_xlabel('Time')
        self.axes[0, 0].set_ylabel('Emotion')
        
        self.axes[0, 1].set_title('Emotion Distribution')
        self.axes[0, 1].set_xlabel('Emotion')
        self.axes[0, 1].set_ylabel('Count')
        
        self.axes[1, 0].set_title('Confidence Levels')
        self.axes[1, 0].set_xlabel('Time')
        self.axes[1, 0].set_ylabel('Confidence')
        
        self.axes[1, 1].set_title('Risk Assessment')
        self.axes[1, 1].set_xlabel('Time')
        self.axes[1, 1].set_ylabel('Risk Score')
        
        plt.tight_layout()
    
    def add_emotion_data(self, emotion: str, confidence: float, 
                        timestamp: datetime.datetime = None):
        """Add new emotion data point"""
        try:
            if timestamp is None:
                timestamp = datetime.datetime.now()
            
            self.emotion_data.append({
                'emotion': emotion,
                'confidence': confidence,
                'timestamp': timestamp
            })
            
            # Keep only last 100 data points for real-time plotting
            if len(self.emotion_data) > 100:
                self.emotion_data = self.emotion_data[-100:]
                
        except Exception as e:
            self.logger.error(f"Error adding emotion data: {e}")
    
    def add_session_data(self, session_data: Dict):
        """Add session data for analysis"""
        try:
            self.session_data.append(session_data)
        except Exception as e:
            self.logger.error(f"Error adding session data: {e}")
    
    def create_emotion_timeline(self, data: List[Dict] = None) -> go.Figure:
        """Create emotion timeline visualization"""
        try:
            if data is None:
                data = self.emotion_data
            
            if not data:
                return go.Figure()
            
            # Convert to DataFrame
            df = pd.DataFrame(data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Create scatter plot
            fig = go.Figure()
            
            for emotion in df['emotion'].unique():
                emotion_data = df[df['emotion'] == emotion]
                fig.add_trace(go.Scatter(
                    x=emotion_data['timestamp'],
                    y=emotion_data['confidence'],
                    mode='markers',
                    name=emotion,
                    marker=dict(
                        color=self.emotion_colors.get(emotion, '#808080'),
                        size=8,
                        opacity=0.7
                    ),
                    text=[f"Emotion: {emotion}<br>Confidence: {conf:.2f}" 
                          for conf in emotion_data['confidence']],
                    hovertemplate='%{text}<br>Time: %{x}<extra></extra>'
                ))
            
            fig.update_layout(
                title='Emotion Detection Timeline',
                xaxis_title='Time',
                yaxis_title='Confidence Level',
                hovermode='closest',
                showlegend=True
            )
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Error creating emotion timeline: {e}")
            return go.Figure()
    
    def create_emotion_distribution(self, data: List[Dict] = None) -> go.Figure:
        """Create emotion distribution pie chart"""
        try:
            if data is None:
                data = self.emotion_data
            
            if not data:
                return go.Figure()
            
            # Count emotions
            emotion_counts = {}
            for entry in data:
                emotion = entry['emotion']
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
            # Create pie chart
            fig = go.Figure(data=[go.Pie(
                labels=list(emotion_counts.keys()),
                values=list(emotion_counts.values()),
                marker_colors=[self.emotion_colors.get(emotion, '#808080') 
                              for emotion in emotion_counts.keys()],
                textinfo='label+percent',
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            )])
            
            fig.update_layout(
                title='Emotion Distribution',
                showlegend=True
            )
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Error creating emotion distribution: {e}")
            return go.Figure()
    
    def create_confidence_trend(self, data: List[Dict] = None) -> go.Figure:
        """Create confidence trend line chart"""
        try:
            if data is None:
                data = self.emotion_data
            
            if not data:
                return go.Figure()
            
            # Convert to DataFrame
            df = pd.DataFrame(data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            
            # Create line plot
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['confidence'],
                mode='lines+markers',
                name='Confidence',
                line=dict(color='#1f77b4', width=2),
                marker=dict(size=4),
                hovertemplate='Time: %{x}<br>Confidence: %{y:.2f}<extra></extra>'
            ))
            
            # Add average line
            avg_confidence = df['confidence'].mean()
            fig.add_hline(
                y=avg_confidence,
                line_dash="dash",
                line_color="red",
                annotation_text=f"Average: {avg_confidence:.2f}"
            )
            
            fig.update_layout(
                title='Confidence Trend Over Time',
                xaxis_title='Time',
                yaxis_title='Confidence Level',
                hovermode='x unified'
            )
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Error creating confidence trend: {e}")
            return go.Figure()
    
    def create_risk_assessment_chart(self, risk_data: List[Dict] = None) -> go.Figure:
        """Create risk assessment visualization"""
        try:
            if risk_data is None:
                # Extract risk data from session data
                risk_data = []
                for session in self.session_data:
                    if 'risk_score' in session:
                        risk_data.append({
                            'timestamp': session.get('timestamp', datetime.datetime.now()),
                            'risk_score': session['risk_score'],
                            'risk_level': session.get('risk_level', 0)
                        })
            
            if not risk_data:
                return go.Figure()
            
            # Convert to DataFrame
            df = pd.DataFrame(risk_data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            
            # Create area chart
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['risk_score'],
                mode='lines',
                fill='tonexty',
                name='Risk Score',
                line=dict(color='red', width=2),
                fillcolor='rgba(255, 0, 0, 0.3)',
                hovertemplate='Time: %{x}<br>Risk Score: %{y}<extra></extra>'
            ))
            
            # Add risk level zones
            fig.add_hline(y=7, line_dash="dash", line_color="orange", 
                         annotation_text="Crisis Threshold")
            fig.add_hline(y=4, line_dash="dash", line_color="yellow", 
                         annotation_text="High Risk")
            
            fig.update_layout(
                title='Risk Assessment Over Time',
                xaxis_title='Time',
                yaxis_title='Risk Score',
                hovermode='x unified'
            )
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Error creating risk assessment chart: {e}")
            return go.Figure()
    
    def create_comprehensive_dashboard(self) -> go.Figure:
        """Create comprehensive analytics dashboard"""
        try:
            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Emotion Timeline', 'Emotion Distribution', 
                              'Confidence Trend', 'Risk Assessment'),
                specs=[[{"secondary_y": False}, {"type": "pie"}],
                       [{"secondary_y": False}, {"secondary_y": False}]]
            )
            
            # Add emotion timeline
            if self.emotion_data:
                df = pd.DataFrame(self.emotion_data)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                
                for emotion in df['emotion'].unique():
                    emotion_data = df[df['emotion'] == emotion]
                    fig.add_trace(
                        go.Scatter(
                            x=emotion_data['timestamp'],
                            y=emotion_data['confidence'],
                            mode='markers',
                            name=emotion,
                            marker=dict(
                                color=self.emotion_colors.get(emotion, '#808080'),
                                size=6
                            )
                        ),
                        row=1, col=1
                    )
            
            # Add emotion distribution
            if self.emotion_data:
                emotion_counts = {}
                for entry in self.emotion_data:
                    emotion = entry['emotion']
                    emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
                
                fig.add_trace(
                    go.Pie(
                        labels=list(emotion_counts.keys()),
                        values=list(emotion_counts.values()),
                        marker_colors=[self.emotion_colors.get(emotion, '#808080') 
                                      for emotion in emotion_counts.keys()]
                    ),
                    row=1, col=2
                )
            
            # Add confidence trend
            if self.emotion_data:
                df = pd.DataFrame(self.emotion_data)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df = df.sort_values('timestamp')
                
                fig.add_trace(
                    go.Scatter(
                        x=df['timestamp'],
                        y=df['confidence'],
                        mode='lines+markers',
                        name='Confidence',
                        line=dict(color='blue', width=2)
                    ),
                    row=2, col=1
                )
            
            # Add risk assessment
            risk_data = []
            for session in self.session_data:
                if 'risk_score' in session:
                    risk_data.append({
                        'timestamp': session.get('timestamp', datetime.datetime.now()),
                        'risk_score': session['risk_score']
                    })
            
            if risk_data:
                df_risk = pd.DataFrame(risk_data)
                df_risk['timestamp'] = pd.to_datetime(df_risk['timestamp'])
                df_risk = df_risk.sort_values('timestamp')
                
                fig.add_trace(
                    go.Scatter(
                        x=df_risk['timestamp'],
                        y=df_risk['risk_score'],
                        mode='lines',
                        name='Risk Score',
                        line=dict(color='red', width=2)
                    ),
                    row=2, col=2
                )
            
            fig.update_layout(
                title='AI Therapy System - Comprehensive Analytics Dashboard',
                height=800,
                showlegend=True
            )
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Error creating comprehensive dashboard: {e}")
            return go.Figure()
    
    def create_session_summary_chart(self, session_id: str) -> go.Figure:
        """Create detailed session summary chart"""
        try:
            # Find session data
            session_data = None
            for session in self.session_data:
                if session.get('session_id') == session_id:
                    session_data = session
                    break
            
            if not session_data:
                return go.Figure()
            
            # Create subplots for session details
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Session Emotions', 'Conversation Flow', 
                              'Risk Progression', 'Intervention Timeline'),
                specs=[[{"type": "bar"}, {"secondary_y": False}],
                       [{"secondary_y": False}, {"secondary_y": False}]]
            )
            
            # Add session-specific visualizations
            if 'emotions' in session_data:
                emotion_counts = {}
                for emotion_entry in session_data['emotions']:
                    emotion = emotion_entry['emotion']
                    emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
                
                fig.add_trace(
                    go.Bar(
                        x=list(emotion_counts.keys()),
                        y=list(emotion_counts.values()),
                        name='Emotion Count',
                        marker_color=[self.emotion_colors.get(emotion, '#808080') 
                                     for emotion in emotion_counts.keys()]
                    ),
                    row=1, col=1
                )
            
            # Add conversation flow
            if 'conversations' in session_data:
                conversations = session_data['conversations']
                timestamps = [conv['timestamp'] for conv in conversations]
                sentiment_scores = [conv.get('sentiment_score', 0) for conv in conversations]
                
                fig.add_trace(
                    go.Scatter(
                        x=timestamps,
                        y=sentiment_scores,
                        mode='lines+markers',
                        name='Sentiment',
                        line=dict(color='green', width=2)
                    ),
                    row=1, col=2
                )
            
            fig.update_layout(
                title=f'Session Summary - {session_id}',
                height=800,
                showlegend=True
            )
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Error creating session summary chart: {e}")
            return go.Figure()
    
    def generate_statistics_report(self) -> Dict:
        """Generate comprehensive statistics report"""
        try:
            if not self.emotion_data:
                return {}
            
            # Basic statistics
            df = pd.DataFrame(self.emotion_data)
            
            # Emotion statistics
            emotion_stats = df['emotion'].value_counts().to_dict()
            avg_confidence = df['confidence'].mean()
            confidence_std = df['confidence'].std()
            
            # Time-based statistics
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['hour'] = df['timestamp'].dt.hour
            df['day'] = df['timestamp'].dt.date
            
            # Hourly distribution
            hourly_dist = df.groupby('hour')['emotion'].count().to_dict()
            
            # Daily distribution
            daily_dist = df.groupby('day')['emotion'].count().to_dict()
            
            # Risk statistics
            risk_stats = {}
            if self.session_data:
                risk_scores = [s.get('risk_score', 0) for s in self.session_data if 'risk_score' in s]
                if risk_scores:
                    risk_stats = {
                        'avg_risk_score': np.mean(risk_scores),
                        'max_risk_score': max(risk_scores),
                        'min_risk_score': min(risk_scores),
                        'high_risk_sessions': sum(1 for score in risk_scores if score >= 7)
                    }
            
            return {
                'total_data_points': len(self.emotion_data),
                'emotion_distribution': emotion_stats,
                'confidence_statistics': {
                    'average': avg_confidence,
                    'standard_deviation': confidence_std,
                    'min': df['confidence'].min(),
                    'max': df['confidence'].max()
                },
                'temporal_distribution': {
                    'hourly': hourly_dist,
                    'daily': daily_dist
                },
                'risk_statistics': risk_stats,
                'session_count': len(self.session_data),
                'data_collection_period': {
                    'start': df['timestamp'].min().isoformat() if len(df) > 0 else None,
                    'end': df['timestamp'].max().isoformat() if len(df) > 0 else None
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error generating statistics report: {e}")
            return {}
    
    def export_visualization_data(self) -> Dict:
        """Export data for external visualization tools"""
        try:
            return {
                'emotion_data': [
                    {
                        'emotion': entry['emotion'],
                        'confidence': entry['confidence'],
                        'timestamp': entry['timestamp'].isoformat()
                    }
                    for entry in self.emotion_data
                ],
                'session_data': self.session_data,
                'statistics': self.generate_statistics_report(),
                'export_timestamp': datetime.datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error exporting visualization data: {e}")
            return {}
    
    def start_real_time_visualization(self, update_callback: Optional[callable] = None):
        """Start real-time visualization updates"""
        try:
            self.is_real_time_active = True
            
            def update_loop():
                while self.is_real_time_active:
                    if update_callback:
                        update_callback()
                    time.sleep(self.update_interval)
            
            self.real_time_thread = threading.Thread(target=update_loop, daemon=True)
            self.real_time_thread.start()
            
            self.logger.info("Real-time visualization started")
            
        except Exception as e:
            self.logger.error(f"Error starting real-time visualization: {e}")
    
    def stop_real_time_visualization(self):
        """Stop real-time visualization updates"""
        try:
            self.is_real_time_active = False
            self.logger.info("Real-time visualization stopped")
        except Exception as e:
            self.logger.error(f"Error stopping real-time visualization: {e}")
    
    def clear_data(self):
        """Clear all visualization data"""
        try:
            self.emotion_data = []
            self.session_data = []
            self.logger.info("Visualization data cleared")
        except Exception as e:
            self.logger.error(f"Error clearing visualization data: {e}")
    
    def save_figure(self, fig: go.Figure, filename: str, format: str = 'html'):
        """Save figure to file"""
        try:
            if format.lower() == 'html':
                fig.write_html(filename)
            elif format.lower() == 'png':
                fig.write_image(filename)
            elif format.lower() == 'pdf':
                fig.write_image(filename)
            else:
                self.logger.warning(f"Unsupported format: {format}")
                return False
            
            self.logger.info(f"Figure saved to {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving figure: {e}")
            return False
