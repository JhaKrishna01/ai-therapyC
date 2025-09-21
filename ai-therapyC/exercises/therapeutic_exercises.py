"""
Therapeutic Exercises and Mood-Lifting Activities
Provides guided exercises, breathing techniques, journaling prompts, and relaxation activities
"""

import random
import time
import threading
import logging
from typing import Dict, List, Optional, Callable
import json
import datetime

class TherapeuticExercises:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.active_exercises = {}
        self.exercise_history = []
        
        # Initialize exercise categories
        self._initialize_breathing_exercises()
        self._initialize_mindfulness_exercises()
        self._initialize_journaling_prompts()
        self._initialize_relaxation_exercises()
        self._initialize_mood_lifting_activities()
    
    def _initialize_breathing_exercises(self):
        """Initialize breathing exercise templates"""
        self.breathing_exercises = {
            'box_breathing': {
                'name': 'Box Breathing (4-4-4-4)',
                'description': 'A calming technique used by Navy SEALs to reduce stress',
                'steps': [
                    'Breathe in slowly for 4 counts',
                    'Hold your breath for 4 counts', 
                    'Breathe out slowly for 4 counts',
                    'Hold empty for 4 counts',
                    'Repeat the cycle'
                ],
                'duration': 300,  # 5 minutes
                'benefits': 'Reduces anxiety, improves focus, calms nervous system'
            },
            '478_breathing': {
                'name': '4-7-8 Breathing',
                'description': 'A technique to quickly calm the nervous system',
                'steps': [
                    'Breathe in through nose for 4 counts',
                    'Hold breath for 7 counts',
                    'Breathe out through mouth for 8 counts',
                    'Repeat 4 times'
                ],
                'duration': 120,  # 2 minutes
                'benefits': 'Quick stress relief, better sleep, anxiety reduction'
            },
            'diaphragmatic_breathing': {
                'name': 'Diaphragmatic Breathing',
                'description': 'Deep belly breathing to activate relaxation response',
                'steps': [
                    'Place one hand on chest, one on belly',
                    'Breathe deeply so belly rises, chest stays still',
                    'Exhale slowly, feeling belly fall',
                    'Focus on slow, deep breaths'
                ],
                'duration': 180,  # 3 minutes
                'benefits': 'Activates parasympathetic nervous system, reduces cortisol'
            },
            'alternate_nostril': {
                'name': 'Alternate Nostril Breathing',
                'description': 'Balancing breathing technique from yoga tradition',
                'steps': [
                    'Close right nostril with thumb, inhale through left',
                    'Close left nostril with ring finger, exhale through right',
                    'Inhale through right nostril',
                    'Close right nostril, exhale through left',
                    'Continue alternating'
                ],
                'duration': 240,  # 4 minutes
                'benefits': 'Balances nervous system, improves focus, reduces stress'
            }
        }
    
    def _initialize_mindfulness_exercises(self):
        """Initialize mindfulness exercise templates"""
        self.mindfulness_exercises = {
            'body_scan': {
                'name': 'Body Scan Meditation',
                'description': 'Progressive relaxation through body awareness',
                'steps': [
                    'Start at the top of your head',
                    'Notice any tension or sensations',
                    'Slowly move down through each body part',
                    'Release tension as you go',
                    'End at your toes'
                ],
                'duration': 600,  # 10 minutes
                'benefits': 'Reduces physical tension, improves body awareness'
            },
            'loving_kindness': {
                'name': 'Loving-Kindness Meditation',
                'description': 'Cultivate compassion for yourself and others',
                'steps': [
                    'Send loving thoughts to yourself',
                    'Think of someone you love',
                    'Send loving thoughts to them',
                    'Think of a neutral person',
                    'Send loving thoughts to them',
                    'Think of someone difficult',
                    'Send loving thoughts to them'
                ],
                'duration': 480,  # 8 minutes
                'benefits': 'Increases compassion, reduces negative emotions'
            },
            'mindful_walking': {
                'name': 'Mindful Walking',
                'description': 'Walking meditation for grounding and presence',
                'steps': [
                    'Walk slowly and deliberately',
                    'Feel each step connecting with ground',
                    'Notice your surroundings',
                    'Focus on the present moment',
                    'If mind wanders, gently return to walking'
                ],
                'duration': 300,  # 5 minutes
                'benefits': 'Grounding, present moment awareness, gentle movement'
            },
            'five_senses': {
                'name': 'Five Senses Grounding',
                'description': 'Quick grounding technique using all senses',
                'steps': [
                    'Name 5 things you can see',
                    'Name 4 things you can touch',
                    'Name 3 things you can hear',
                    'Name 2 things you can smell',
                    'Name 1 thing you can taste'
                ],
                'duration': 60,  # 1 minute
                'benefits': 'Quick grounding, anxiety relief, present moment awareness'
            }
        }
    
    def _initialize_journaling_prompts(self):
        """Initialize journaling prompt templates"""
        self.journaling_prompts = {
            'emotion_exploration': {
                'name': 'Emotion Exploration',
                'prompts': [
                    'What emotion am I feeling right now?',
                    'Where do I feel this emotion in my body?',
                    'What thoughts are connected to this emotion?',
                    'What might have triggered this feeling?',
                    'What would I tell a friend feeling this way?'
                ],
                'duration': 600,  # 10 minutes
                'benefits': 'Emotional awareness, self-compassion, insight'
            },
            'gratitude_practice': {
                'name': 'Gratitude Practice',
                'prompts': [
                    'What am I grateful for today?',
                    'Who am I grateful for in my life?',
                    'What small moments brought me joy today?',
                    'What challenges taught me something valuable?',
                    'How can I express gratitude to others?'
                ],
                'duration': 300,  # 5 minutes
                'benefits': 'Increases positive emotions, improves mood, builds resilience'
            },
            'stress_processing': {
                'name': 'Stress Processing',
                'prompts': [
                    'What is causing me stress right now?',
                    'What aspects of this situation can I control?',
                    'What aspects are outside my control?',
                    'What coping strategies have worked for me before?',
                    'What support do I need right now?'
                ],
                'duration': 480,  # 8 minutes
                'benefits': 'Stress reduction, problem-solving, self-awareness'
            },
            'self_compassion': {
                'name': 'Self-Compassion Practice',
                'prompts': [
                    'How am I treating myself right now?',
                    'What would I say to a good friend in my situation?',
                    'What do I need to hear right now?',
                    'How can I be kinder to myself today?',
                    'What strengths do I have that I can rely on?'
                ],
                'duration': 360,  # 6 minutes
                'benefits': 'Self-compassion, emotional healing, self-acceptance'
            },
            'future_visioning': {
                'name': 'Future Visioning',
                'prompts': [
                    'What do I want my life to look like in one year?',
                    'What values are most important to me?',
                    'What steps can I take toward my goals?',
                    'What obstacles might I face?',
                    'How will I know I\'m making progress?'
                ],
                'duration': 600,  # 10 minutes
                'benefits': 'Goal setting, motivation, hope, direction'
            }
        }
    
    def _initialize_relaxation_exercises(self):
        """Initialize relaxation exercise templates"""
        self.relaxation_exercises = {
            'progressive_muscle': {
                'name': 'Progressive Muscle Relaxation',
                'description': 'Systematically tense and release muscle groups',
                'steps': [
                    'Start with your feet, tense for 5 seconds',
                    'Release and feel the relaxation',
                    'Move up to calves, tense and release',
                    'Continue through thighs, abdomen, arms, shoulders',
                    'End with facial muscles',
                    'Feel the overall relaxation'
                ],
                'duration': 900,  # 15 minutes
                'benefits': 'Reduces muscle tension, promotes relaxation, improves sleep'
            },
            'visualization': {
                'name': 'Guided Visualization',
                'description': 'Create a peaceful mental sanctuary',
                'steps': [
                    'Close your eyes and take deep breaths',
                    'Imagine a peaceful place (beach, forest, garden)',
                    'Use all your senses to experience this place',
                    'Feel the peace and safety there',
                    'Stay in this place for a few minutes',
                    'Slowly return to the present moment'
                ],
                'duration': 600,  # 10 minutes
                'benefits': 'Stress relief, mental escape, relaxation'
            },
            'autogenic_training': {
                'name': 'Autogenic Training',
                'description': 'Self-hypnosis technique for deep relaxation',
                'steps': [
                    'Focus on heaviness in your limbs',
                    'Feel warmth spreading through your body',
                    'Notice your calm, steady heartbeat',
                    'Feel your breathing becoming natural',
                    'Experience warmth in your abdomen',
                    'Feel coolness on your forehead'
                ],
                'duration': 1200,  # 20 minutes
                'benefits': 'Deep relaxation, stress reduction, self-regulation'
            }
        }
    
    def _initialize_mood_lifting_activities(self):
        """Initialize mood-lifting activity templates"""
        self.mood_lifting_activities = {
            'music_therapy': {
                'name': 'Music Therapy',
                'description': 'Use music to improve mood and emotional state',
                'activities': [
                    'Listen to uplifting music',
                    'Sing along to favorite songs',
                    'Dance to energetic music',
                    'Play calming instrumental music',
                    'Create a mood-boosting playlist'
                ],
                'duration': 300,  # 5 minutes
                'benefits': 'Mood elevation, emotional expression, stress relief'
            },
            'movement_break': {
                'name': 'Movement Break',
                'description': 'Gentle physical activity to boost mood',
                'activities': [
                    'Take a short walk',
                    'Do gentle stretching',
                    'Try simple yoga poses',
                    'Dance to favorite music',
                    'Do jumping jacks or light exercise'
                ],
                'duration': 180,  # 3 minutes
                'benefits': 'Endorphin release, energy boost, mood improvement'
            },
            'nature_connection': {
                'name': 'Nature Connection',
                'description': 'Connect with nature to improve wellbeing',
                'activities': [
                    'Look out the window at nature',
                    'Take photos of beautiful things',
                    'Spend time in a garden or park',
                    'Listen to nature sounds',
                    'Practice outdoor mindfulness'
                ],
                'duration': 240,  # 4 minutes
                'benefits': 'Stress reduction, mood improvement, connection'
            },
            'creative_expression': {
                'name': 'Creative Expression',
                'description': 'Express emotions through creative activities',
                'activities': [
                    'Draw or sketch your feelings',
                    'Write poetry or short stories',
                    'Take creative photos',
                    'Do simple crafts',
                    'Express through movement or dance'
                ],
                'duration': 600,  # 10 minutes
                'benefits': 'Emotional expression, creativity, self-discovery'
            },
            'social_connection': {
                'name': 'Social Connection',
                'description': 'Connect with others to improve mood',
                'activities': [
                    'Call a friend or family member',
                    'Send a thoughtful message',
                    'Share something positive on social media',
                    'Write a thank you note',
                    'Plan a future social activity'
                ],
                'duration': 300,  # 5 minutes
                'benefits': 'Social support, mood improvement, connection'
            }
        }
    
    def get_exercise_recommendation(self, emotion: str, risk_level: int = 0) -> Dict:
        """Get personalized exercise recommendation based on emotion and risk level"""
        try:
            recommendations = []
            
            # High risk - focus on crisis intervention and grounding
            if risk_level >= 4:
                recommendations.extend([
                    self.breathing_exercises['box_breathing'],
                    self.mindfulness_exercises['five_senses'],
                    self.relaxation_exercises['progressive_muscle']
                ])
            
            # Emotion-specific recommendations
            elif emotion == 'Sad':
                recommendations.extend([
                    self.mood_lifting_activities['music_therapy'],
                    self.journaling_prompts['gratitude_practice'],
                    self.mindfulness_exercises['loving_kindness'],
                    self.mood_lifting_activities['movement_break']
                ])
            
            elif emotion == 'Angry':
                recommendations.extend([
                    self.breathing_exercises['box_breathing'],
                    self.relaxation_exercises['progressive_muscle'],
                    self.mindfulness_exercises['body_scan'],
                    self.mood_lifting_activities['movement_break']
                ])
            
            elif emotion == 'Fear':
                recommendations.extend([
                    self.breathing_exercises['478_breathing'],
                    self.mindfulness_exercises['five_senses'],
                    self.relaxation_exercises['visualization'],
                    self.journaling_prompts['stress_processing']
                ])
            
            elif emotion == 'Happy':
                recommendations.extend([
                    self.journaling_prompts['gratitude_practice'],
                    self.mood_lifting_activities['creative_expression'],
                    self.mindfulness_exercises['mindful_walking'],
                    self.mood_lifting_activities['social_connection']
                ])
            
            else:  # Neutral or other emotions
                recommendations.extend([
                    self.mindfulness_exercises['body_scan'],
                    self.journaling_prompts['emotion_exploration'],
                    self.breathing_exercises['diaphragmatic_breathing'],
                    self.mood_lifting_activities['nature_connection']
                ])
            
            # Select random recommendation
            selected = random.choice(recommendations)
            
            return {
                'exercise_type': selected['name'],
                'description': selected['description'],
                'steps': selected.get('steps', selected.get('activities', selected.get('prompts', []))),
                'duration': selected['duration'],
                'benefits': selected['benefits'],
                'recommended_for': emotion,
                'risk_level': risk_level
            }
            
        except Exception as e:
            self.logger.error(f"Error getting exercise recommendation: {e}")
            return {}
    
    def start_exercise(self, exercise_id: str, exercise_data: Dict, 
                      progress_callback: Optional[Callable] = None) -> str:
        """Start a therapeutic exercise"""
        try:
            exercise_session_id = f"exercise_{int(time.time())}"
            
            # Create exercise session
            exercise_session = {
                'id': exercise_session_id,
                'exercise_id': exercise_id,
                'exercise_data': exercise_data,
                'start_time': datetime.datetime.now(),
                'status': 'active',
                'progress_callback': progress_callback,
                'current_step': 0,
                'total_steps': len(exercise_data.get('steps', [])),
                'duration': exercise_data.get('duration', 300)
            }
            
            self.active_exercises[exercise_session_id] = exercise_session
            
            # Start exercise thread
            exercise_thread = threading.Thread(
                target=self._run_exercise,
                args=(exercise_session_id,),
                daemon=True
            )
            exercise_thread.start()
            
            self.logger.info(f"Started exercise {exercise_id} with session {exercise_session_id}")
            return exercise_session_id
            
        except Exception as e:
            self.logger.error(f"Error starting exercise: {e}")
            return ""
    
    def _run_exercise(self, session_id: str):
        """Run the exercise in a separate thread"""
        try:
            if session_id not in self.active_exercises:
                return
            
            exercise_session = self.active_exercises[session_id]
            exercise_data = exercise_session['exercise_data']
            steps = exercise_data.get('steps', [])
            duration = exercise_session['duration']
            
            start_time = time.time()
            
            # Run through steps
            for i, step in enumerate(steps):
                if session_id not in self.active_exercises:
                    break
                
                exercise_session['current_step'] = i
                
                # Call progress callback if provided
                if exercise_session['progress_callback']:
                    exercise_session['progress_callback']({
                        'session_id': session_id,
                        'current_step': i,
                        'total_steps': len(steps),
                        'step_text': step,
                        'progress': (i / len(steps)) * 100
                    })
                
                # Wait for step duration
                step_duration = duration / len(steps)
                time.sleep(step_duration)
            
            # Complete exercise
            if session_id in self.active_exercises:
                exercise_session['status'] = 'completed'
                exercise_session['end_time'] = datetime.datetime.now()
                
                # Log completion
                self.exercise_history.append({
                    'session_id': session_id,
                    'exercise_id': exercise_session['exercise_id'],
                    'duration': time.time() - start_time,
                    'completed_at': datetime.datetime.now()
                })
                
                # Final callback
                if exercise_session['progress_callback']:
                    exercise_session['progress_callback']({
                        'session_id': session_id,
                        'status': 'completed',
                        'progress': 100
                    })
                
                self.logger.info(f"Completed exercise session {session_id}")
            
        except Exception as e:
            self.logger.error(f"Error running exercise {session_id}: {e}")
            if session_id in self.active_exercises:
                self.active_exercises[session_id]['status'] = 'error'
    
    def stop_exercise(self, session_id: str) -> bool:
        """Stop an active exercise"""
        try:
            if session_id in self.active_exercises:
                self.active_exercises[session_id]['status'] = 'stopped'
                del self.active_exercises[session_id]
                self.logger.info(f"Stopped exercise session {session_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error stopping exercise {session_id}: {e}")
            return False
    
    def get_exercise_status(self, session_id: str) -> Dict:
        """Get status of an exercise session"""
        try:
            if session_id in self.active_exercises:
                session = self.active_exercises[session_id]
                return {
                    'session_id': session_id,
                    'status': session['status'],
                    'current_step': session['current_step'],
                    'total_steps': session['total_steps'],
                    'progress': (session['current_step'] / session['total_steps']) * 100,
                    'duration': session['duration']
                }
            return {}
        except Exception as e:
            self.logger.error(f"Error getting exercise status: {e}")
            return {}
    
    def get_breathing_exercise(self, exercise_type: str = None) -> Dict:
        """Get a specific breathing exercise"""
        try:
            if exercise_type and exercise_type in self.breathing_exercises:
                return self.breathing_exercises[exercise_type]
            else:
                # Return random breathing exercise
                return random.choice(list(self.breathing_exercises.values()))
        except Exception as e:
            self.logger.error(f"Error getting breathing exercise: {e}")
            return {}
    
    def get_journaling_prompt(self, prompt_type: str = None) -> Dict:
        """Get a specific journaling prompt"""
        try:
            if prompt_type and prompt_type in self.journaling_prompts:
                return self.journaling_prompts[prompt_type]
            else:
                # Return random journaling prompt
                return random.choice(list(self.journaling_prompts.values()))
        except Exception as e:
            self.logger.error(f"Error getting journaling prompt: {e}")
            return {}
    
    def get_mood_lifting_activity(self, activity_type: str = None) -> Dict:
        """Get a specific mood-lifting activity"""
        try:
            if activity_type and activity_type in self.mood_lifting_activities:
                return self.mood_lifting_activities[activity_type]
            else:
                # Return random mood-lifting activity
                return random.choice(list(self.mood_lifting_activities.values()))
        except Exception as e:
            self.logger.error(f"Error getting mood-lifting activity: {e}")
            return {}
    
    def get_exercise_history(self) -> List[Dict]:
        """Get history of completed exercises"""
        return self.exercise_history.copy()
    
    def get_exercise_statistics(self) -> Dict:
        """Get statistics about exercise usage"""
        try:
            if not self.exercise_history:
                return {}
            
            # Count exercises by type
            exercise_counts = {}
            total_duration = 0
            
            for entry in self.exercise_history:
                exercise_id = entry['exercise_id']
                exercise_counts[exercise_id] = exercise_counts.get(exercise_id, 0) + 1
                total_duration += entry['duration']
            
            return {
                'total_exercises': len(self.exercise_history),
                'exercise_counts': exercise_counts,
                'total_duration': total_duration,
                'average_duration': total_duration / len(self.exercise_history),
                'most_popular_exercise': max(exercise_counts, key=exercise_counts.get) if exercise_counts else None
            }
            
        except Exception as e:
            self.logger.error(f"Error getting exercise statistics: {e}")
            return {}
    
    def export_exercise_data(self) -> Dict:
        """Export exercise data for research"""
        return {
            'exercise_history': [
                {
                    'session_id': entry['session_id'],
                    'exercise_id': entry['exercise_id'],
                    'duration': entry['duration'],
                    'completed_at': entry['completed_at'].isoformat()
                }
                for entry in self.exercise_history
            ],
            'exercise_statistics': self.get_exercise_statistics(),
            'available_exercises': {
                'breathing': list(self.breathing_exercises.keys()),
                'mindfulness': list(self.mindfulness_exercises.keys()),
                'journaling': list(self.journaling_prompts.keys()),
                'relaxation': list(self.relaxation_exercises.keys()),
                'mood_lifting': list(self.mood_lifting_activities.keys())
            }
        }
