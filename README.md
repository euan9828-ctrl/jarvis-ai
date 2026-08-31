# 🤖 JARVIS AI Assistant

A sophisticated voice-controlled AI assistant that helps you manage daily tasks, provide information, and automate routines. JARVIS responds to voice commands and can manage your to-do lists, answer questions, and provide real-time information.

## ✨ Features

- 🎤 **Voice Recognition** - Speak naturally to JARVIS
- 🗣️ **Text-to-Speech** - JARVIS responds with natural speech
- 📋 **Task Management** - Add, complete, and track daily tasks
- ⏰ **Reminders & Scheduling** - Set reminders for important tasks
- 🌐 **Web Information** - Get weather, time, date, and more
- 📊 **Task Analytics** - Track task completion and productivity
- 🌐 **Web UI** - Manage tasks through a web interface
- 🔊 **Natural Dialogue** - Conversational interaction with AI

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Microphone and speakers
- Pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/jarvis-ai.git
   cd jarvis-ai
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your preferences
   ```

### Running JARVIS

**Start the assistant:**
```bash
python main.py
```

JARVIS will initialize and start listening for the wake word ("jarvis" by default).

**Access web UI:**
Open your browser and navigate to `http://localhost:5000`

## 🎙️ Voice Commands

### Task Management
- "Add task [task name]" - Create a new task
- "List tasks" - Show all pending tasks
- "Complete task [number/name]" - Mark task as done
- "Delete task [number/name]" - Remove a task
- "Task summary" - Get overview of your tasks

### Information
- "What time is it?" - Get current time
- "What's the date?" - Get current date
- "Weather" - Get weather information
- "Help" - List all available commands

### Examples
```
You: "Jarvis, add task buy groceries"
JARVIS: "Task 'buy groceries' added to your personal tasks."

You: "Jarvis, list tasks"
JARVIS: "Here are your pending tasks: 1. buy groceries. 2. call mom. 3. finish report."

You: "Jarvis, complete task 1"
JARVIS: "Task 'buy groceries' marked as complete."
```

## 📁 Project Structure

```
jarvis-ai/
├── main.py                 # Main application entry point
├── config.py              # Configuration settings
├── voice_handler.py       # Voice recognition & text-to-speech
├── task_manager.py        # Task storage and management
├── command_processor.py    # Command parsing and execution
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
└── README.md             # This file
```

## ⚙️ Configuration

Edit `config.py` to customize:

- **Wake word** - Change from "jarvis" to your preferred keyword
- **Voice rate** - Adjust speaking speed (default: 150)
- **Voice volume** - Control speaker volume (0.0-1.0)
- **Timeout** - Listening duration in seconds
- **Language** - Speech recognition language code

## 🔌 API Endpoints

When web UI is enabled, JARVIS exposes REST APIs:

### Get All Tasks
```
GET /api/tasks
```

### Create Task
```
POST /api/tasks
Content-Type: application/json

{
  "title": "Buy milk",
  "category": "shopping",
  "priority": "normal"
}
```

### Complete Task
```
POST /api/tasks/<task_id>/complete
```

### Delete Task
```
DELETE /api/tasks/<task_id>
```

## 📝 Task Storage

Tasks are automatically saved to `tasks.json` in the following format:

```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "category": "shopping",
    "priority": "normal",
    "completed": false,
    "created_at": "2024-01-15T10:30:00"
  }
]
```

## 🔧 Troubleshooting

### Microphone not detected
- Check microphone is connected and recognized by system
- Test with: `python -m speech_recognition`

### No audio output
- Verify speakers/headphones are connected
- Check system volume settings
- Test with: `python -c "import pyttsx3; pyttsx3.init().say('test').runAndWait()"`

### Wake word not recognized
- Speak clearly and at normal volume
- Adjust `LISTENING_TIMEOUT` in config.py
- Change `WAKE_WORD` to something easier to recognize

### Poor speech recognition
- Use a better microphone
- Reduce background noise
- Speak more clearly and slowly
- Change language in config if needed

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Uses SpeechRecognition for voice input
- Uses pyttsx3 for text-to-speech
- Built with Flask for web interface
- Inspired by JARVIS from Iron Man

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Start using JARVIS today and automate your daily tasks with voice commands!** 🚀