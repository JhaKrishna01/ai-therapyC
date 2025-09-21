"""
Database Management Module for AI Therapy System
Handles SQLite database operations for session logging and research data collection
"""

import sqlite3
import json
import datetime
from typing import Dict, List, Optional, Tuple
import logging

class DatabaseManager:
    def __init__(self, db_path: str = "sessions.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self.init_database()
    
    def init_database(self):
        """Initialize database with all required tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Sessions table - main session tracking
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS sessions (
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
                    )
                ''')
                
                # Emotion detection table - real-time emotion data
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS emotion_detections (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        emotion TEXT NOT NULL,
                        confidence REAL NOT NULL,
                        face_detected BOOLEAN DEFAULT TRUE,
                        frame_data TEXT,
                        FOREIGN KEY (session_id) REFERENCES sessions (session_id)
                    )
                ''')
                
                # Conversation table - chat interactions
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS conversations (
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
                    )
                ''')
                
                # Risk assessments table - safety monitoring
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS risk_assessments (
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
                    )
                ''')
                
                # Therapeutic interventions table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS interventions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        intervention_type TEXT NOT NULL,
                        intervention_data TEXT,
                        user_response TEXT,
                        effectiveness_score INTEGER,
                        duration_seconds INTEGER,
                        FOREIGN KEY (session_id) REFERENCES sessions (session_id)
                    )
                ''')
                
                # User feedback table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS user_feedback (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        feedback_type TEXT,
                        rating INTEGER,
                        comments TEXT,
                        improvement_suggestions TEXT,
                        FOREIGN KEY (session_id) REFERENCES sessions (session_id)
                    )
                ''')
                
                # System performance table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS system_performance (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        emotion_detection_accuracy REAL,
                        response_time_ms INTEGER,
                        system_load REAL,
                        error_count INTEGER DEFAULT 0,
                        FOREIGN KEY (session_id) REFERENCES sessions (session_id)
                    )
                ''')
                
                # Create indexes for better performance
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_emotion_session ON emotion_detections(session_id)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_emotion_timestamp ON emotion_detections(timestamp)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_conversation_session ON conversations(session_id)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_risk_session ON risk_assessments(session_id)')
                
                conn.commit()
                self.logger.info("Database initialized successfully")
                
        except sqlite3.Error as e:
            self.logger.error(f"Database initialization error: {e}")
            raise
    
    def create_session(self, session_id: str, user_id: str = "anonymous", 
                      session_type: str = "therapy") -> bool:
        """Create a new therapy session"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO sessions (session_id, user_id, session_type)
                    VALUES (?, ?, ?)
                ''', (session_id, user_id, session_type))
                conn.commit()
                self.logger.info(f"Session {session_id} created successfully")
                return True
        except sqlite3.Error as e:
            self.logger.error(f"Error creating session: {e}")
            return False
    
    def log_emotion_detection(self, session_id: str, emotion: str, 
                            confidence: float, face_detected: bool = True,
                            frame_data: Optional[Dict] = None) -> bool:
        """Log emotion detection data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                frame_json = json.dumps(frame_data) if frame_data else None
                cursor.execute('''
                    INSERT INTO emotion_detections 
                    (session_id, emotion, confidence, face_detected, frame_data)
                    VALUES (?, ?, ?, ?, ?)
                ''', (session_id, emotion, confidence, face_detected, frame_json))
                conn.commit()
                return True
        except sqlite3.Error as e:
            self.logger.error(f"Error logging emotion detection: {e}")
            return False
    
    def log_conversation(self, session_id: str, user_message: str, 
                        system_response: str, sentiment_score: float = 0.0,
                        emotion_context: str = "", therapeutic_approach: str = "",
                        response_effectiveness: int = 0) -> bool:
        """Log conversation interaction"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO conversations 
                    (session_id, user_message, system_response, sentiment_score,
                     emotion_context, therapeutic_approach, response_effectiveness)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (session_id, user_message, system_response, sentiment_score,
                      emotion_context, therapeutic_approach, response_effectiveness))
                conn.commit()
                return True
        except sqlite3.Error as e:
            self.logger.error(f"Error logging conversation: {e}")
            return False
    
    def log_risk_assessment(self, session_id: str, risk_score: int,
                           risk_factors: List[str], crisis_indicators: List[str],
                           intervention_taken: str = "", escalation_level: int = 0,
                           notes: str = "") -> bool:
        """Log risk assessment data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO risk_assessments 
                    (session_id, risk_score, risk_factors, crisis_indicators,
                     intervention_taken, escalation_level, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (session_id, risk_score, json.dumps(risk_factors),
                      json.dumps(crisis_indicators), intervention_taken,
                      escalation_level, notes))
                conn.commit()
                return True
        except sqlite3.Error as e:
            self.logger.error(f"Error logging risk assessment: {e}")
            return False
    
    def log_intervention(self, session_id: str, intervention_type: str,
                        intervention_data: Dict, user_response: str = "",
                        effectiveness_score: int = 0, duration_seconds: int = 0) -> bool:
        """Log therapeutic intervention"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO interventions 
                    (session_id, intervention_type, intervention_data,
                     user_response, effectiveness_score, duration_seconds)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (session_id, intervention_type, json.dumps(intervention_data),
                      user_response, effectiveness_score, duration_seconds))
                conn.commit()
                return True
        except sqlite3.Error as e:
            self.logger.error(f"Error logging intervention: {e}")
            return False
    
    def log_user_feedback(self, session_id: str, feedback_type: str,
                         rating: int, comments: str = "",
                         improvement_suggestions: str = "") -> bool:
        """Log user feedback"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO user_feedback 
                    (session_id, feedback_type, rating, comments, improvement_suggestions)
                    VALUES (?, ?, ?, ?, ?)
                ''', (session_id, feedback_type, rating, comments, improvement_suggestions))
                conn.commit()
                return True
        except sqlite3.Error as e:
            self.logger.error(f"Error logging user feedback: {e}")
            return False
    
    def log_system_performance(self, session_id: str, emotion_detection_accuracy: float,
                              response_time_ms: int, system_load: float,
                              error_count: int = 0) -> bool:
        """Log system performance metrics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO system_performance 
                    (session_id, emotion_detection_accuracy, response_time_ms,
                     system_load, error_count)
                    VALUES (?, ?, ?, ?, ?)
                ''', (session_id, emotion_detection_accuracy, response_time_ms,
                      system_load, error_count))
                conn.commit()
                return True
        except sqlite3.Error as e:
            self.logger.error(f"Error logging system performance: {e}")
            return False
    
    def end_session(self, session_id: str, session_outcome: str = "",
                   notes: str = "") -> bool:
        """End a therapy session"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE sessions 
                    SET end_time = CURRENT_TIMESTAMP, status = 'completed',
                        session_outcome = ?, notes = ?
                    WHERE session_id = ?
                ''', (session_outcome, notes, session_id))
                conn.commit()
                self.logger.info(f"Session {session_id} ended successfully")
                return True
        except sqlite3.Error as e:
            self.logger.error(f"Error ending session: {e}")
            return False
    
    def get_session_data(self, session_id: str) -> Dict:
        """Get complete session data for analysis"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                # Get session info
                cursor.execute('SELECT * FROM sessions WHERE session_id = ?', (session_id,))
                session = dict(cursor.fetchone()) if cursor.fetchone() else {}
                
                # Get emotion data
                cursor.execute('SELECT * FROM emotion_detections WHERE session_id = ? ORDER BY timestamp', (session_id,))
                emotions = [dict(row) for row in cursor.fetchall()]
                
                # Get conversation data
                cursor.execute('SELECT * FROM conversations WHERE session_id = ? ORDER BY timestamp', (session_id,))
                conversations = [dict(row) for row in cursor.fetchall()]
                
                # Get risk assessments
                cursor.execute('SELECT * FROM risk_assessments WHERE session_id = ? ORDER BY timestamp', (session_id,))
                risks = [dict(row) for row in cursor.fetchall()]
                
                # Get interventions
                cursor.execute('SELECT * FROM interventions WHERE session_id = ? ORDER BY timestamp', (session_id,))
                interventions = [dict(row) for row in cursor.fetchall()]
                
                return {
                    'session': session,
                    'emotions': emotions,
                    'conversations': conversations,
                    'risks': risks,
                    'interventions': interventions
                }
        except sqlite3.Error as e:
            self.logger.error(f"Error getting session data: {e}")
            return {}
    
    def get_all_sessions(self) -> List[Dict]:
        """Get all sessions for research analysis"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM sessions ORDER BY start_time DESC')
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            self.logger.error(f"Error getting all sessions: {e}")
            return []
    
    def export_session_data(self, session_id: str, format: str = 'json') -> str:
        """Export session data in specified format"""
        data = self.get_session_data(session_id)
        if format.lower() == 'json':
            return json.dumps(data, indent=2, default=str)
        elif format.lower() == 'csv':
            # Convert to CSV format (simplified)
            import pandas as pd
            df = pd.DataFrame(data['emotions'])
            return df.to_csv(index=False)
        return ""
    
    def get_emotion_statistics(self, session_id: str = None) -> Dict:
        """Get emotion detection statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if session_id:
                    cursor.execute('''
                        SELECT emotion, COUNT(*) as count, AVG(confidence) as avg_confidence
                        FROM emotion_detections 
                        WHERE session_id = ?
                        GROUP BY emotion
                    ''', (session_id,))
                else:
                    cursor.execute('''
                        SELECT emotion, COUNT(*) as count, AVG(confidence) as avg_confidence
                        FROM emotion_detections 
                        GROUP BY emotion
                    ''')
                
                results = cursor.fetchall()
                return {row[0]: {'count': row[1], 'avg_confidence': row[2]} for row in results}
        except sqlite3.Error as e:
            self.logger.error(f"Error getting emotion statistics: {e}")
            return {}
    
    def cleanup_old_data(self, days_old: int = 30):
        """Clean up old data to manage database size"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days_old)
                
                # Delete old emotion detections
                cursor.execute('DELETE FROM emotion_detections WHERE timestamp < ?', (cutoff_date,))
                
                # Delete old system performance logs
                cursor.execute('DELETE FROM system_performance WHERE timestamp < ?', (cutoff_date,))
                
                conn.commit()
                self.logger.info(f"Cleaned up data older than {days_old} days")
        except sqlite3.Error as e:
            self.logger.error(f"Error cleaning up old data: {e}")
