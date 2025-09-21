"""
NURSE Framework Therapeutic Response System
Implements Naming, Understanding, Respecting, Supporting, Exploring approach
"""

import random
import logging
from typing import Dict, List, Optional, Tuple
from textblob import TextBlob
import json
import datetime

class NURSEFramework:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session_context = {}
        self.emotion_history = []
        self.conversation_history = []
        
        # Initialize response templates
        self._initialize_response_templates()
        
        # Crisis keywords for risk assessment
        self.crisis_keywords = [
            'suicide', 'kill myself', 'end it all', 'not worth living',
            'hurt myself', 'self harm', 'cut myself', 'overdose',
            'die', 'death', 'hopeless', 'worthless', 'burden'
        ]
        
        # Emotion-specific response strategies
        self.emotion_strategies = {
            'Sad': ['naming', 'understanding', 'supporting'],
            'Angry': ['naming', 'respecting', 'exploring'],
            'Fear': ['understanding', 'supporting', 'exploring'],
            'Happy': ['respecting', 'exploring'],
            'Neutral': ['exploring', 'understanding'],
            'Disgust': ['naming', 'understanding'],
            'Surprise': ['understanding', 'exploring']
        }
    
    def _initialize_response_templates(self):
        """Initialize NURSE framework response templates"""
        self.response_templates = {
            'naming': {
                'Sad': [
                    "I can see that you're feeling sad right now.",
                    "It sounds like you're experiencing sadness.",
                    "I notice sadness in your expression and words.",
                    "You seem to be feeling down at the moment."
                ],
                'Angry': [
                    "I can sense that you're feeling angry.",
                    "It sounds like you're experiencing frustration or anger.",
                    "I notice anger in your expression.",
                    "You seem to be feeling upset right now."
                ],
                'Fear': [
                    "I can see that you're feeling anxious or fearful.",
                    "It sounds like you're experiencing worry or fear.",
                    "I notice anxiety in your expression.",
                    "You seem to be feeling scared or worried."
                ],
                'Happy': [
                    "I can see that you're feeling happy right now.",
                    "It sounds like you're experiencing joy.",
                    "I notice happiness in your expression.",
                    "You seem to be in a good mood."
                ],
                'Neutral': [
                    "I can see that you're feeling calm right now.",
                    "It sounds like you're in a neutral state.",
                    "I notice a calm expression.",
                    "You seem to be feeling balanced."
                ]
            },
            
            'understanding': {
                'Sad': [
                    "It's completely understandable to feel sad when going through difficult times.",
                    "Sadness is a natural response to challenging situations.",
                    "I can understand why you might be feeling this way.",
                    "It makes sense that you're feeling sad given what you're experiencing."
                ],
                'Angry': [
                    "It's understandable to feel angry when things don't go as expected.",
                    "Anger is a natural response to feeling hurt or frustrated.",
                    "I can understand why you might be feeling upset.",
                    "It makes sense that you're feeling angry given the situation."
                ],
                'Fear': [
                    "It's completely normal to feel anxious when facing uncertainty.",
                    "Fear is a natural response to perceived threats.",
                    "I can understand why you might be feeling worried.",
                    "It makes sense that you're feeling anxious given the circumstances."
                ],
                'Happy': [
                    "It's wonderful that you're feeling happy right now.",
                    "Joy is such a beautiful emotion to experience.",
                    "I'm glad to see you're feeling good.",
                    "It's great that you're in a positive mood."
                ],
                'Neutral': [
                    "It's good that you're feeling calm and centered.",
                    "A neutral state can be quite peaceful.",
                    "I'm glad you're feeling balanced.",
                    "It's nice to see you in a calm state."
                ]
            },
            
            'respecting': {
                'Sad': [
                    "Your feelings are completely valid and important.",
                    "I respect that you're sharing this with me.",
                    "It takes courage to acknowledge and express sadness.",
                    "Your emotions deserve to be heard and respected."
                ],
                'Angry': [
                    "Your anger is a valid emotion that deserves to be acknowledged.",
                    "I respect that you're expressing your feelings honestly.",
                    "It's important that your frustration is heard.",
                    "Your feelings are completely valid."
                ],
                'Fear': [
                    "Your fears and worries are completely valid.",
                    "I respect that you're sharing your concerns with me.",
                    "It takes courage to acknowledge anxiety.",
                    "Your feelings deserve to be taken seriously."
                ],
                'Happy': [
                    "I'm happy that you're feeling good right now.",
                    "Your joy is wonderful to see.",
                    "I respect and celebrate your positive feelings.",
                    "It's great that you're sharing your happiness."
                ],
                'Neutral': [
                    "I respect your calm and balanced state.",
                    "Your peaceful feelings are valuable.",
                    "It's good that you're feeling centered.",
                    "I appreciate your calm demeanor."
                ]
            },
            
            'supporting': {
                'Sad': [
                    "I'm here to support you through this difficult time.",
                    "You don't have to face this sadness alone.",
                    "I want you to know that I care about how you're feeling.",
                    "Let's work together to help you feel better."
                ],
                'Angry': [
                    "I'm here to help you work through these feelings.",
                    "Let's find healthy ways to process your anger.",
                    "I want to support you in managing these emotions.",
                    "Together we can find constructive ways to handle this."
                ],
                'Fear': [
                    "I'm here to help you feel safer and more secure.",
                    "Let's work together to address your concerns.",
                    "I want to support you in managing your anxiety.",
                    "Together we can find ways to help you feel more calm."
                ],
                'Happy': [
                    "I'm glad I can be here to share in your joy.",
                    "It's wonderful to see you feeling so good.",
                    "I'm here to help you maintain this positive feeling.",
                    "Let's work together to keep this good energy going."
                ],
                'Neutral': [
                    "I'm here to support you in maintaining this calm state.",
                    "It's good that you're feeling balanced.",
                    "I'm here if you need anything.",
                    "Let's work together to keep you feeling centered."
                ]
            },
            
            'exploring': {
                'Sad': [
                    "Can you tell me more about what's making you feel sad?",
                    "What thoughts or situations are contributing to this sadness?",
                    "When did you first notice feeling this way?",
                    "What would help you feel less sad right now?"
                ],
                'Angry': [
                    "Can you help me understand what's making you feel angry?",
                    "What specific situation is causing this frustration?",
                    "When did you first start feeling this way?",
                    "What would help you feel calmer right now?"
                ],
                'Fear': [
                    "Can you tell me more about what's worrying you?",
                    "What specific concerns are on your mind?",
                    "When did you first start feeling anxious?",
                    "What would help you feel safer right now?"
                ],
                'Happy': [
                    "Can you tell me more about what's making you feel happy?",
                    "What's contributing to this positive feeling?",
                    "What would help you maintain this good mood?",
                    "How can we build on this positive energy?"
                ],
                'Neutral': [
                    "Can you tell me more about how you're feeling right now?",
                    "What's helping you maintain this calm state?",
                    "Is there anything specific on your mind?",
                    "What would you like to explore or discuss?"
                ]
            }
        }
    
    def analyze_sentiment(self, text: str) -> float:
        """Analyze sentiment of user input"""
        try:
            blob = TextBlob(text)
            return blob.sentiment.polarity  # -1 to 1 scale
        except Exception as e:
            self.logger.error(f"Error analyzing sentiment: {e}")
            return 0.0
    
    def assess_risk_level(self, text: str, emotion: str) -> Tuple[int, List[str]]:
        """Assess risk level based on text and emotion"""
        try:
            risk_score = 0
            risk_factors = []
            
            text_lower = text.lower()
            
            # Check for crisis keywords
            for keyword in self.crisis_keywords:
                if keyword in text_lower:
                    risk_score += 3
                    risk_factors.append(f"Crisis keyword detected: {keyword}")
            
            # Emotion-based risk assessment
            if emotion in ['Sad', 'Angry']:
                risk_score += 1
                risk_factors.append(f"Negative emotion detected: {emotion}")
            
            # Sentiment analysis
            sentiment = self.analyze_sentiment(text)
            if sentiment < -0.5:
                risk_score += 2
                risk_factors.append("Very negative sentiment detected")
            elif sentiment < -0.2:
                risk_score += 1
                risk_factors.append("Negative sentiment detected")
            
            # Intensity indicators
            intensity_words = ['extremely', 'terribly', 'awfully', 'completely', 'totally', 'absolutely']
            for word in intensity_words:
                if word in text_lower:
                    risk_score += 1
                    risk_factors.append(f"Intensity indicator: {word}")
            
            return min(risk_score, 10), risk_factors  # Cap at 10
            
        except Exception as e:
            self.logger.error(f"Error assessing risk level: {e}")
            return 0, []
    
    def generate_response(self, user_input: str, detected_emotion: str, 
                         confidence: float, session_context: Dict) -> Dict:
        """Generate therapeutic response using NURSE framework"""
        try:
            # Update session context
            self.session_context.update(session_context)
            self.emotion_history.append({
                'emotion': detected_emotion,
                'confidence': confidence,
                'timestamp': datetime.datetime.now()
            })
            
            # Assess risk level
            risk_score, risk_factors = self.assess_risk_level(user_input, detected_emotion)
            
            # Determine appropriate NURSE components
            strategies = self.emotion_strategies.get(detected_emotion, ['understanding', 'supporting'])
            
            # Select primary strategy based on risk level
            if risk_score >= 7:
                primary_strategy = 'supporting'
                secondary_strategy = 'understanding'
            elif risk_score >= 4:
                primary_strategy = 'understanding'
                secondary_strategy = 'supporting'
            else:
                primary_strategy = strategies[0] if strategies else 'understanding'
                secondary_strategy = strategies[1] if len(strategies) > 1 else 'exploring'
            
            # Generate response
            response = self._generate_nurse_response(
                user_input, detected_emotion, primary_strategy, secondary_strategy
            )
            
            # Add crisis intervention if needed
            if risk_score >= 7:
                response = self._add_crisis_intervention(response, risk_score)
            
            # Log conversation
            self.conversation_history.append({
                'user_input': user_input,
                'detected_emotion': detected_emotion,
                'confidence': confidence,
                'risk_score': risk_score,
                'response': response['text'],
                'strategies_used': [primary_strategy, secondary_strategy],
                'timestamp': datetime.datetime.now()
            })
            
            return {
                'response_text': response['text'],
                'strategies_used': [primary_strategy, secondary_strategy],
                'risk_score': risk_score,
                'risk_factors': risk_factors,
                'crisis_intervention': response.get('crisis_intervention', False),
                'follow_up_suggestions': response.get('follow_up_suggestions', []),
                'therapeutic_approach': f"NURSE-{primary_strategy.capitalize()}"
            }
            
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            return {
                'response_text': "I'm here to listen and support you. Can you tell me more about how you're feeling?",
                'strategies_used': ['supporting'],
                'risk_score': 0,
                'risk_factors': [],
                'crisis_intervention': False,
                'follow_up_suggestions': [],
                'therapeutic_approach': 'NURSE-Supporting'
            }
    
    def _generate_nurse_response(self, user_input: str, emotion: str, 
                               primary_strategy: str, secondary_strategy: str) -> Dict:
        """Generate response using NURSE framework components"""
        try:
            # Get templates for the emotion
            primary_templates = self.response_templates.get(primary_strategy, {}).get(emotion, [])
            secondary_templates = self.response_templates.get(secondary_strategy, {}).get(emotion, [])
            
            # Select random templates
            primary_response = random.choice(primary_templates) if primary_templates else ""
            secondary_response = random.choice(secondary_templates) if secondary_templates else ""
            
            # Combine responses
            if primary_response and secondary_response:
                response_text = f"{primary_response} {secondary_response}"
            elif primary_response:
                response_text = primary_response
            else:
                response_text = "I'm here to listen and support you. Can you tell me more about how you're feeling?"
            
            # Add personalized elements based on user input
            response_text = self._personalize_response(response_text, user_input, emotion)
            
            return {
                'text': response_text,
                'crisis_intervention': False,
                'follow_up_suggestions': self._get_follow_up_suggestions(emotion, primary_strategy)
            }
            
        except Exception as e:
            self.logger.error(f"Error generating NURSE response: {e}")
            return {
                'text': "I'm here to listen and support you. Can you tell me more about how you're feeling?",
                'crisis_intervention': False,
                'follow_up_suggestions': []
            }
    
    def _personalize_response(self, response: str, user_input: str, emotion: str) -> str:
        """Personalize response based on user input"""
        try:
            # Extract key topics from user input
            user_words = user_input.lower().split()
            
            # Add context-specific elements
            if 'work' in user_words or 'job' in user_words:
                response += " I understand that work-related stress can be overwhelming."
            elif 'family' in user_words or 'relationship' in user_words:
                response += " Family and relationship issues can be particularly challenging."
            elif 'health' in user_words or 'sick' in user_words:
                response += " Health concerns can understandably cause worry."
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error personalizing response: {e}")
            return response
    
    def _get_follow_up_suggestions(self, emotion: str, strategy: str) -> List[str]:
        """Get follow-up suggestions based on emotion and strategy"""
        suggestions = {
            'Sad': [
                "Would you like to try a breathing exercise to help you feel calmer?",
                "Would you like to talk about what's making you feel this way?",
                "Would you like to try a mood-lifting activity?"
            ],
            'Angry': [
                "Would you like to try some relaxation techniques?",
                "Would you like to talk about what's causing these feelings?",
                "Would you like to try a calming exercise?"
            ],
            'Fear': [
                "Would you like to try some anxiety-reducing techniques?",
                "Would you like to talk about your concerns?",
                "Would you like to try a grounding exercise?"
            ],
            'Happy': [
                "Would you like to explore what's making you feel good?",
                "Would you like to try to maintain this positive feeling?",
                "Would you like to share more about what's going well?"
            ],
            'Neutral': [
                "Would you like to explore your thoughts and feelings?",
                "Would you like to try a mindfulness exercise?",
                "Would you like to talk about what's on your mind?"
            ]
        }
        
        return suggestions.get(emotion, [
            "Would you like to talk more about how you're feeling?",
            "Would you like to try a relaxation exercise?",
            "Would you like to explore your thoughts?"
        ])
    
    def _add_crisis_intervention(self, response: Dict, risk_score: int) -> Dict:
        """Add crisis intervention elements to response"""
        crisis_responses = [
            "I'm very concerned about what you're telling me. Your safety is important.",
            "It sounds like you're going through an extremely difficult time right now.",
            "I want you to know that there are people who care about you and want to help."
        ]
        
        crisis_response = random.choice(crisis_responses)
        
        response['text'] = f"{response['text']} {crisis_response}"
        response['crisis_intervention'] = True
        
        # Add crisis resources
        response['crisis_resources'] = [
            "National Suicide Prevention Lifeline: 988",
            "Crisis Text Line: Text HOME to 741741",
            "Emergency Services: 911"
        ]
        
        return response
    
    def get_session_summary(self) -> Dict:
        """Get summary of current session"""
        try:
            if not self.conversation_history:
                return {}
            
            # Calculate emotion distribution
            emotion_counts = {}
            total_risk_score = 0
            
            for entry in self.conversation_history:
                emotion = entry['detected_emotion']
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
                total_risk_score += entry['risk_score']
            
            avg_risk_score = total_risk_score / len(self.conversation_history)
            
            # Get most common emotion
            dominant_emotion = max(emotion_counts, key=emotion_counts.get) if emotion_counts else 'Neutral'
            
            # Get strategies used
            strategies_used = set()
            for entry in self.conversation_history:
                strategies_used.update(entry['strategies_used'])
            
            return {
                'total_interactions': len(self.conversation_history),
                'emotion_distribution': emotion_counts,
                'dominant_emotion': dominant_emotion,
                'average_risk_score': avg_risk_score,
                'strategies_used': list(strategies_used),
                'session_duration': self._calculate_session_duration(),
                'crisis_interventions': sum(1 for entry in self.conversation_history if entry.get('crisis_intervention', False))
            }
            
        except Exception as e:
            self.logger.error(f"Error generating session summary: {e}")
            return {}
    
    def _calculate_session_duration(self) -> float:
        """Calculate session duration in minutes"""
        try:
            if len(self.conversation_history) < 2:
                return 0.0
            
            start_time = self.conversation_history[0]['timestamp']
            end_time = self.conversation_history[-1]['timestamp']
            duration = (end_time - start_time).total_seconds() / 60
            return round(duration, 2)
            
        except Exception as e:
            self.logger.error(f"Error calculating session duration: {e}")
            return 0.0
    
    def reset_session(self):
        """Reset session data"""
        self.session_context = {}
        self.emotion_history = []
        self.conversation_history = []
        self.logger.info("Session data reset")
    
    def export_session_data(self) -> Dict:
        """Export session data for research analysis"""
        return {
            'session_context': self.session_context,
            'emotion_history': [
                {
                    'emotion': entry['emotion'],
                    'confidence': entry['confidence'],
                    'timestamp': entry['timestamp'].isoformat()
                }
                for entry in self.emotion_history
            ],
            'conversation_history': [
                {
                    'user_input': entry['user_input'],
                    'detected_emotion': entry['detected_emotion'],
                    'confidence': entry['confidence'],
                    'risk_score': entry['risk_score'],
                    'response': entry['response'],
                    'strategies_used': entry['strategies_used'],
                    'timestamp': entry['timestamp'].isoformat()
                }
                for entry in self.conversation_history
            ],
            'session_summary': self.get_session_summary()
        }
