"""
Real-time Emotion Detection Module
Uses OpenCV and TensorFlow for webcam-based emotion recognition
"""

import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import threading
import queue
import time
import logging
from typing import Dict, List, Optional, Tuple
import os

class EmotionDetector:
    def __init__(self, model_path: str = None):
        self.logger = logging.getLogger(__name__)
        self.emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
        self.model = None
        self.face_cascade = None
        self.is_running = False
        self.frame_queue = queue.Queue(maxsize=10)
        self.emotion_queue = queue.Queue(maxsize=50)
        self.current_emotion = "Neutral"
        self.current_confidence = 0.0
        self.face_detected = False
        
        # Initialize components
        self._load_model(model_path)
        self._load_face_cascade()
    
    def _load_model(self, model_path: str = None):
        """Load the emotion detection model"""
        try:
            if model_path and os.path.exists(model_path):
                self.model = load_model(model_path)
                self.logger.info(f"Loaded emotion model from {model_path}")
            else:
                # Create a simple CNN model for emotion detection
                self.model = self._create_default_model()
                self.logger.info("Created default emotion detection model")
        except Exception as e:
            self.logger.error(f"Error loading emotion model: {e}")
            self.model = self._create_default_model()
    
    def _create_default_model(self):
        """Create a default CNN model for emotion detection"""
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(512, activation='relu'),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(7, activation='softmax')
        ])
        
        model.compile(optimizer='adam',
                     loss='categorical_crossentropy',
                     metrics=['accuracy'])
        
        # Initialize with random weights (in production, load pre-trained weights)
        model.build(input_shape=(None, 48, 48, 1))
        return model
    
    def _load_face_cascade(self):
        """Load OpenCV face cascade classifier"""
        try:
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
            if self.face_cascade.empty():
                raise Exception("Failed to load face cascade")
            self.logger.info("Face cascade loaded successfully")
        except Exception as e:
            self.logger.error(f"Error loading face cascade: {e}")
            self.face_cascade = None
    
    def preprocess_face(self, face_roi: np.ndarray) -> np.ndarray:
        """Preprocess face region for emotion detection"""
        try:
            # Resize to 48x48 (standard for emotion detection)
            face_resized = cv2.resize(face_roi, (48, 48))
            
            # Convert to grayscale if needed
            if len(face_resized.shape) == 3:
                face_gray = cv2.cvtColor(face_resized, cv2.COLOR_BGR2GRAY)
            else:
                face_gray = face_resized
            
            # Normalize pixel values
            face_normalized = face_gray.astype('float32') / 255.0
            
            # Reshape for model input
            face_reshaped = face_normalized.reshape(1, 48, 48, 1)
            
            return face_reshaped
        except Exception as e:
            self.logger.error(f"Error preprocessing face: {e}")
            return None
    
    def detect_emotion(self, face_roi: np.ndarray) -> Tuple[str, float]:
        """Detect emotion from face region"""
        try:
            if self.model is None:
                return "Neutral", 0.5
            
            # Preprocess face
            processed_face = self.preprocess_face(face_roi)
            if processed_face is None:
                return "Neutral", 0.0
            
            # Predict emotion
            predictions = self.model.predict(processed_face, verbose=0)
            emotion_index = np.argmax(predictions[0])
            confidence = float(predictions[0][emotion_index])
            
            emotion = self.emotion_labels[emotion_index]
            return emotion, confidence
            
        except Exception as e:
            self.logger.error(f"Error detecting emotion: {e}")
            return "Neutral", 0.0
    
    def process_frame(self, frame: np.ndarray) -> Dict:
        """Process a single frame for emotion detection"""
        try:
            result = {
                'emotion': 'Neutral',
                'confidence': 0.0,
                'face_detected': False,
                'face_bbox': None,
                'frame': frame.copy()
            }
            
            if self.face_cascade is None:
                return result
            
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray, 
                scaleFactor=1.1, 
                minNeighbors=5, 
                minSize=(30, 30)
            )
            
            if len(faces) > 0:
                # Use the largest face
                largest_face = max(faces, key=lambda x: x[2] * x[3])
                x, y, w, h = largest_face
                
                # Extract face ROI
                face_roi = gray[y:y+h, x:x+w]
                
                # Detect emotion
                emotion, confidence = self.detect_emotion(face_roi)
                
                result.update({
                    'emotion': emotion,
                    'confidence': confidence,
                    'face_detected': True,
                    'face_bbox': largest_face
                })
                
                # Draw bounding box and emotion on frame
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, f"{emotion}: {confidence:.2f}", 
                           (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing frame: {e}")
            return {
                'emotion': 'Neutral',
                'confidence': 0.0,
                'face_detected': False,
                'face_bbox': None,
                'frame': frame
            }
    
    def start_camera(self, camera_index: int = 0) -> bool:
        """Start camera capture"""
        try:
            self.cap = cv2.VideoCapture(camera_index)
            if not self.cap.isOpened():
                self.logger.error("Failed to open camera")
                return False
            
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            self.is_running = True
            
            # Start processing thread
            self.processing_thread = threading.Thread(target=self._camera_loop, daemon=True)
            self.processing_thread.start()
            
            self.logger.info("Camera started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error starting camera: {e}")
            return False
    
    def _camera_loop(self):
        """Main camera processing loop"""
        while self.is_running:
            try:
                ret, frame = self.cap.read()
                if not ret:
                    self.logger.warning("Failed to read frame from camera")
                    continue
                
                # Process frame
                result = self.process_frame(frame)
                
                # Update current state
                self.current_emotion = result['emotion']
                self.current_confidence = result['confidence']
                self.face_detected = result['face_detected']
                
                # Add to queues
                if not self.frame_queue.full():
                    self.frame_queue.put(result['frame'])
                
                if not self.emotion_queue.full():
                    self.emotion_queue.put({
                        'emotion': result['emotion'],
                        'confidence': result['confidence'],
                        'face_detected': result['face_detected'],
                        'timestamp': time.time()
                    })
                
                # Small delay to prevent overwhelming the system
                time.sleep(0.033)  # ~30 FPS
                
            except Exception as e:
                self.logger.error(f"Error in camera loop: {e}")
                time.sleep(0.1)
    
    def get_latest_frame(self) -> Optional[np.ndarray]:
        """Get the latest processed frame"""
        try:
            if not self.frame_queue.empty():
                return self.frame_queue.get_nowait()
            return None
        except queue.Empty:
            return None
    
    def get_emotion_history(self, max_items: int = 10) -> List[Dict]:
        """Get recent emotion detection history"""
        try:
            emotions = []
            temp_queue = queue.Queue()
            
            # Extract items from emotion queue
            while not self.emotion_queue.empty():
                item = self.emotion_queue.get_nowait()
                emotions.append(item)
                temp_queue.put(item)
            
            # Put items back
            while not temp_queue.empty():
                self.emotion_queue.put(temp_queue.get_nowait())
            
            return emotions[-max_items:] if emotions else []
            
        except Exception as e:
            self.logger.error(f"Error getting emotion history: {e}")
            return []
    
    def get_current_state(self) -> Dict:
        """Get current emotion detection state"""
        return {
            'emotion': self.current_emotion,
            'confidence': self.current_confidence,
            'face_detected': self.face_detected,
            'is_running': self.is_running
        }
    
    def stop_camera(self):
        """Stop camera capture"""
        try:
            self.is_running = False
            if hasattr(self, 'cap'):
                self.cap.release()
            
            if hasattr(self, 'processing_thread'):
                self.processing_thread.join(timeout=2)
            
            self.logger.info("Camera stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Error stopping camera: {e}")
    
    def get_emotion_statistics(self) -> Dict:
        """Get emotion detection statistics"""
        try:
            emotions = self.get_emotion_history(max_items=100)
            if not emotions:
                return {}
            
            emotion_counts = {}
            total_confidence = 0
            
            for item in emotions:
                emotion = item['emotion']
                confidence = item['confidence']
                
                if emotion not in emotion_counts:
                    emotion_counts[emotion] = {'count': 0, 'total_confidence': 0}
                
                emotion_counts[emotion]['count'] += 1
                emotion_counts[emotion]['total_confidence'] += confidence
                total_confidence += confidence
            
            # Calculate averages
            for emotion in emotion_counts:
                count = emotion_counts[emotion]['count']
                emotion_counts[emotion]['avg_confidence'] = emotion_counts[emotion]['total_confidence'] / count
                emotion_counts[emotion]['percentage'] = (count / len(emotions)) * 100
            
            return emotion_counts
            
        except Exception as e:
            self.logger.error(f"Error calculating emotion statistics: {e}")
            return {}
    
    def calibrate_detection(self, calibration_frames: int = 30) -> Dict:
        """Calibrate emotion detection for current user"""
        try:
            self.logger.info(f"Starting calibration with {calibration_frames} frames")
            
            calibration_data = []
            start_time = time.time()
            
            while len(calibration_data) < calibration_frames and self.is_running:
                emotions = self.get_emotion_history(max_items=1)
                if emotions:
                    calibration_data.append(emotions[0])
                time.sleep(0.1)
            
            if calibration_data:
                # Calculate baseline emotions
                emotion_counts = {}
                total_confidence = 0
                
                for item in calibration_data:
                    emotion = item['emotion']
                    confidence = item['confidence']
                    
                    if emotion not in emotion_counts:
                        emotion_counts[emotion] = 0
                    emotion_counts[emotion] += 1
                    total_confidence += confidence
                
                avg_confidence = total_confidence / len(calibration_data)
                dominant_emotion = max(emotion_counts, key=emotion_counts.get)
                
                calibration_result = {
                    'dominant_emotion': dominant_emotion,
                    'avg_confidence': avg_confidence,
                    'emotion_distribution': emotion_counts,
                    'calibration_frames': len(calibration_data),
                    'duration': time.time() - start_time
                }
                
                self.logger.info(f"Calibration completed: {calibration_result}")
                return calibration_result
            
            return {}
            
        except Exception as e:
            self.logger.error(f"Error during calibration: {e}")
            return {}
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        self.stop_camera()
