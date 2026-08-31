import re
from datetime import datetime
from task_manager import TaskManager
from voice_handler import VoiceHandler
import requests
import logging

logger = logging.getLogger(__name__)

class CommandProcessor:
    def __init__(self):
        """Initialize command processor"""
        self.task_manager = TaskManager()
        self.voice_handler = VoiceHandler()
    
    def process_command(self, user_input):
        """Process user voice command and execute appropriate action"""
        try:
            # Task management commands
            if "add task" in user_input or "create task" in user_input:
                self.handle_add_task(user_input)
            
            elif "list tasks" in user_input or "show tasks" in user_input or "my tasks" in user_input:
                self.handle_list_tasks()
            
            elif "complete task" in user_input or "done task" in user_input:
                self.handle_complete_task(user_input)
            
            elif "delete task" in user_input or "remove task" in user_input:
                self.handle_delete_task(user_input)
            
            elif "task summary" in user_input:
                summary = self.task_manager.get_task_summary()
                self.voice_handler.speak(summary)
            
            # Information commands
            elif "what time" in user_input or "current time" in user_input:
                self.handle_time()
            
            elif "what date" in user_input or "current date" in user_input:
                self.handle_date()
            
            elif "weather" in user_input:
                self.handle_weather()
            
            elif "help" in user_input or "commands" in user_input:
                self.handle_help()
            
            else:
                self.voice_handler.speak("I didn't recognize that command. Say 'help' for available commands.")
        
        except Exception as e:
            logger.error(f"Error processing command: {e}")
            self.voice_handler.speak("An error occurred processing your command.")
    
    def handle_add_task(self, user_input):
        """Handle adding a new task"""
        # Extract task title from input
        # Pattern: "add task [title]"
        match = re.search(r'(?:add|create)\s+task\s+(.+?)(?:\s+for|$)', user_input)
        
        if match:
            title = match.group(1).strip()
            
            # Determine category
            category = "personal"
            if "work" in user_input:
                category = "work"
            elif "shopping" in user_input:
                category = "shopping"
            elif "health" in user_input:
                category = "health"
            
            task = self.task_manager.add_task(title, category)
            self.voice_handler.speak(f"Task '{title}' added to your {category} tasks.")
        else:
            self.voice_handler.speak("What task would you like to add?")
    
    def handle_list_tasks(self):
        """Handle listing tasks"""
        tasks = self.task_manager.get_pending_tasks()
        
        if not tasks:
            self.voice_handler.speak("You have no pending tasks.")
            return
        
        response = "Here are your pending tasks: "
        for i, task in enumerate(tasks, 1):
            response += f"{i}. {task['title']}. "
        
        self.voice_handler.speak(response)
    
    def handle_complete_task(self, user_input):
        """Handle marking a task as complete"""
        # Extract task number or title
        match = re.search(r'(?:complete|done)\s+(?:task\s+)?(\d+|.+)', user_input)
        
        if match:
            task_identifier = match.group(1).strip()
            
            # Try to parse as number
            try:
                task_num = int(task_identifier)
                tasks = self.task_manager.get_pending_tasks()
                if task_num <= len(tasks):
                    task = tasks[task_num - 1]
                    self.task_manager.complete_task(task['id'])
                    self.voice_handler.speak(f"Task '{task['title']}' marked as complete.")
                else:
                    self.voice_handler.speak("Task number out of range.")
            except ValueError:
                # Search by title
                tasks = self.task_manager.get_pending_tasks()
                for task in tasks:
                    if task_identifier.lower() in task['title'].lower():
                        self.task_manager.complete_task(task['id'])
                        self.voice_handler.speak(f"Task '{task['title']}' marked as complete.")
                        return
                self.voice_handler.speak("Task not found.")
        else:
            self.voice_handler.speak("Which task would you like to complete?")
    
    def handle_delete_task(self, user_input):
        """Handle deleting a task"""
        match = re.search(r'(?:delete|remove)\s+(?:task\s+)?(\d+|.+)', user_input)
        
        if match:
            task_identifier = match.group(1).strip()
            
            try:
                task_num = int(task_identifier)
                tasks = self.task_manager.get_all_tasks()
                if task_num <= len(tasks):
                    task = tasks[task_num - 1]
                    self.task_manager.delete_task(task['id'])
                    self.voice_handler.speak(f"Task '{task['title']}' deleted.")
            except ValueError:
                tasks = self.task_manager.get_all_tasks()
                for task in tasks:
                    if task_identifier.lower() in task['title'].lower():
                        self.task_manager.delete_task(task['id'])
                        self.voice_handler.speak(f"Task '{task['title']}' deleted.")
                        return
                self.voice_handler.speak("Task not found.")
    
    def handle_time(self):
        """Get and announce current time"""
        current_time = datetime.now().strftime("%I:%M %p")
        self.voice_handler.speak(f"The current time is {current_time}.")
    
    def handle_date(self):
        """Get and announce current date"""
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        self.voice_handler.speak(f"Today is {current_date}.")
    
    def handle_weather(self):
        """Get weather information"""
        try:
            response = requests.get("https://wttr.in/?format=3", timeout=5)
            if response.status_code == 200:
                self.voice_handler.speak(f"Weather: {response.text}")
            else:
                self.voice_handler.speak("Unable to fetch weather information.")
        except Exception as e:
            logger.error(f"Error fetching weather: {e}")
            self.voice_handler.speak("Unable to fetch weather information.")
    
    def handle_help(self):
        """List available commands"""
        help_text = "Available commands: Add task, List tasks, Complete task, Delete task, What time, What date, Weather, and Help."
        self.voice_handler.speak(help_text)