#!/usr/bin/env python3
"""
JARVIS AI Assistant - Main Entry Point
A voice-controlled AI assistant for managing daily tasks
"""

import logging
import threading
from voice_handler import VoiceHandler
from command_processor import CommandProcessor
from config import CONFIG
import schedule
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(CONFIG['LOG_FILE']),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class JarvisAI:
    def __init__(self):
        """Initialize JARVIS AI Assistant"""
        self.voice_handler = VoiceHandler()
        self.command_processor = CommandProcessor()
        self.running = True
    
    def greet(self):
        """Greet the user"""
        greeting = "Hello, I'm JARVIS. Your personal AI assistant. I'm here to help you manage your daily tasks and provide information. Say 'help' to see what I can do."
        self.voice_handler.speak(greeting)
        logger.info("JARVIS AI initialized and greeted user")
    
    def main_loop(self):
        """Main listening and command processing loop"""
        self.greet()
        
        while self.running:
            try:
                # Wait for wake word
                self.voice_handler.wait_for_wake_word()
                
                # Listen for command
                user_input = self.voice_handler.listen()
                
                if user_input:
                    logger.info(f"User command: {user_input}")
                    self.command_processor.process_command(user_input)
                
            except KeyboardInterrupt:
                logger.info("Keyboard interrupt received")
                self.shutdown()
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                continue
    
    def shutdown(self):
        """Gracefully shutdown JARVIS"""
        self.running = False
        self.voice_handler.speak("Goodbye! Have a great day.")
        logger.info("JARVIS AI shutdown")

def run_web_ui():
    """Run web UI in separate thread"""
    try:
        from flask import Flask, render_template, jsonify, request
        from task_manager import TaskManager
        
        app = Flask(__name__)
        task_manager = TaskManager()
        
        @app.route('/')
        def index():
            return jsonify({"status": "JARVIS API running"})
        
        @app.route('/api/tasks', methods=['GET'])
        def get_tasks():
            return jsonify(task_manager.get_all_tasks())
        
        @app.route('/api/tasks', methods=['POST'])
        def add_task():
            data = request.json
            task = task_manager.add_task(
                data.get('title'),
                data.get('category', 'personal'),
                data.get('priority', 'normal')
            )
            return jsonify(task), 201
        
        @app.route('/api/tasks/<int:task_id>/complete', methods=['POST'])
        def complete_task(task_id):
            task = task_manager.complete_task(task_id)
            return jsonify(task) if task else jsonify({"error": "Task not found"}), 404
        
        @app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
        def delete_task(task_id):
            task_manager.delete_task(task_id)
            return jsonify({"status": "deleted"}), 200
        
        logger.info(f"Starting Flask web UI on port {CONFIG['FLASK_PORT']}")
        app.run(host='0.0.0.0', port=CONFIG['FLASK_PORT'], debug=False)
    
    except Exception as e:
        logger.error(f"Error running web UI: {e}")

if __name__ == "__main__":
    jarvis = JarvisAI()
    
    # Start web UI in background thread if enabled
    if CONFIG['ENABLE_WEB_UI']:
        web_thread = threading.Thread(target=run_web_ui, daemon=True)
        web_thread.start()
        logger.info("Web UI thread started")
    
    # Run main JARVIS loop
    try:
        jarvis.main_loop()
    except Exception as e:
        logger.critical(f"Critical error: {e}")
        jarvis.shutdown()