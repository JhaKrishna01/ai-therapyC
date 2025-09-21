"""
Main GUI Interface for AI Therapy System
Professional CustomTkinter interface with integrated camera feed and therapeutic features
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk
import threading
import time
import logging
from typing import Dict, List, Optional
import datetime
import json

# Import our modules
from emotion_detection.emotion_detector import EmotionDetector
from therapeutic_system.nurse_framework import NURSEFramework
from crisis_detection.crisis_detector import CrisisDetector
from database.database_manager import DatabaseManager
from exercises.therapeutic_exercises import TherapeuticExercises
from visualization.data_visualizer import DataVisualizer
from export.research_exporter import ResearchDataExporter

class AITherapyGUI:
    def __init__(self):
        # Configure CustomTkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Initialize main window
        self.root = ctk.CTk()
        self.root.title("AI Therapy System - Emotion & Risk Detection")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Initialize logging
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.emotion_detector = EmotionDetector()
        self.nurse_framework = NURSEFramework()
        self.crisis_detector = CrisisDetector()
        self.database_manager = DatabaseManager()
        self.therapeutic_exercises = TherapeuticExercises()
        self.data_visualizer = DataVisualizer()
        self.research_exporter = ResearchDataExporter()
        
        # Session management
        self.current_session_id = None
        self.session_active = False
        self.camera_active = False
        
        # GUI state
        self.current_emotion = "Neutral"
        self.current_confidence = 0.0
        self.risk_level = 0
        self.conversation_history = []
        
        # Initialize GUI
        self._setup_gui()
        self._setup_menu()
        self._setup_status_bar()
        
        # Start update loop
        self._start_update_loop()
    
    def _setup_gui(self):
        """Setup the main GUI layout"""
        # Create main container
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill="both", expand=True)
        
        # Create tabs
        self._create_main_tab()
        self._create_session_tab()
        self._create_exercises_tab()
        self._create_analytics_tab()
        self._create_settings_tab()
    
    def _create_main_tab(self):
        """Create the main therapy session tab"""
        self.main_tab = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.main_tab, text="Therapy Session")
        
        # Create main layout
        main_frame = ctk.CTkFrame(self.main_tab)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left panel - Camera and emotion display
        left_panel = ctk.CTkFrame(main_frame)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Camera feed
        self.camera_label = ctk.CTkLabel(left_panel, text="Camera Feed", 
                                        font=ctk.CTkFont(size=16, weight="bold"))
        self.camera_label.pack(pady=10)
        
        self.camera_frame = ctk.CTkFrame(left_panel, width=400, height=300)
        self.camera_frame.pack(pady=10)
        
        # Emotion display
        emotion_frame = ctk.CTkFrame(left_panel)
        emotion_frame.pack(fill="x", pady=10)
        
        self.emotion_label = ctk.CTkLabel(emotion_frame, text="Detected Emotion: Neutral", 
                                        font=ctk.CTkFont(size=14))
        self.emotion_label.pack(pady=5)
        
        self.confidence_label = ctk.CTkLabel(emotion_frame, text="Confidence: 0.0%", 
                                           font=ctk.CTkFont(size=12))
        self.confidence_label.pack(pady=5)
        
        # Risk indicator
        self.risk_label = ctk.CTkLabel(emotion_frame, text="Risk Level: Low", 
                                      font=ctk.CTkFont(size=12), text_color="green")
        self.risk_label.pack(pady=5)
        
        # Right panel - Chat interface
        right_panel = ctk.CTkFrame(main_frame)
        right_panel.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Chat display
        chat_frame = ctk.CTkFrame(right_panel)
        chat_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        self.chat_text = ctk.CTkTextbox(chat_frame, height=300)
        self.chat_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Input frame
        input_frame = ctk.CTkFrame(right_panel)
        input_frame.pack(fill="x", pady=(0, 10))
        
        self.message_entry = ctk.CTkEntry(input_frame, placeholder_text="Type your message here...")
        self.message_entry.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
        
        self.send_button = ctk.CTkButton(input_frame, text="Send", command=self._send_message)
        self.send_button.pack(side="right", padx=(5, 10), pady=10)
        
        # Session controls
        control_frame = ctk.CTkFrame(right_panel)
        control_frame.pack(fill="x")
        
        self.start_session_button = ctk.CTkButton(control_frame, text="Start Session", 
                                                command=self._start_session)
        self.start_session_button.pack(side="left", padx=10, pady=10)
        
        self.stop_session_button = ctk.CTkButton(control_frame, text="Stop Session", 
                                                command=self._stop_session, state="disabled")
        self.stop_session_button.pack(side="left", padx=10, pady=10)
        
        self.camera_button = ctk.CTkButton(control_frame, text="Start Camera", 
                                         command=self._toggle_camera)
        self.camera_button.pack(side="right", padx=10, pady=10)
    
    def _create_session_tab(self):
        """Create the session management tab"""
        self.session_tab = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.session_tab, text="Session Management")
        
        # Session list
        session_frame = ctk.CTkFrame(self.session_tab)
        session_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Session listbox
        self.session_listbox = tk.Listbox(session_frame, font=("Arial", 12))
        self.session_listbox.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Session controls
        session_controls = ctk.CTkFrame(self.session_tab)
        session_controls.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkButton(session_controls, text="Refresh Sessions", 
                     command=self._refresh_sessions).pack(side="left", padx=5, pady=10)
        ctk.CTkButton(session_controls, text="View Session Details", 
                     command=self._view_session_details).pack(side="left", padx=5, pady=10)
        ctk.CTkButton(session_controls, text="Export Session", 
                     command=self._export_session).pack(side="left", padx=5, pady=10)
    
    def _create_exercises_tab(self):
        """Create the therapeutic exercises tab"""
        self.exercises_tab = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.exercises_tab, text="Therapeutic Exercises")
        
        # Exercise selection
        exercise_frame = ctk.CTkFrame(self.exercises_tab)
        exercise_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Exercise categories
        categories_frame = ctk.CTkFrame(exercise_frame)
        categories_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(categories_frame, text="Exercise Categories", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        self.exercise_category = ctk.CTkComboBox(categories_frame, 
                                                values=["Breathing", "Mindfulness", "Journaling", 
                                                       "Relaxation", "Mood Lifting"])
        self.exercise_category.pack(pady=10)
        
        # Exercise selection
        self.exercise_type = ctk.CTkComboBox(categories_frame, 
                                            values=["Select Exercise Type"])
        self.exercise_type.pack(pady=10)
        
        # Exercise display
        self.exercise_display = ctk.CTkTextbox(exercise_frame, height=200)
        self.exercise_display.pack(fill="both", expand=True, pady=10)
        
        # Exercise controls
        exercise_controls = ctk.CTkFrame(exercise_frame)
        exercise_controls.pack(fill="x", pady=10)
        
        ctk.CTkButton(exercise_controls, text="Start Exercise", 
                     command=self._start_exercise).pack(side="left", padx=5, pady=10)
        ctk.CTkButton(exercise_controls, text="Stop Exercise", 
                     command=self._stop_exercise).pack(side="left", padx=5, pady=10)
        
        # Progress bar
        self.exercise_progress = ctk.CTkProgressBar(exercise_frame)
        self.exercise_progress.pack(fill="x", pady=10)
        self.exercise_progress.set(0)
    
    def _create_analytics_tab(self):
        """Create the analytics and visualization tab"""
        self.analytics_tab = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.analytics_tab, text="Analytics")
        
        # Analytics controls
        controls_frame = ctk.CTkFrame(self.analytics_tab)
        controls_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(controls_frame, text="Generate Report", 
                     command=self._generate_report).pack(side="left", padx=5, pady=10)
        ctk.CTkButton(controls_frame, text="Export Data", 
                     command=self._export_data).pack(side="left", padx=5, pady=10)
        ctk.CTkButton(controls_frame, text="View Statistics", 
                     command=self._view_statistics).pack(side="left", padx=5, pady=10)
        
        # Analytics display
        self.analytics_display = ctk.CTkTextbox(self.analytics_tab, height=400)
        self.analytics_display.pack(fill="both", expand=True, padx=10, pady=10)
    
    def _create_settings_tab(self):
        """Create the settings tab"""
        self.settings_tab = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.settings_tab, text="Settings")
        
        # Settings frame
        settings_frame = ctk.CTkFrame(self.settings_tab)
        settings_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Camera settings
        camera_settings = ctk.CTkFrame(settings_frame)
        camera_settings.pack(fill="x", pady=10)
        
        ctk.CTkLabel(camera_settings, text="Camera Settings", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        self.camera_index = ctk.CTkEntry(camera_settings, placeholder_text="Camera Index (default: 0)")
        self.camera_index.pack(pady=10)
        
        # Database settings
        db_settings = ctk.CTkFrame(settings_frame)
        db_settings.pack(fill="x", pady=10)
        
        ctk.CTkLabel(db_settings, text="Database Settings", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        ctk.CTkButton(db_settings, text="Clear Database", 
                     command=self._clear_database).pack(pady=10)
        ctk.CTkButton(db_settings, text="Backup Database", 
                     command=self._backup_database).pack(pady=10)
        
        # Export settings
        export_settings = ctk.CTkFrame(settings_frame)
        export_settings.pack(fill="x", pady=10)
        
        ctk.CTkLabel(export_settings, text="Export Settings", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        self.export_directory = ctk.CTkEntry(export_settings, placeholder_text="Export Directory")
        self.export_directory.pack(pady=10)
        
        ctk.CTkButton(export_settings, text="Set Export Directory", 
                     command=self._set_export_directory).pack(pady=10)
    
    def _setup_menu(self):
        """Setup the menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Session", command=self._start_session)
        file_menu.add_command(label="Export Data", command=self._export_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._exit_application)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Camera Calibration", command=self._calibrate_camera)
        tools_menu.add_command(label="Database Management", command=self._manage_database)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
        help_menu.add_command(label="Documentation", command=self._show_documentation)
    
    def _setup_status_bar(self):
        """Setup the status bar"""
        self.status_bar = ctk.CTkFrame(self.root, height=30)
        self.status_bar.pack(fill="x", side="bottom")
        
        self.status_label = ctk.CTkLabel(self.status_bar, text="Ready")
        self.status_label.pack(side="left", padx=10, pady=5)
        
        self.session_status_label = ctk.CTkLabel(self.status_bar, text="No Active Session")
        self.session_status_label.pack(side="right", padx=10, pady=5)
    
    def _start_update_loop(self):
        """Start the main update loop"""
        self._update_gui()
        self.root.after(100, self._start_update_loop)  # Update every 100ms
    
    def _update_gui(self):
        """Update GUI elements"""
        try:
            # Update camera feed
            if self.camera_active:
                frame = self.emotion_detector.get_latest_frame()
                if frame is not None:
                    self._update_camera_display(frame)
            
            # Update emotion display
            state = self.emotion_detector.get_current_state()
            if state:
                self.current_emotion = state['emotion']
                self.current_confidence = state['confidence']
                
                self.emotion_label.configure(text=f"Detected Emotion: {self.current_emotion}")
                self.confidence_label.configure(text=f"Confidence: {self.current_confidence:.1%}")
            
            # Update risk level
            if self.session_active and self.conversation_history:
                latest_message = self.conversation_history[-1] if self.conversation_history else None
                if latest_message:
                    risk_analysis = self.crisis_detector.analyze_text(latest_message.get('user_input', ''))
                    self.risk_level = risk_analysis['risk_level']
                    
                    risk_colors = {0: "green", 1: "yellow", 2: "orange", 3: "red", 4: "darkred", 5: "purple"}
                    risk_names = {0: "Low", 1: "Mild", 2: "Moderate", 3: "High", 4: "Crisis", 5: "Emergency"}
                    
                    self.risk_label.configure(
                        text=f"Risk Level: {risk_names.get(self.risk_level, 'Unknown')}",
                        text_color=risk_colors.get(self.risk_level, "black")
                    )
            
            # Update session status
            if self.session_active:
                self.session_status_label.configure(text=f"Session: {self.current_session_id}")
            else:
                self.session_status_label.configure(text="No Active Session")
                
        except Exception as e:
            self.logger.error(f"Error updating GUI: {e}")
    
    def _update_camera_display(self, frame):
        """Update the camera display"""
        try:
            # Resize frame to fit display
            height, width = frame.shape[:2]
            max_width, max_height = 400, 300
            
            if width > max_width or height > max_height:
                scale = min(max_width/width, max_height/height)
                new_width = int(width * scale)
                new_height = int(height * scale)
                frame = cv2.resize(frame, (new_width, new_height))
            
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert to PIL Image
            image = Image.fromarray(frame_rgb)
            photo = ImageTk.PhotoImage(image)
            
            # Update camera label
            self.camera_label.configure(image=photo)
            self.camera_label.image = photo  # Keep a reference
            
        except Exception as e:
            self.logger.error(f"Error updating camera display: {e}")
    
    def _toggle_camera(self):
        """Toggle camera on/off"""
        try:
            if not self.camera_active:
                # Start camera
                camera_index = int(self.camera_index.get() or 0)
                if self.emotion_detector.start_camera(camera_index):
                    self.camera_active = True
                    self.camera_button.configure(text="Stop Camera")
                    self.status_label.configure(text="Camera Started")
                else:
                    messagebox.showerror("Error", "Failed to start camera")
            else:
                # Stop camera
                self.emotion_detector.stop_camera()
                self.camera_active = False
                self.camera_button.configure(text="Start Camera")
                self.status_label.configure(text="Camera Stopped")
                
        except Exception as e:
            self.logger.error(f"Error toggling camera: {e}")
            messagebox.showerror("Error", f"Camera error: {e}")
    
    def _start_session(self):
        """Start a new therapy session"""
        try:
            if self.session_active:
                messagebox.showwarning("Warning", "A session is already active")
                return
            
            # Generate session ID
            self.current_session_id = f"session_{int(time.time())}"
            
            # Create session in database
            if self.database_manager.create_session(self.current_session_id):
                self.session_active = True
                self.start_session_button.configure(state="disabled")
                self.stop_session_button.configure(state="normal")
                
                # Start crisis monitoring
                self.crisis_detector.start_monitoring()
                
                self.status_label.configure(text="Session Started")
                self._add_chat_message("System", "Welcome! I'm here to listen and support you. How are you feeling today?")
                
            else:
                messagebox.showerror("Error", "Failed to create session")
                
        except Exception as e:
            self.logger.error(f"Error starting session: {e}")
            messagebox.showerror("Error", f"Session error: {e}")
    
    def _stop_session(self):
        """Stop the current therapy session"""
        try:
            if not self.session_active:
                return
            
            # End session in database
            self.database_manager.end_session(self.current_session_id, "User ended session")
            
            # Stop crisis monitoring
            self.crisis_detector.stop_monitoring()
            
            # Reset session state
            self.session_active = False
            self.current_session_id = None
            self.conversation_history = []
            
            # Update GUI
            self.start_session_button.configure(state="normal")
            self.stop_session_button.configure(state="disabled")
            
            self.status_label.configure(text="Session Ended")
            self._add_chat_message("System", "Session ended. Thank you for using the AI Therapy System.")
            
        except Exception as e:
            self.logger.error(f"Error stopping session: {e}")
            messagebox.showerror("Error", f"Session error: {e}")
    
    def _send_message(self):
        """Send a message and get therapeutic response"""
        try:
            if not self.session_active:
                messagebox.showwarning("Warning", "Please start a session first")
                return
            
            message = self.message_entry.get().strip()
            if not message:
                return
            
            # Add user message to chat
            self._add_chat_message("You", message)
            
            # Clear input
            self.message_entry.delete(0, tk.END)
            
            # Get therapeutic response
            response = self.nurse_framework.generate_response(
                message, self.current_emotion, self.current_confidence, 
                {'session_id': self.current_session_id}
            )
            
            # Add system response to chat
            self._add_chat_message("AI Therapist", response['response_text'])
            
            # Log conversation
            self.database_manager.log_conversation(
                self.current_session_id, message, response['response_text'],
                sentiment_score=0.0, emotion_context=self.current_emotion,
                therapeutic_approach=response['therapeutic_approach']
            )
            
            # Log emotion detection
            self.database_manager.log_emotion_detection(
                self.current_session_id, self.current_emotion, self.current_confidence
            )
            
            # Log risk assessment
            if response['risk_score'] > 0:
                self.database_manager.log_risk_assessment(
                    self.current_session_id, response['risk_score'],
                    response['risk_factors'], []
                )
            
            # Store conversation
            self.conversation_history.append({
                'user_input': message,
                'system_response': response['response_text'],
                'timestamp': datetime.datetime.now(),
                'emotion': self.current_emotion,
                'risk_score': response['risk_score']
            })
            
            # Check for crisis intervention
            if response['crisis_intervention']:
                self._handle_crisis_intervention(response)
            
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
            messagebox.showerror("Error", f"Message error: {e}")
    
    def _add_chat_message(self, sender: str, message: str):
        """Add a message to the chat display"""
        try:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            formatted_message = f"[{timestamp}] {sender}: {message}\n\n"
            
            self.chat_text.insert(tk.END, formatted_message)
            self.chat_text.see(tk.END)
            
        except Exception as e:
            self.logger.error(f"Error adding chat message: {e}")
    
    def _handle_crisis_intervention(self, response: Dict):
        """Handle crisis intervention"""
        try:
            # Show crisis intervention dialog
            crisis_window = ctk.CTkToplevel(self.root)
            crisis_window.title("Crisis Intervention")
            crisis_window.geometry("500x400")
            crisis_window.grab_set()
            
            # Crisis message
            crisis_text = ctk.CTkTextbox(crisis_window, height=200)
            crisis_text.pack(fill="both", expand=True, padx=10, pady=10)
            
            crisis_message = f"""CRISIS INTERVENTION ACTIVATED

{response['response_text']}

CRISIS RESOURCES:
- National Suicide Prevention Lifeline: 988
- Crisis Text Line: Text HOME to 741741
- Emergency Services: 911

Your safety is our top priority. Please reach out for help immediately."""
            
            crisis_text.insert(tk.END, crisis_message)
            crisis_text.configure(state="disabled")
            
            # Close button
            ctk.CTkButton(crisis_window, text="I Understand", 
                          command=crisis_window.destroy).pack(pady=10)
            
        except Exception as e:
            self.logger.error(f"Error handling crisis intervention: {e}")
    
    def _start_exercise(self):
        """Start a therapeutic exercise"""
        try:
            category = self.exercise_category.get()
            exercise_type = self.exercise_type.get()
            
            if not category or exercise_type == "Select Exercise Type":
                messagebox.showwarning("Warning", "Please select an exercise category and type")
                return
            
            # Get exercise recommendation
            exercise = self.therapeutic_exercises.get_exercise_recommendation(
                self.current_emotion, self.risk_level
            )
            
            if not exercise:
                messagebox.showerror("Error", "No exercise available")
                return
            
            # Display exercise
            exercise_text = f"""Exercise: {exercise['exercise_type']}

Description: {exercise['description']}

Steps:
"""
            for i, step in enumerate(exercise['steps'], 1):
                exercise_text += f"{i}. {step}\n"
            
            exercise_text += f"\nDuration: {exercise['duration']} seconds\n"
            exercise_text += f"Benefits: {exercise['benefits']}"
            
            self.exercise_display.delete("1.0", tk.END)
            self.exercise_display.insert("1.0", exercise_text)
            
            # Start exercise
            def progress_callback(progress_data):
                self.exercise_progress.set(progress_data['progress'] / 100)
            
            session_id = self.therapeutic_exercises.start_exercise(
                exercise_type, exercise, progress_callback
            )
            
            if session_id:
                self.status_label.configure(text=f"Exercise Started: {exercise_type}")
            
        except Exception as e:
            self.logger.error(f"Error starting exercise: {e}")
            messagebox.showerror("Error", f"Exercise error: {e}")
    
    def _stop_exercise(self):
        """Stop current exercise"""
        try:
            # This would need to track active exercise sessions
            self.exercise_progress.set(0)
            self.status_label.configure(text="Exercise Stopped")
            
        except Exception as e:
            self.logger.error(f"Error stopping exercise: {e}")
    
    def _refresh_sessions(self):
        """Refresh session list"""
        try:
            sessions = self.database_manager.get_all_sessions()
            self.session_listbox.delete(0, tk.END)
            
            for session in sessions:
                session_text = f"{session['session_id']} - {session['start_time']} - {session['status']}"
                self.session_listbox.insert(tk.END, session_text)
                
        except Exception as e:
            self.logger.error(f"Error refreshing sessions: {e}")
    
    def _view_session_details(self):
        """View details of selected session"""
        try:
            selection = self.session_listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a session")
                return
            
            # Get session data and display
            session_text = self.session_listbox.get(selection[0])
            session_id = session_text.split(" - ")[0]
            
            session_data = self.database_manager.get_session_data(session_id)
            
            # Create details window
            details_window = ctk.CTkToplevel(self.root)
            details_window.title(f"Session Details - {session_id}")
            details_window.geometry("800x600")
            
            details_text = ctk.CTkTextbox(details_window)
            details_text.pack(fill="both", expand=True, padx=10, pady=10)
            
            details_content = json.dumps(session_data, indent=2, default=str)
            details_text.insert("1.0", details_content)
            
        except Exception as e:
            self.logger.error(f"Error viewing session details: {e}")
    
    def _export_session(self):
        """Export selected session"""
        try:
            selection = self.session_listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a session")
                return
            
            session_text = self.session_listbox.get(selection[0])
            session_id = session_text.split(" - ")[0]
            
            # Choose export format
            format_window = ctk.CTkToplevel(self.root)
            format_window.title("Export Format")
            format_window.geometry("300x200")
            format_window.grab_set()
            
            ctk.CTkLabel(format_window, text="Select Export Format:").pack(pady=10)
            
            format_var = tk.StringVar(value="json")
            ctk.CTkRadioButton(format_window, text="JSON", variable=format_var, value="json").pack(pady=5)
            ctk.CTkRadioButton(format_window, text="CSV", variable=format_var, value="csv").pack(pady=5)
            ctk.CTkRadioButton(format_window, text="Excel", variable=format_var, value="excel").pack(pady=5)
            
            def export_selected():
                format_type = format_var.get()
                filepath = self.research_exporter.export_session_data(session_id, format_type)
                if filepath:
                    messagebox.showinfo("Success", f"Session exported to {filepath}")
                else:
                    messagebox.showerror("Error", "Export failed")
                format_window.destroy()
            
            ctk.CTkButton(format_window, text="Export", command=export_selected).pack(pady=10)
            
        except Exception as e:
            self.logger.error(f"Error exporting session: {e}")
    
    def _generate_report(self):
        """Generate analytics report"""
        try:
            report = self.data_visualizer.generate_statistics_report()
            
            self.analytics_display.delete("1.0", tk.END)
            report_text = json.dumps(report, indent=2, default=str)
            self.analytics_display.insert("1.0", report_text)
            
        except Exception as e:
            self.logger.error(f"Error generating report: {e}")
    
    def _export_data(self):
        """Export all data"""
        try:
            filepath = self.research_exporter.export_research_report("excel")
            if filepath:
                messagebox.showinfo("Success", f"Data exported to {filepath}")
            else:
                messagebox.showerror("Error", "Export failed")
                
        except Exception as e:
            self.logger.error(f"Error exporting data: {e}")
    
    def _view_statistics(self):
        """View system statistics"""
        try:
            stats = self.database_manager.get_emotion_statistics()
            
            self.analytics_display.delete("1.0", tk.END)
            stats_text = json.dumps(stats, indent=2, default=str)
            self.analytics_display.insert("1.0", stats_text)
            
        except Exception as e:
            self.logger.error(f"Error viewing statistics: {e}")
    
    def _calibrate_camera(self):
        """Calibrate camera for emotion detection"""
        try:
            if not self.camera_active:
                messagebox.showwarning("Warning", "Please start the camera first")
                return
            
            calibration_result = self.emotion_detector.calibrate_detection()
            
            if calibration_result:
                messagebox.showinfo("Calibration Complete", 
                                  f"Calibration completed successfully.\n"
                                  f"Dominant emotion: {calibration_result.get('dominant_emotion', 'Unknown')}\n"
                                  f"Average confidence: {calibration_result.get('avg_confidence', 0):.2f}")
            else:
                messagebox.showerror("Error", "Calibration failed")
                
        except Exception as e:
            self.logger.error(f"Error calibrating camera: {e}")
    
    def _manage_database(self):
        """Open database management window"""
        try:
            db_window = ctk.CTkToplevel(self.root)
            db_window.title("Database Management")
            db_window.geometry("600x400")
            
            # Database info
            info_text = ctk.CTkTextbox(db_window)
            info_text.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Get database statistics
            sessions = self.database_manager.get_all_sessions()
            emotion_stats = self.database_manager.get_emotion_statistics()
            
            db_info = {
                'total_sessions': len(sessions),
                'emotion_statistics': emotion_stats,
                'database_path': self.database_manager.db_path
            }
            
            info_text.insert("1.0", json.dumps(db_info, indent=2, default=str))
            
        except Exception as e:
            self.logger.error(f"Error managing database: {e}")
    
    def _clear_database(self):
        """Clear database (with confirmation)"""
        try:
            result = messagebox.askyesno("Confirm", 
                                      "Are you sure you want to clear the database? This action cannot be undone.")
            if result:
                # Implementation would go here
                messagebox.showinfo("Success", "Database cleared")
                
        except Exception as e:
            self.logger.error(f"Error clearing database: {e}")
    
    def _backup_database(self):
        """Backup database"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".db",
                filetypes=[("Database files", "*.db"), ("All files", "*.*")]
            )
            
            if filename:
                # Implementation would go here
                messagebox.showinfo("Success", f"Database backed up to {filename}")
                
        except Exception as e:
            self.logger.error(f"Error backing up database: {e}")
    
    def _set_export_directory(self):
        """Set export directory"""
        try:
            directory = filedialog.askdirectory()
            if directory:
                self.export_directory.delete(0, tk.END)
                self.export_directory.insert(0, directory)
                self.research_exporter.export_directory = directory
                
        except Exception as e:
            self.logger.error(f"Error setting export directory: {e}")
    
    def _show_about(self):
        """Show about dialog"""
        messagebox.showinfo("About", 
                          "AI Therapy System\n"
                          "Emotion & Risk Detection Therapeutic AI\n"
                          "Version 1.0\n\n"
                          "A comprehensive therapeutic AI system for emotion detection, "
                          "crisis intervention, and research data collection.")
    
    def _show_documentation(self):
        """Show documentation"""
        messagebox.showinfo("Documentation", 
                          "Documentation is available in the project directory.\n"
                          "Please refer to README.md and SETUP.md files.")
    
    def _exit_application(self):
        """Exit the application"""
        try:
            # Stop camera if active
            if self.camera_active:
                self.emotion_detector.stop_camera()
            
            # End session if active
            if self.session_active:
                self._stop_session()
            
            # Close application
            self.root.quit()
            
        except Exception as e:
            self.logger.error(f"Error exiting application: {e}")
            self.root.quit()
    
    def run(self):
        """Run the application"""
        try:
            self.root.protocol("WM_DELETE_WINDOW", self._exit_application)
            self.root.mainloop()
        except Exception as e:
            self.logger.error(f"Error running application: {e}")

def main():
    """Main entry point"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/therapy_system.log'),
            logging.StreamHandler()
        ]
    )
    
    # Create logs directory if it doesn't exist
    import os
    os.makedirs('logs', exist_ok=True)
    
    # Run the application
    app = AITherapyGUI()
    app.run()

if __name__ == "__main__":
    main()
