"""
Research Data Export System
Comprehensive data export functionality for research analysis
"""

import pandas as pd
import json
import csv
import logging
from typing import Dict, List, Optional, Any
import datetime
import os
import sqlite3
from pathlib import Path

class ResearchDataExporter:
    def __init__(self, export_directory: str = "exports"):
        self.logger = logging.getLogger(__name__)
        self.export_directory = Path(export_directory)
        self.export_directory.mkdir(exist_ok=True)
        
        # Export formats supported
        self.supported_formats = ['csv', 'json', 'excel', 'sqlite', 'xml']
        
        # Data categories for export
        self.data_categories = {
            'sessions': 'Session metadata and outcomes',
            'emotions': 'Emotion detection data with timestamps',
            'conversations': 'Chat interactions and responses',
            'risk_assessments': 'Risk assessment scores and factors',
            'interventions': 'Therapeutic interventions used',
            'exercises': 'Exercise completion and effectiveness',
            'feedback': 'User feedback and ratings',
            'performance': 'System performance metrics'
        }
    
    def export_session_data(self, session_id: str, format: str = 'json', 
                           include_all: bool = True) -> str:
        """Export data for a specific session"""
        try:
            # Get session data from database
            db_manager = self._get_database_manager()
            session_data = db_manager.get_session_data(session_id)
            
            if not session_data:
                self.logger.warning(f"No data found for session {session_id}")
                return ""
            
            # Generate filename
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"session_{session_id}_{timestamp}.{format}"
            filepath = self.export_directory / filename
            
            # Export based on format
            if format.lower() == 'json':
                self._export_to_json(session_data, filepath)
            elif format.lower() == 'csv':
                self._export_to_csv(session_data, filepath)
            elif format.lower() == 'excel':
                self._export_to_excel(session_data, filepath)
            elif format.lower() == 'xml':
                self._export_to_xml(session_data, filepath)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            self.logger.info(f"Session data exported to {filepath}")
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Error exporting session data: {e}")
            return ""
    
    def export_all_sessions(self, format: str = 'excel', 
                           date_range: Optional[Tuple[datetime.datetime, datetime.datetime]] = None) -> str:
        """Export data for all sessions"""
        try:
            # Get all sessions data
            db_manager = self._get_database_manager()
            all_sessions = db_manager.get_all_sessions()
            
            if not all_sessions:
                self.logger.warning("No sessions found for export")
                return ""
            
            # Filter by date range if provided
            if date_range:
                start_date, end_date = date_range
                filtered_sessions = []
                for session in all_sessions:
                    session_date = datetime.datetime.fromisoformat(session['start_time'])
                    if start_date <= session_date <= end_date:
                        filtered_sessions.append(session)
                all_sessions = filtered_sessions
            
            # Generate filename
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"all_sessions_{timestamp}.{format}"
            filepath = self.export_directory / filename
            
            # Export based on format
            if format.lower() == 'json':
                self._export_all_to_json(all_sessions, filepath)
            elif format.lower() == 'excel':
                self._export_all_to_excel(all_sessions, filepath)
            elif format.lower() == 'csv':
                self._export_all_to_csv(all_sessions, filepath)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            self.logger.info(f"All sessions data exported to {filepath}")
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Error exporting all sessions: {e}")
            return ""
    
    def export_emotion_analysis(self, format: str = 'csv', 
                               session_ids: Optional[List[str]] = None) -> str:
        """Export emotion analysis data"""
        try:
            db_manager = self._get_database_manager()
            
            # Get emotion data
            emotion_data = []
            if session_ids:
                for session_id in session_ids:
                    session_data = db_manager.get_session_data(session_id)
                    if session_data and 'emotions' in session_data:
                        emotion_data.extend(session_data['emotions'])
            else:
                # Get all emotion data
                with sqlite3.connect(db_manager.db_path) as conn:
                    conn.row_factory = sqlite3.Row
                    cursor = conn.cursor()
                    cursor.execute('SELECT * FROM emotion_detections ORDER BY timestamp')
                    emotion_data = [dict(row) for row in cursor.fetchall()]
            
            if not emotion_data:
                self.logger.warning("No emotion data found for export")
                return ""
            
            # Generate filename
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"emotion_analysis_{timestamp}.{format}"
            filepath = self.export_directory / filename
            
            # Convert to DataFrame for analysis
            df = pd.DataFrame(emotion_data)
            
            # Add analysis columns
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['hour'] = df['timestamp'].dt.hour
            df['day_of_week'] = df['timestamp'].dt.day_name()
            df['date'] = df['timestamp'].dt.date
            
            # Export based on format
            if format.lower() == 'csv':
                df.to_csv(filepath, index=False)
            elif format.lower() == 'excel':
                with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Raw Data', index=False)
                    
                    # Add summary sheets
                    emotion_summary = df.groupby('emotion').agg({
                        'confidence': ['count', 'mean', 'std', 'min', 'max']
                    }).round(3)
                    emotion_summary.to_excel(writer, sheet_name='Emotion Summary')
                    
                    hourly_dist = df.groupby(['hour', 'emotion']).size().unstack(fill_value=0)
                    hourly_dist.to_excel(writer, sheet_name='Hourly Distribution')
                    
                    daily_dist = df.groupby(['day_of_week', 'emotion']).size().unstack(fill_value=0)
                    daily_dist.to_excel(writer, sheet_name='Daily Distribution')
            
            self.logger.info(f"Emotion analysis exported to {filepath}")
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Error exporting emotion analysis: {e}")
            return ""
    
    def export_conversation_analysis(self, format: str = 'excel') -> str:
        """Export conversation analysis data"""
        try:
            db_manager = self._get_database_manager()
            
            # Get conversation data
            with sqlite3.connect(db_manager.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM conversations ORDER BY timestamp')
                conversations = [dict(row) for row in cursor.fetchall()]
            
            if not conversations:
                self.logger.warning("No conversation data found for export")
                return ""
            
            # Generate filename
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_analysis_{timestamp}.{format}"
            filepath = self.export_directory / filename
            
            # Convert to DataFrame
            df = pd.DataFrame(conversations)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Add analysis columns
            df['message_length'] = df['user_message'].str.len()
            df['response_length'] = df['system_response'].str.len()
            df['hour'] = df['timestamp'].dt.hour
            df['day_of_week'] = df['timestamp'].dt.day_name()
            
            # Export based on format
            if format.lower() == 'excel':
                with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Raw Conversations', index=False)
                    
                    # Therapeutic approach analysis
                    approach_analysis = df.groupby('therapeutic_approach').agg({
                        'sentiment_score': ['count', 'mean', 'std'],
                        'response_effectiveness': ['count', 'mean', 'std']
                    }).round(3)
                    approach_analysis.to_excel(writer, sheet_name='Therapeutic Approach Analysis')
                    
                    # Sentiment analysis
                    sentiment_analysis = df.groupby('emotion_context').agg({
                        'sentiment_score': ['count', 'mean', 'std'],
                        'response_effectiveness': ['count', 'mean', 'std']
                    }).round(3)
                    sentiment_analysis.to_excel(writer, sheet_name='Sentiment Analysis')
            
            self.logger.info(f"Conversation analysis exported to {filepath}")
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Error exporting conversation analysis: {e}")
            return ""
    
    def export_risk_assessment_data(self, format: str = 'excel') -> str:
        """Export risk assessment data"""
        try:
            db_manager = self._get_database_manager()
            
            # Get risk assessment data
            with sqlite3.connect(db_manager.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM risk_assessments ORDER BY timestamp')
                risk_data = [dict(row) for row in cursor.fetchall()]
            
            if not risk_data:
                self.logger.warning("No risk assessment data found for export")
                return ""
            
            # Generate filename
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"risk_assessment_{timestamp}.{format}"
            filepath = self.export_directory / filename
            
            # Convert to DataFrame
            df = pd.DataFrame(risk_data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Parse JSON fields
            df['risk_factors'] = df['risk_factors'].apply(lambda x: json.loads(x) if x else [])
            df['crisis_indicators'] = df['crisis_indicators'].apply(lambda x: json.loads(x) if x else [])
            
            # Export based on format
            if format.lower() == 'excel':
                with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Risk Assessments', index=False)
                    
                    # Risk level analysis
                    risk_analysis = df.groupby('escalation_level').agg({
                        'risk_score': ['count', 'mean', 'std', 'min', 'max']
                    }).round(3)
                    risk_analysis.to_excel(writer, sheet_name='Risk Level Analysis')
                    
                    # Intervention analysis
                    intervention_analysis = df.groupby('intervention_taken').size().sort_values(ascending=False)
                    intervention_analysis.to_excel(writer, sheet_name='Intervention Analysis')
            
            self.logger.info(f"Risk assessment data exported to {filepath}")
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Error exporting risk assessment data: {e}")
            return ""
    
    def export_research_report(self, format: str = 'excel') -> str:
        """Export comprehensive research report"""
        try:
            # Generate filename
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"research_report_{timestamp}.{format}"
            filepath = self.export_directory / filename
            
            db_manager = self._get_database_manager()
            
            if format.lower() == 'excel':
                with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                    # Session summary
                    sessions = db_manager.get_all_sessions()
                    if sessions:
                        sessions_df = pd.DataFrame(sessions)
                        sessions_df.to_excel(writer, sheet_name='Sessions', index=False)
                    
                    # Emotion statistics
                    emotion_stats = db_manager.get_emotion_statistics()
                    if emotion_stats:
                        emotion_df = pd.DataFrame([
                            {'emotion': emotion, 'count': data['count'], 
                             'avg_confidence': data['avg_confidence']}
                            for emotion, data in emotion_stats.items()
                        ])
                        emotion_df.to_excel(writer, sheet_name='Emotion Statistics', index=False)
                    
                    # System performance summary
                    with sqlite3.connect(db_manager.db_path) as conn:
                        cursor = conn.cursor()
                        cursor.execute('''
                            SELECT AVG(emotion_detection_accuracy) as avg_accuracy,
                                   AVG(response_time_ms) as avg_response_time,
                                   SUM(error_count) as total_errors
                            FROM system_performance
                        ''')
                        perf_data = cursor.fetchone()
                        if perf_data:
                            perf_df = pd.DataFrame([{
                                'avg_accuracy': perf_data[0],
                                'avg_response_time': perf_data[1],
                                'total_errors': perf_data[2]
                            }])
                            perf_df.to_excel(writer, sheet_name='System Performance', index=False)
            
            self.logger.info(f"Research report exported to {filepath}")
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Error exporting research report: {e}")
            return ""
    
    def _export_to_json(self, data: Dict, filepath: Path):
        """Export data to JSON format"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str, ensure_ascii=False)
    
    def _export_to_csv(self, data: Dict, filepath: Path):
        """Export data to CSV format"""
        # Export each table as separate CSV
        for table_name, table_data in data.items():
            if isinstance(table_data, list) and table_data:
                csv_filename = filepath.with_suffix(f'_{table_name}.csv')
                df = pd.DataFrame(table_data)
                df.to_csv(csv_filename, index=False)
    
    def _export_to_excel(self, data: Dict, filepath: Path):
        """Export data to Excel format"""
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            for sheet_name, sheet_data in data.items():
                if isinstance(sheet_data, list) and sheet_data:
                    df = pd.DataFrame(sheet_data)
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                elif isinstance(sheet_data, dict):
                    df = pd.DataFrame([sheet_data])
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    def _export_to_xml(self, data: Dict, filepath: Path):
        """Export data to XML format"""
        def dict_to_xml(data_dict, root_name='root'):
            xml = f'<{root_name}>\n'
            for key, value in data_dict.items():
                if isinstance(value, dict):
                    xml += dict_to_xml(value, key)
                elif isinstance(value, list):
                    xml += f'<{key}>\n'
                    for item in value:
                        if isinstance(item, dict):
                            xml += dict_to_xml(item, 'item')
                        else:
                            xml += f'<item>{item}</item>\n'
                    xml += f'</{key}>\n'
                else:
                    xml += f'<{key}>{value}</{key}>\n'
            xml += f'</{root_name}>\n'
            return xml
        
        xml_content = dict_to_xml(data, 'therapy_data')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(xml_content)
    
    def _export_all_to_json(self, sessions: List[Dict], filepath: Path):
        """Export all sessions to JSON"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(sessions, f, indent=2, default=str, ensure_ascii=False)
    
    def _export_all_to_excel(self, sessions: List[Dict], filepath: Path):
        """Export all sessions to Excel"""
        df = pd.DataFrame(sessions)
        df.to_excel(filepath, index=False)
    
    def _export_all_to_csv(self, sessions: List[Dict], filepath: Path):
        """Export all sessions to CSV"""
        df = pd.DataFrame(sessions)
        df.to_csv(filepath, index=False)
    
    def _get_database_manager(self):
        """Get database manager instance"""
        # Import here to avoid circular imports
        from database.database_manager import DatabaseManager
        return DatabaseManager()
    
    def create_export_summary(self) -> Dict:
        """Create summary of all available exports"""
        try:
            export_files = list(self.export_directory.glob('*'))
            
            summary = {
                'export_directory': str(self.export_directory),
                'total_files': len(export_files),
                'file_types': {},
                'recent_exports': [],
                'available_formats': self.supported_formats,
                'data_categories': self.data_categories
            }
            
            # Analyze file types
            for file_path in export_files:
                file_ext = file_path.suffix.lower()
                summary['file_types'][file_ext] = summary['file_types'].get(file_ext, 0) + 1
                
                # Get file info
                stat = file_path.stat()
                summary['recent_exports'].append({
                    'filename': file_path.name,
                    'size': stat.st_size,
                    'created': datetime.datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    'modified': datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
            
            # Sort by creation time
            summary['recent_exports'].sort(key=lambda x: x['created'], reverse=True)
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Error creating export summary: {e}")
            return {}
    
    def cleanup_old_exports(self, days_old: int = 30):
        """Clean up old export files"""
        try:
            cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days_old)
            deleted_count = 0
            
            for file_path in self.export_directory.glob('*'):
                if file_path.is_file():
                    file_time = datetime.datetime.fromtimestamp(file_path.stat().st_ctime)
                    if file_time < cutoff_date:
                        file_path.unlink()
                        deleted_count += 1
            
            self.logger.info(f"Cleaned up {deleted_count} old export files")
            return deleted_count
            
        except Exception as e:
            self.logger.error(f"Error cleaning up old exports: {e}")
            return 0
