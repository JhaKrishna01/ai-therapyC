"""
Safety Features and Crisis Intervention Protocols
Implements comprehensive safety measures and helpline integration
"""

import logging
import webbrowser
import subprocess
import platform
from typing import Dict, List, Optional
import datetime
import json
import threading
import time

class SafetyManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.crisis_active = False
        self.emergency_contacts = []
        self.safety_protocols_active = True
        
        # Crisis intervention resources
        self.crisis_resources = {
            'national_suicide_prevention': {
                'name': 'National Suicide Prevention Lifeline',
                'phone': '988',
                'text': 'Text HOME to 741741',
                'website': 'https://suicidepreventionlifeline.org',
                'description': '24/7 crisis support for suicide prevention'
            },
            'crisis_text_line': {
                'name': 'Crisis Text Line',
                'phone': 'Text HOME to 741741',
                'website': 'https://www.crisistextline.org',
                'description': '24/7 crisis support via text message'
            },
            'emergency_services': {
                'name': 'Emergency Services',
                'phone': '911',
                'description': 'For immediate life-threatening emergencies'
            },
            'mental_health_america': {
                'name': 'Mental Health America',
                'phone': '1-800-273-8255',
                'website': 'https://www.mhanational.org',
                'description': 'Mental health resources and support'
            },
            'substance_abuse_helpline': {
                'name': 'SAMHSA National Helpline',
                'phone': '1-800-662-4357',
                'website': 'https://www.samhsa.gov/find-help/national-helpline',
                'description': 'Substance abuse and mental health services'
            },
            'domestic_violence_hotline': {
                'name': 'National Domestic Violence Hotline',
                'phone': '1-800-799-7233',
                'website': 'https://www.thehotline.org',
                'description': 'Support for domestic violence situations'
            },
            'lgbtq_crisis': {
                'name': 'The Trevor Project',
                'phone': '1-866-488-7386',
                'text': 'Text START to 678678',
                'website': 'https://www.thetrevorproject.org',
                'description': 'Crisis support for LGBTQ+ youth'
            },
            'veterans_crisis': {
                'name': 'Veterans Crisis Line',
                'phone': '1-800-273-8255',
                'text': 'Text 838255',
                'website': 'https://www.veteranscrisisline.net',
                'description': 'Crisis support for veterans'
            }
        }
        
        # Safety protocols
        self.safety_protocols = {
            'crisis_detection': self._crisis_detection_protocol,
            'immediate_intervention': self._immediate_intervention_protocol,
            'emergency_response': self._emergency_response_protocol,
            'follow_up_care': self._follow_up_care_protocol
        }
        
        # User safety preferences
        self.user_safety_preferences = {
            'emergency_contact': None,
            'preferred_crisis_resource': 'national_suicide_prevention',
            'auto_escalation_enabled': True,
            'location_sharing_enabled': False,
            'notification_preferences': {
                'email_alerts': False,
                'sms_alerts': False,
                'push_notifications': True
            }
        }
    
    def activate_crisis_protocol(self, risk_level: int, crisis_data: Dict) -> Dict:
        """Activate appropriate crisis protocol based on risk level"""
        try:
            if not self.safety_protocols_active:
                return {'status': 'disabled', 'message': 'Safety protocols are disabled'}
            
            self.crisis_active = True
            
            if risk_level >= 5:  # Emergency
                return self.safety_protocols['emergency_response'](crisis_data)
            elif risk_level >= 4:  # Crisis
                return self.safety_protocols['immediate_intervention'](crisis_data)
            elif risk_level >= 2:  # Moderate to High Risk
                return self.safety_protocols['crisis_detection'](crisis_data)
            else:
                return self.safety_protocols['follow_up_care'](crisis_data)
                
        except Exception as e:
            self.logger.error(f"Error activating crisis protocol: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _crisis_detection_protocol(self, crisis_data: Dict) -> Dict:
        """Crisis detection and early intervention protocol"""
        try:
            intervention = {
                'protocol_type': 'crisis_detection',
                'priority': 'high',
                'actions_taken': [
                    'Crisis indicators detected',
                    'User safety assessment initiated',
                    'Crisis resources provided',
                    'Monitoring increased'
                ],
                'immediate_responses': [
                    'Express concern for user safety',
                    'Provide crisis resources',
                    'Encourage professional help',
                    'Create safety plan'
                ],
                'resources_provided': self._get_crisis_resources(),
                'follow_up_required': True,
                'monitoring_level': 'increased',
                'timestamp': datetime.datetime.now().isoformat()
            }
            
            # Log crisis detection
            self._log_crisis_event('crisis_detection', crisis_data, intervention)
            
            return intervention
            
        except Exception as e:
            self.logger.error(f"Error in crisis detection protocol: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _immediate_intervention_protocol(self, crisis_data: Dict) -> Dict:
        """Immediate crisis intervention protocol"""
        try:
            intervention = {
                'protocol_type': 'immediate_intervention',
                'priority': 'critical',
                'actions_taken': [
                    'Crisis intervention activated',
                    'Safety plan created',
                    'Crisis resources provided',
                    'Emergency contacts notified',
                    'Professional help encouraged'
                ],
                'immediate_responses': [
                    'Direct safety assessment',
                    'Crisis hotline information provided',
                    'Safety plan implementation',
                    'Emergency contact notification',
                    'Professional referral'
                ],
                'resources_provided': self._get_crisis_resources(),
                'emergency_contacts': self._get_emergency_contacts(),
                'follow_up_required': True,
                'monitoring_level': 'critical',
                'escalation_threshold': 'immediate',
                'timestamp': datetime.datetime.now().isoformat()
            }
            
            # Attempt to open crisis resources
            self._open_crisis_resources()
            
            # Log crisis intervention
            self._log_crisis_event('immediate_intervention', crisis_data, intervention)
            
            return intervention
            
        except Exception as e:
            self.logger.error(f"Error in immediate intervention protocol: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _emergency_response_protocol(self, crisis_data: Dict) -> Dict:
        """Emergency response protocol"""
        try:
            intervention = {
                'protocol_type': 'emergency_response',
                'priority': 'emergency',
                'actions_taken': [
                    'Emergency protocol activated',
                    'Emergency services contacted',
                    'Crisis resources provided',
                    'Emergency contacts notified',
                    'Safety measures implemented'
                ],
                'immediate_responses': [
                    'Call 911 immediately',
                    'Stay with the person',
                    'Remove means of self-harm',
                    'Provide crisis resources',
                    'Contact emergency contacts'
                ],
                'emergency_services': {
                    'phone': '911',
                    'description': 'Call immediately for life-threatening emergency'
                },
                'resources_provided': self._get_crisis_resources(),
                'emergency_contacts': self._get_emergency_contacts(),
                'follow_up_required': True,
                'monitoring_level': 'emergency',
                'escalation_threshold': 'immediate',
                'timestamp': datetime.datetime.now().isoformat()
            }
            
            # Attempt to call emergency services
            self._call_emergency_services()
            
            # Open crisis resources
            self._open_crisis_resources()
            
            # Log emergency response
            self._log_crisis_event('emergency_response', crisis_data, intervention)
            
            return intervention
            
        except Exception as e:
            self.logger.error(f"Error in emergency response protocol: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _follow_up_care_protocol(self, crisis_data: Dict) -> Dict:
        """Follow-up care protocol"""
        try:
            intervention = {
                'protocol_type': 'follow_up_care',
                'priority': 'moderate',
                'actions_taken': [
                    'Follow-up care initiated',
                    'Resources provided',
                    'Monitoring scheduled',
                    'Support plan created'
                ],
                'immediate_responses': [
                    'Provide supportive resources',
                    'Schedule follow-up check',
                    'Create support plan',
                    'Encourage professional help'
                ],
                'resources_provided': self._get_support_resources(),
                'follow_up_required': True,
                'monitoring_level': 'standard',
                'follow_up_schedule': '24_hours',
                'timestamp': datetime.datetime.now().isoformat()
            }
            
            # Log follow-up care
            self._log_crisis_event('follow_up_care', crisis_data, intervention)
            
            return intervention
            
        except Exception as e:
            self.logger.error(f"Error in follow-up care protocol: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _get_crisis_resources(self) -> List[Dict]:
        """Get crisis intervention resources"""
        return [
            self.crisis_resources['national_suicide_prevention'],
            self.crisis_resources['crisis_text_line'],
            self.crisis_resources['emergency_services']
        ]
    
    def _get_support_resources(self) -> List[Dict]:
        """Get general support resources"""
        return [
            self.crisis_resources['mental_health_america'],
            self.crisis_resources['substance_abuse_helpline']
        ]
    
    def _get_emergency_contacts(self) -> List[Dict]:
        """Get emergency contacts for the user"""
        return self.emergency_contacts
    
    def _open_crisis_resources(self):
        """Open crisis resources in browser"""
        try:
            # Open National Suicide Prevention Lifeline
            webbrowser.open(self.crisis_resources['national_suicide_prevention']['website'])
            
            # Open Crisis Text Line
            webbrowser.open(self.crisis_resources['crisis_text_line']['website'])
            
        except Exception as e:
            self.logger.error(f"Error opening crisis resources: {e}")
    
    def _call_emergency_services(self):
        """Attempt to call emergency services"""
        try:
            system = platform.system()
            
            if system == "Windows":
                # Windows - open phone dialer
                subprocess.run(['start', 'tel:911'], shell=True)
            elif system == "Darwin":  # macOS
                # macOS - open phone dialer
                subprocess.run(['open', 'tel:911'])
            elif system == "Linux":
                # Linux - try to open phone dialer
                subprocess.run(['xdg-open', 'tel:911'])
            
            self.logger.info("Emergency services dialer opened")
            
        except Exception as e:
            self.logger.error(f"Error calling emergency services: {e}")
    
    def _log_crisis_event(self, event_type: str, crisis_data: Dict, intervention: Dict):
        """Log crisis event for research and safety purposes"""
        try:
            crisis_log = {
                'event_type': event_type,
                'timestamp': datetime.datetime.now().isoformat(),
                'crisis_data': crisis_data,
                'intervention': intervention,
                'user_id': crisis_data.get('user_id', 'anonymous'),
                'session_id': crisis_data.get('session_id', 'unknown')
            }
            
            # Log to file
            log_filename = f"logs/crisis_events_{datetime.datetime.now().strftime('%Y%m%d')}.json"
            with open(log_filename, 'a') as f:
                f.write(json.dumps(crisis_log) + '\n')
            
            self.logger.critical(f"Crisis event logged: {event_type}")
            
        except Exception as e:
            self.logger.error(f"Error logging crisis event: {e}")
    
    def create_safety_plan(self, user_preferences: Dict = None) -> Dict:
        """Create personalized safety plan"""
        try:
            safety_plan = {
                'warning_signs': [
                    'Feeling hopeless or worthless',
                    'Thoughts of self-harm or suicide',
                    'Increased isolation',
                    'Substance use increase',
                    'Sleep or appetite changes',
                    'Loss of interest in activities',
                    'Mood swings or irritability',
                    'Feeling like a burden to others'
                ],
                'coping_strategies': [
                    'Deep breathing exercises',
                    'Calling a trusted friend or family member',
                    'Going for a walk in nature',
                    'Listening to calming music',
                    'Practicing mindfulness or meditation',
                    'Engaging in creative activities',
                    'Exercising or physical activity',
                    'Using the AI therapy system'
                ],
                'social_supports': [
                    'Family members',
                    'Close friends',
                    'Mental health professional',
                    'Support group members',
                    'Crisis hotline',
                    'Online support communities'
                ],
                'professional_resources': [
                    'Therapist or counselor',
                    'Psychiatrist',
                    'Primary care doctor',
                    'Crisis intervention team',
                    'Emergency services',
                    'Mental health clinic'
                ],
                'environmental_safety': [
                    'Remove or secure means of self-harm',
                    'Stay in a safe environment',
                    'Avoid alcohol and drugs',
                    'Ensure someone knows your location',
                    'Have emergency contacts readily available',
                    'Keep crisis hotline numbers accessible'
                ],
                'crisis_contacts': [
                    {'name': 'National Suicide Prevention Lifeline', 'number': '988'},
                    {'name': 'Crisis Text Line', 'number': 'Text HOME to 741741'},
                    {'name': 'Emergency Services', 'number': '911'}
                ],
                'follow_up_plan': [
                    'Schedule regular check-ins with therapist',
                    'Attend support group meetings',
                    'Use AI therapy system daily',
                    'Practice coping strategies regularly',
                    'Monitor warning signs',
                    'Update safety plan as needed'
                ]
            }
            
            # Customize based on user preferences
            if user_preferences:
                for key, value in user_preferences.items():
                    if key in safety_plan and isinstance(value, list):
                        safety_plan[key] = value
            
            return safety_plan
            
        except Exception as e:
            self.logger.error(f"Error creating safety plan: {e}")
            return {}
    
    def add_emergency_contact(self, contact: Dict):
        """Add emergency contact"""
        try:
            required_fields = ['name', 'phone', 'relationship']
            if all(field in contact for field in required_fields):
                self.emergency_contacts.append(contact)
                self.logger.info(f"Emergency contact added: {contact['name']}")
            else:
                raise ValueError("Missing required fields for emergency contact")
                
        except Exception as e:
            self.logger.error(f"Error adding emergency contact: {e}")
    
    def remove_emergency_contact(self, contact_name: str):
        """Remove emergency contact"""
        try:
            self.emergency_contacts = [
                contact for contact in self.emergency_contacts 
                if contact['name'] != contact_name
            ]
            self.logger.info(f"Emergency contact removed: {contact_name}")
            
        except Exception as e:
            self.logger.error(f"Error removing emergency contact: {e}")
    
    def update_safety_preferences(self, preferences: Dict):
        """Update user safety preferences"""
        try:
            self.user_safety_preferences.update(preferences)
            self.logger.info("Safety preferences updated")
            
        except Exception as e:
            self.logger.error(f"Error updating safety preferences: {e}")
    
    def get_safety_status(self) -> Dict:
        """Get current safety status"""
        return {
            'crisis_active': self.crisis_active,
            'safety_protocols_active': self.safety_protocols_active,
            'emergency_contacts_count': len(self.emergency_contacts),
            'preferred_crisis_resource': self.user_safety_preferences['preferred_crisis_resource'],
            'auto_escalation_enabled': self.user_safety_preferences['auto_escalation_enabled']
        }
    
    def deactivate_crisis(self):
        """Deactivate crisis mode"""
        try:
            self.crisis_active = False
            self.logger.info("Crisis mode deactivated")
            
        except Exception as e:
            self.logger.error(f"Error deactivating crisis: {e}")
    
    def disable_safety_protocols(self):
        """Disable safety protocols (for testing only)"""
        try:
            self.safety_protocols_active = False
            self.logger.warning("Safety protocols disabled")
            
        except Exception as e:
            self.logger.error(f"Error disabling safety protocols: {e}")
    
    def enable_safety_protocols(self):
        """Enable safety protocols"""
        try:
            self.safety_protocols_active = True
            self.logger.info("Safety protocols enabled")
            
        except Exception as e:
            self.logger.error(f"Error enabling safety protocols: {e}")
    
    def export_safety_data(self) -> Dict:
        """Export safety data for research"""
        return {
            'crisis_resources': self.crisis_resources,
            'safety_protocols': list(self.safety_protocols.keys()),
            'user_safety_preferences': self.user_safety_preferences,
            'emergency_contacts': self.emergency_contacts,
            'safety_status': self.get_safety_status(),
            'export_timestamp': datetime.datetime.now().isoformat()
        }
