"""
Configuration Management
Centralized configuration for the AI Therapy System
"""

import json
import os
from pathlib import Path
from typing import Dict, Any
import logging

class ConfigManager:
    def __init__(self, config_file: str = "config/settings.json"):
        self.config_file = Path(config_file)
        self.logger = logging.getLogger(__name__)
        self.config = self._load_default_config()
        self._load_config()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration"""
        return {
            "system": {
                "name": "AI Therapy System",
                "version": "1.0.0",
                "debug_mode": False,
                "log_level": "INFO",
                "data_retention_days": 30
            },
            "camera": {
                "default_index": 0,
                "resolution": {
                    "width": 640,
                    "height": 480
                },
                "fps": 30,
                "auto_start": False
            },
            "emotion_detection": {
                "model_path": None,
                "confidence_threshold": 0.3,
                "update_interval": 0.1,
                "calibration_frames": 30,
                "emotion_labels": [
                    "Angry", "Disgust", "Fear", "Happy", 
                    "Sad", "Surprise", "Neutral"
                ]
            },
            "therapeutic_system": {
                "nurse_framework_enabled": True,
                "response_delay": 1.0,
                "max_conversation_length": 1000,
                "sentiment_analysis_enabled": True
            },
            "crisis_detection": {
                "enabled": True,
                "risk_threshold": 7,
                "monitoring_active": True,
                "auto_escalation": True,
                "crisis_keywords": [
                    "suicide", "kill myself", "end it all", 
                    "not worth living", "hurt myself", "self harm"
                ]
            },
            "database": {
                "path": "sessions.db",
                "backup_enabled": True,
                "backup_interval_hours": 24,
                "cleanup_enabled": True,
                "cleanup_interval_days": 7
            },
            "gui": {
                "theme": "light",
                "color_theme": "blue",
                "window_size": {
                    "width": 1400,
                    "height": 900
                },
                "min_window_size": {
                    "width": 1200,
                    "height": 800
                }
            },
            "export": {
                "default_directory": "exports",
                "default_format": "excel",
                "include_metadata": True,
                "anonymize_data": False
            },
            "safety": {
                "protocols_enabled": True,
                "emergency_contacts": [],
                "crisis_resources": {
                    "national_suicide_prevention": "988",
                    "crisis_text_line": "Text HOME to 741741",
                    "emergency_services": "911"
                },
                "auto_notification": False
            },
            "exercises": {
                "breathing_exercises_enabled": True,
                "mindfulness_exercises_enabled": True,
                "journaling_prompts_enabled": True,
                "relaxation_exercises_enabled": True,
                "mood_lifting_activities_enabled": True
            },
            "visualization": {
                "real_time_enabled": True,
                "update_interval": 1.0,
                "chart_types": ["timeline", "distribution", "trends"],
                "export_formats": ["png", "pdf", "html"]
            },
            "research": {
                "data_collection_enabled": True,
                "anonymize_participants": True,
                "export_frequency": "session_end",
                "statistical_analysis_enabled": True
            }
        }
    
    def _load_config(self):
        """Load configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    self._merge_config(loaded_config)
                self.logger.info(f"Configuration loaded from {self.config_file}")
            else:
                self._save_config()
                self.logger.info(f"Default configuration saved to {self.config_file}")
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
    
    def _merge_config(self, loaded_config: Dict[str, Any]):
        """Merge loaded configuration with default config"""
        def merge_dict(default: dict, loaded: dict):
            for key, value in loaded.items():
                if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                    merge_dict(default[key], value)
                else:
                    default[key] = value
        
        merge_dict(self.config, loaded_config)
    
    def _save_config(self):
        """Save configuration to file"""
        try:
            # Ensure config directory exists
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            
            self.logger.info(f"Configuration saved to {self.config_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving configuration: {e}")
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """Get configuration value using dot notation"""
        try:
            keys = key_path.split('.')
            value = self.config
            
            for key in keys:
                if isinstance(value, dict) and key in value:
                    value = value[key]
                else:
                    return default
            
            return value
            
        except Exception as e:
            self.logger.error(f"Error getting config value {key_path}: {e}")
            return default
    
    def set(self, key_path: str, value: Any):
        """Set configuration value using dot notation"""
        try:
            keys = key_path.split('.')
            config = self.config
            
            # Navigate to the parent of the target key
            for key in keys[:-1]:
                if key not in config:
                    config[key] = {}
                config = config[key]
            
            # Set the value
            config[keys[-1]] = value
            
            self.logger.info(f"Configuration updated: {key_path} = {value}")
            
        except Exception as e:
            self.logger.error(f"Error setting config value {key_path}: {e}")
    
    def save(self):
        """Save current configuration to file"""
        self._save_config()
    
    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        try:
            self.config = self._load_default_config()
            self._save_config()
            self.logger.info("Configuration reset to defaults")
            
        except Exception as e:
            self.logger.error(f"Error resetting configuration: {e}")
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """Get entire configuration section"""
        return self.get(section, {})
    
    def set_section(self, section: str, values: Dict[str, Any]):
        """Set entire configuration section"""
        try:
            self.config[section] = values
            self.logger.info(f"Configuration section updated: {section}")
            
        except Exception as e:
            self.logger.error(f"Error setting config section {section}: {e}")
    
    def export_config(self, filepath: str):
        """Export configuration to specified file"""
        try:
            export_path = Path(filepath)
            export_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(export_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            
            self.logger.info(f"Configuration exported to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Error exporting configuration: {e}")
    
    def import_config(self, filepath: str):
        """Import configuration from specified file"""
        try:
            import_path = Path(filepath)
            
            if not import_path.exists():
                raise FileNotFoundError(f"Configuration file not found: {filepath}")
            
            with open(import_path, 'r') as f:
                imported_config = json.load(f)
            
            self._merge_config(imported_config)
            self._save_config()
            
            self.logger.info(f"Configuration imported from {filepath}")
            
        except Exception as e:
            self.logger.error(f"Error importing configuration: {e}")
    
    def validate_config(self) -> Dict[str, Any]:
        """Validate configuration and return validation results"""
        validation_results = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        try:
            # Validate required sections
            required_sections = [
                'system', 'camera', 'emotion_detection', 'therapeutic_system',
                'crisis_detection', 'database', 'gui', 'export', 'safety'
            ]
            
            for section in required_sections:
                if section not in self.config:
                    validation_results['errors'].append(f"Missing required section: {section}")
                    validation_results['valid'] = False
            
            # Validate specific values
            if self.get('camera.default_index', 0) < 0:
                validation_results['warnings'].append("Camera index should be non-negative")
            
            if self.get('emotion_detection.confidence_threshold', 0.3) < 0 or self.get('emotion_detection.confidence_threshold', 0.3) > 1:
                validation_results['errors'].append("Confidence threshold must be between 0 and 1")
                validation_results['valid'] = False
            
            if self.get('crisis_detection.risk_threshold', 7) < 0 or self.get('crisis_detection.risk_threshold', 7) > 10:
                validation_results['errors'].append("Risk threshold must be between 0 and 10")
                validation_results['valid'] = False
            
            # Validate file paths
            db_path = self.get('database.path', 'sessions.db')
            if not isinstance(db_path, str):
                validation_results['errors'].append("Database path must be a string")
                validation_results['valid'] = False
            
            export_dir = self.get('export.default_directory', 'exports')
            if not isinstance(export_dir, str):
                validation_results['errors'].append("Export directory must be a string")
                validation_results['valid'] = False
            
        except Exception as e:
            validation_results['valid'] = False
            validation_results['errors'].append(f"Validation error: {e}")
            self.logger.error(f"Error validating configuration: {e}")
        
        return validation_results
    
    def get_all(self) -> Dict[str, Any]:
        """Get entire configuration"""
        return self.config.copy()
    
    def update_from_dict(self, updates: Dict[str, Any]):
        """Update configuration from dictionary"""
        try:
            self._merge_config(updates)
            self.logger.info("Configuration updated from dictionary")
            
        except Exception as e:
            self.logger.error(f"Error updating configuration from dictionary: {e}")

# Global configuration instance
config = ConfigManager()
