import os
from dotenv import load_dotenv

load_dotenv()

# Configuration Settings
CONFIG = {
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
    "WAKE_WORD": "jarvis",
    "VOICE_RATE": 150,
    "VOICE_VOLUME": 0.9,
    "LISTENING_TIMEOUT": 10,
    "LANGUAGE": "en-US",
    "TASK_STORAGE": "tasks.json",
    "LOG_FILE": "jarvis.log",
    "FLASK_PORT": 5000,
    "ENABLE_WEB_UI": True,
    "TIMEZONE": "UTC"
}

# Task Categories
TASK_CATEGORIES = {
    "work": "Work-related tasks",
    "personal": "Personal tasks",
    "health": "Health and fitness",
    "shopping": "Shopping list",
    "reminders": "Reminders",
    "entertainment": "Entertainment"
}

# Supported Commands
SUPPORTED_COMMANDS = {
    "add task": "Add a new task",
    "list tasks": "Show all tasks",
    "delete task": "Remove a task",
    "complete task": "Mark task as done",
    "get weather": "Get weather information",
    "get time": "Get current time",
    "get date": "Get current date",
    "set reminder": "Set a reminder",
    "play music": "Play music",
    "read news": "Read latest news",
    "search": "Search the web"
}