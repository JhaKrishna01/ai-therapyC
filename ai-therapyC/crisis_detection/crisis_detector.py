"""
Crisis Detection and Safety Guardrails System
Monitors for crisis indicators and implements safety protocols
"""

import re
import logging
import datetime
from typing import Dict, List, Optional, Tuple
import json
import threading
import time

class CrisisDetector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.crisis_threshold = 7
        self.escalation_levels = {
            0: "Low Risk",
            1: "Mild Concern", 
            2: "Moderate Risk",
            3: "High Risk",
            4: "Crisis Level",
            5: "Emergency"
        }
        
        # Crisis indicators
        self.crisis_indicators = {
            'suicidal_ideation': {
                'keywords': [
                    'suicide', 'kill myself', 'end it all', 'not worth living',
                    'better off dead', 'want to die', 'end my life',
                    'suicidal', 'self harm', 'hurt myself'
                ],
                'weight': 5,
                'patterns': [
                    r'i want to (die|kill myself|end it all)',
                    r'i should (die|kill myself)',
                    r'i wish i was (dead|gone)',
                    r'nothing matters anymore',
                    r'i have no reason to live'
                ]
            },
            'self_harm': {
                'keywords': [
                    'cut myself', 'hurt myself', 'self harm', 'burn myself',
                    'hit myself', 'punish myself', 'hurt my body'
                ],
                'weight': 4,
                'patterns': [
                    r'i want to (cut|hurt|burn) myself',
                    r'i deserve to be (hurt|punished)',
                    r'i should (cut|hurt) myself'
                ]
            },
            'hopelessness': {
                'keywords': [
                    'hopeless', 'worthless', 'useless', 'burden',
                    'no point', 'nothing will help', 'can\'t go on',
                    'give up', 'no future'
                ],
                'weight': 3,
                'patterns': [
                    r'there\'s no (point|hope|future)',
                    r'i\'m (worthless|useless|a burden)',
                    r'nothing will (help|change|get better)',
                    r'i (can\'t|can not) go on'
                ]
            },
            'isolation': {
                'keywords': [
                    'alone', 'nobody cares', 'no one understands',
                    'isolated', 'lonely', 'abandoned', 'rejected'
                ],
                'weight': 2,
                'patterns': [
                    r'nobody (cares|understands|loves) me',
                    r'i\'m (alone|isolated|abandoned)',
                    r'no one (cares|understands)'
                ]
            },
            'substance_abuse': {
                'keywords': [
                    'drink', 'drugs', 'overdose', 'too much',
                    'can\'t stop', 'addicted', 'need it'
                ],
                'weight': 3,
                'patterns': [
                    r'i need to (drink|use|take)',
                    r'i can\'t stop (drinking|using)',
                    r'i want to (overdose|take too much)'
                ]
            },
            'trauma': {
                'keywords': [
                    'flashback', 'nightmare', 'trauma', 'ptsd',
                    'triggered', 'reliving', 'can\'t forget'
                ],
                'weight': 3,
                'patterns': [
                    r'i keep (reliving|remembering)',
                    r'i can\'t (forget|stop thinking about)',
                    r'i\'m (triggered|having flashbacks)'
                ]
            }
        }
        
        # Safety protocols
        self.safety_protocols = {
            4: self._crisis_protocol,
            5: self._emergency_protocol
        }
        
        # Crisis resources
        self.crisis_resources = {
            'national_suicide_prevention': {
                'name': 'National Suicide Prevention Lifeline',
                'number': '988',
                'text': 'Text HOME to 741741',
                'website': 'https://suicidepreventionlifeline.org'
            },
            'crisis_text_line': {
                'name': 'Crisis Text Line',
                'number': 'Text HOME to 741741',
                'website': 'https://www.crisistextline.org'
            },
            'emergency_services': {
                'name': 'Emergency Services',
                'number': '911',
                'description': 'For immediate life-threatening emergencies'
            },
            'mental_health_america': {
                'name': 'Mental Health America',
                'number': '1-800-273-8255',
                'website': 'https://www.mhanational.org'
            }
        }
        
        # Monitoring state
        self.current_risk_level = 0
        self.risk_history = []
        self.intervention_log = []
        self.is_monitoring = False
    
    def analyze_text(self, text: str) -> Dict:
        """Analyze text for crisis indicators"""
        try:
            risk_score = 0
            detected_indicators = []
            confidence_scores = {}
            
            text_lower = text.lower()
            
            # Check each crisis indicator category
            for category, data in self.crisis_indicators.items():
                category_score = 0
                category_indicators = []
                
                # Check keywords
                for keyword in data['keywords']:
                    if keyword in text_lower:
                        category_score += data['weight']
                        category_indicators.append(f"Keyword: {keyword}")
                
                # Check patterns
                for pattern in data['patterns']:
                    matches = re.findall(pattern, text_lower)
                    if matches:
                        category_score += data['weight'] * len(matches)
                        category_indicators.append(f"Pattern: {pattern}")
                
                if category_score > 0:
                    detected_indicators.append({
                        'category': category,
                        'score': category_score,
                        'indicators': category_indicators
                    })
                    risk_score += category_score
                    confidence_scores[category] = min(category_score / (data['weight'] * 3), 1.0)
            
            # Determine risk level
            risk_level = self._calculate_risk_level(risk_score)
            
            # Check for escalation
            escalation_needed = self._check_escalation(risk_level)
            
            return {
                'risk_score': min(risk_score, 20),  # Cap at 20
                'risk_level': risk_level,
                'risk_level_name': self.escalation_levels[risk_level],
                'detected_indicators': detected_indicators,
                'confidence_scores': confidence_scores,
                'escalation_needed': escalation_needed,
                'timestamp': datetime.datetime.now()
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing text for crisis indicators: {e}")
            return {
                'risk_score': 0,
                'risk_level': 0,
                'risk_level_name': 'Low Risk',
                'detected_indicators': [],
                'confidence_scores': {},
                'escalation_needed': False,
                'timestamp': datetime.datetime.now()
            }
    
    def analyze_emotion_pattern(self, emotion_history: List[Dict]) -> Dict:
        """Analyze emotion patterns for crisis indicators"""
        try:
            if len(emotion_history) < 5:
                return {'risk_score': 0, 'patterns': []}
            
            risk_score = 0
            patterns = []
            
            # Check for sustained negative emotions
            recent_emotions = emotion_history[-10:]  # Last 10 emotions
            negative_emotions = ['Sad', 'Angry', 'Fear']
            
            negative_count = sum(1 for e in recent_emotions if e['emotion'] in negative_emotions)
            if negative_count >= 8:  # 80% negative emotions
                risk_score += 3
                patterns.append("Sustained negative emotional state")
            
            # Check for emotional volatility
            emotion_changes = 0
            for i in range(1, len(recent_emotions)):
                if recent_emotions[i]['emotion'] != recent_emotions[i-1]['emotion']:
                    emotion_changes += 1
            
            if emotion_changes >= 7:  # High volatility
                risk_score += 2
                patterns.append("High emotional volatility")
            
            # Check for increasing distress
            if len(emotion_history) >= 20:
                early_emotions = emotion_history[-20:-10]
                late_emotions = emotion_history[-10:]
                
                early_negative = sum(1 for e in early_emotions if e['emotion'] in negative_emotions)
                late_negative = sum(1 for e in late_emotions if e['emotion'] in negative_emotions)
                
                if late_negative > early_negative + 3:  # Significant increase
                    risk_score += 2
                    patterns.append("Increasing emotional distress")
            
            # Check for low confidence in emotion detection (possible masking)
            low_confidence_count = sum(1 for e in recent_emotions if e['confidence'] < 0.3)
            if low_confidence_count >= 5:
                risk_score += 1
                patterns.append("Possible emotional masking")
            
            return {
                'risk_score': risk_score,
                'patterns': patterns,
                'analysis': {
                    'negative_emotion_ratio': negative_count / len(recent_emotions),
                    'emotional_volatility': emotion_changes / len(recent_emotions),
                    'confidence_trend': sum(e['confidence'] for e in recent_emotions) / len(recent_emotions)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing emotion patterns: {e}")
            return {'risk_score': 0, 'patterns': []}
    
    def _calculate_risk_level(self, risk_score: int) -> int:
        """Calculate risk level based on score"""
        if risk_score >= 15:
            return 5  # Emergency
        elif risk_score >= 12:
            return 4  # Crisis
        elif risk_score >= 8:
            return 3  # High Risk
        elif risk_score >= 5:
            return 2  # Moderate Risk
        elif risk_score >= 2:
            return 1  # Mild Concern
        else:
            return 0  # Low Risk
    
    def _check_escalation(self, risk_level: int) -> bool:
        """Check if escalation is needed"""
        return risk_level >= 4
    
    def _crisis_protocol(self, analysis: Dict) -> Dict:
        """Implement crisis intervention protocol"""
        try:
            intervention = {
                'protocol_type': 'crisis_intervention',
                'immediate_actions': [
                    "Express concern for the person's safety",
                    "Ask directly about suicidal thoughts",
                    "Provide crisis resources",
                    "Encourage professional help",
                    "Create safety plan"
                ],
                'response_template': self._get_crisis_response_template(),
                'resources': self._get_crisis_resources(),
                'follow_up_actions': [
                    "Schedule immediate follow-up",
                    "Contact emergency contact if available",
                    "Document intervention",
                    "Monitor closely"
                ]
            }
            
            self.logger.warning(f"Crisis intervention triggered: {analysis}")
            return intervention
            
        except Exception as e:
            self.logger.error(f"Error in crisis protocol: {e}")
            return {}
    
    def _emergency_protocol(self, analysis: Dict) -> Dict:
        """Implement emergency protocol"""
        try:
            intervention = {
                'protocol_type': 'emergency_response',
                'immediate_actions': [
                    "Call emergency services (911)",
                    "Stay with the person",
                    "Remove any means of self-harm",
                    "Provide immediate crisis resources",
                    "Contact emergency contact"
                ],
                'response_template': self._get_emergency_response_template(),
                'resources': self._get_emergency_resources(),
                'follow_up_actions': [
                    "Coordinate with emergency services",
                    "Document all actions taken",
                    "Follow up after emergency response",
                    "Provide ongoing support resources"
                ]
            }
            
            self.logger.critical(f"Emergency protocol triggered: {analysis}")
            return intervention
            
        except Exception as e:
            self.logger.error(f"Error in emergency protocol: {e}")
            return {}
    
    def _get_crisis_response_template(self) -> str:
        """Get crisis response template"""
        return """I'm very concerned about what you're telling me. Your safety is my top priority right now. 

I want you to know that:
- You are not alone in this
- Your feelings are valid and important
- There are people who care about you
- Professional help is available

If you're having thoughts of hurting yourself, please reach out to:
- National Suicide Prevention Lifeline: 988
- Crisis Text Line: Text HOME to 741741
- Emergency Services: 911

Would you like me to help you create a safety plan or connect you with resources?"""
    
    def _get_emergency_response_template(self) -> str:
        """Get emergency response template"""
        return """This is an emergency situation. Your safety is critical right now.

I need you to:
1. Stay with me right now
2. Call 911 or go to the nearest emergency room
3. Contact the National Suicide Prevention Lifeline: 988

If you have someone you trust nearby, please ask them to stay with you.

I'm here to support you through this crisis. Please don't give up - help is available and you matter."""
    
    def _get_crisis_resources(self) -> List[Dict]:
        """Get crisis resources"""
        return [
            self.crisis_resources['national_suicide_prevention'],
            self.crisis_resources['crisis_text_line'],
            self.crisis_resources['mental_health_america']
        ]
    
    def _get_emergency_resources(self) -> List[Dict]:
        """Get emergency resources"""
        return [
            self.crisis_resources['emergency_services'],
            self.crisis_resources['national_suicide_prevention'],
            self.crisis_resources['crisis_text_line']
        ]
    
    def create_safety_plan(self, user_preferences: Dict = None) -> Dict:
        """Create a personalized safety plan"""
        try:
            default_plan = {
                'warning_signs': [
                    "Feeling hopeless or worthless",
                    "Thoughts of self-harm or suicide",
                    "Increased isolation",
                    "Substance use increase",
                    "Sleep or appetite changes"
                ],
                'coping_strategies': [
                    "Deep breathing exercises",
                    "Calling a trusted friend or family member",
                    "Going for a walk",
                    "Listening to calming music",
                    "Practicing mindfulness"
                ],
                'social_supports': [
                    "Family members",
                    "Close friends",
                    "Mental health professional",
                    "Support group",
                    "Crisis hotline"
                ],
                'professional_resources': [
                    "Therapist or counselor",
                    "Psychiatrist",
                    "Primary care doctor",
                    "Crisis intervention team",
                    "Emergency services"
                ],
                'environmental_safety': [
                    "Remove or secure means of self-harm",
                    "Stay in a safe environment",
                    "Avoid alcohol and drugs",
                    "Ensure someone knows your location",
                    "Have emergency contacts readily available"
                ],
                'crisis_contacts': [
                    {"name": "National Suicide Prevention Lifeline", "number": "988"},
                    {"name": "Crisis Text Line", "number": "Text HOME to 741741"},
                    {"name": "Emergency Services", "number": "911"}
                ]
            }
            
            # Customize based on user preferences
            if user_preferences:
                for key, value in user_preferences.items():
                    if key in default_plan and isinstance(value, list):
                        default_plan[key] = value
            
            return default_plan
            
        except Exception as e:
            self.logger.error(f"Error creating safety plan: {e}")
            return {}
    
    def monitor_session(self, session_data: Dict) -> Dict:
        """Monitor ongoing session for crisis indicators"""
        try:
            current_analysis = {
                'text_analysis': self.analyze_text(session_data.get('user_input', '')),
                'emotion_analysis': self.analyze_emotion_pattern(session_data.get('emotion_history', [])),
                'timestamp': datetime.datetime.now()
            }
            
            # Combine risk scores
            total_risk_score = (
                current_analysis['text_analysis']['risk_score'] +
                current_analysis['emotion_analysis']['risk_score']
            )
            
            current_risk_level = self._calculate_risk_level(total_risk_score)
            
            # Update monitoring state
            self.current_risk_level = current_risk_level
            self.risk_history.append({
                'risk_level': current_risk_level,
                'risk_score': total_risk_score,
                'timestamp': datetime.datetime.now()
            })
            
            # Check for intervention needed
            intervention = None
            if current_risk_level in self.safety_protocols:
                intervention = self.safety_protocols[current_risk_level](current_analysis)
                self.intervention_log.append({
                    'intervention': intervention,
                    'risk_level': current_risk_level,
                    'timestamp': datetime.datetime.now()
                })
            
            return {
                'current_risk_level': current_risk_level,
                'risk_level_name': self.escalation_levels[current_risk_level],
                'total_risk_score': total_risk_score,
                'analysis': current_analysis,
                'intervention_needed': intervention is not None,
                'intervention': intervention,
                'monitoring_active': True
            }
            
        except Exception as e:
            self.logger.error(f"Error monitoring session: {e}")
            return {
                'current_risk_level': 0,
                'risk_level_name': 'Low Risk',
                'total_risk_score': 0,
                'analysis': {},
                'intervention_needed': False,
                'intervention': None,
                'monitoring_active': False
            }
    
    def get_monitoring_summary(self) -> Dict:
        """Get summary of monitoring session"""
        try:
            if not self.risk_history:
                return {}
            
            # Calculate statistics
            risk_levels = [entry['risk_level'] for entry in self.risk_history]
            max_risk_level = max(risk_levels)
            avg_risk_level = sum(risk_levels) / len(risk_levels)
            
            # Count interventions
            intervention_count = len(self.intervention_log)
            
            # Get risk trend
            recent_risks = risk_levels[-10:] if len(risk_levels) >= 10 else risk_levels
            risk_trend = "stable"
            if len(recent_risks) >= 3:
                if recent_risks[-1] > recent_risks[0]:
                    risk_trend = "increasing"
                elif recent_risks[-1] < recent_risks[0]:
                    risk_trend = "decreasing"
            
            return {
                'session_duration': len(self.risk_history),
                'max_risk_level': max_risk_level,
                'max_risk_level_name': self.escalation_levels[max_risk_level],
                'average_risk_level': round(avg_risk_level, 2),
                'intervention_count': intervention_count,
                'risk_trend': risk_trend,
                'current_status': self.escalation_levels[self.current_risk_level],
                'monitoring_active': self.is_monitoring
            }
            
        except Exception as e:
            self.logger.error(f"Error getting monitoring summary: {e}")
            return {}
    
    def start_monitoring(self):
        """Start crisis monitoring"""
        self.is_monitoring = True
        self.logger.info("Crisis monitoring started")
    
    def stop_monitoring(self):
        """Stop crisis monitoring"""
        self.is_monitoring = False
        self.logger.info("Crisis monitoring stopped")
    
    def reset_monitoring(self):
        """Reset monitoring state"""
        self.current_risk_level = 0
        self.risk_history = []
        self.intervention_log = []
        self.is_monitoring = False
        self.logger.info("Monitoring state reset")
    
    def export_monitoring_data(self) -> Dict:
        """Export monitoring data for research"""
        return {
            'risk_history': [
                {
                    'risk_level': entry['risk_level'],
                    'risk_score': entry['risk_score'],
                    'timestamp': entry['timestamp'].isoformat()
                }
                for entry in self.risk_history
            ],
            'intervention_log': [
                {
                    'intervention': entry['intervention'],
                    'risk_level': entry['risk_level'],
                    'timestamp': entry['timestamp'].isoformat()
                }
                for entry in self.intervention_log
            ],
            'monitoring_summary': self.get_monitoring_summary()
        }
