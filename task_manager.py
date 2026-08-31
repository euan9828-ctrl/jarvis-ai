import json
import os
from datetime import datetime
from config import CONFIG
import logging

logger = logging.getLogger(__name__)

class TaskManager:
    def __init__(self):
        """Initialize task manager and load existing tasks"""
        self.task_file = CONFIG['TASK_STORAGE']
        self.tasks = self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        try:
            if os.path.exists(self.task_file):
                with open(self.task_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Error loading tasks: {e}")
            return []
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        try:
            with open(self.task_file, 'w') as f:
                json.dump(self.tasks, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving tasks: {e}")
            return False
    
    def add_task(self, title, category="personal", priority="normal", due_date=None):
        """Add a new task"""
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "category": category,
            "priority": priority,
            "due_date": due_date,
            "completed": False,
            "created_at": datetime.now().isoformat()
        }
        self.tasks.append(task)
        self.save_tasks()
        logger.info(f"Task added: {title}")
        return task
    
    def get_all_tasks(self):
        """Get all tasks"""
        return self.tasks
    
    def get_pending_tasks(self):
        """Get incomplete tasks"""
        return [task for task in self.tasks if not task['completed']]
    
    def get_tasks_by_category(self, category):
        """Get tasks by category"""
        return [task for task in self.tasks if task['category'] == category]
    
    def complete_task(self, task_id):
        """Mark a task as completed"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = True
                task['completed_at'] = datetime.now().isoformat()
                self.save_tasks()
                logger.info(f"Task completed: {task['title']}")
                return task
        return None
    
    def delete_task(self, task_id):
        """Delete a task"""
        self.tasks = [task for task in self.tasks if task['id'] != task_id]
        self.save_tasks()
        logger.info(f"Task deleted: ID {task_id}")
        return True
    
    def get_task_summary(self):
        """Get summary of tasks"""
        pending = self.get_pending_tasks()
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task['completed'])
        
        summary = f"You have {len(pending)} pending tasks out of {total} total. "
        summary += f"{completed} tasks completed. "
        
        if pending:
            summary += "Your pending tasks are: "
            for task in pending[:3]:  # List first 3
                summary += f"{task['title']}, "
        
        return summary