import json
from pathlib import Path
from datetime import datetime

class TaskManager:
    def __init__(self, config_path = None):
        if config_path is None:
            config_path = Path(__file__).resolve().parent.parent/"config"/"tasks.json"
        self.config_path = Path(config_path)
        self.config_path.parent.mkdir(parents = True, exist_ok=True)
        self.tasks = []
        self.load()
    def load(self):

        if not self.config_path.exists():

            self.tasks = []

            self.save()

            return

        try:
            with open(self.config_path, "r", encoding="utf-8" ) as file:
                data = json.load(file)
            self.tasks = data.get("tasks", [])
        except (json.JSONDecodeError, OSError):
            self.tasks = []
    def save(self):
        with open(self.config_path, "w", encoding="utf-8") as file:
            json.dump({"tasks": self.tasks}, file, indent=4)
    def create_task(self, title, steps = None):
        if not title.strip():
            raise ValueError("Task title cannot be empty.")
        if steps is None:
            steps = []
        task_id = f"task_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        task = {
            "id": task_id,
            "title": title.strip(),
            "status": ("in_progress" if steps else "not_started"),
            "created_at": datetime.now().isoformat(),
            "steps": []
        }

        for index, description in enumerate(steps, start = 1):
            task["steps"].append({
                "id": index, 
                "description": description,
                "completed": False
            })
        self.tasks.append(task)
        self.save()
        return task

    def get_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None

    def get_task_by_title(self, title):
        title = title.lower()
        for task in self.tasks:
            if task["title"].lower() == title:
                return task
        return None

    def list_tasks(self):
        return self.tasks.copy()

    def complete_step(self, task_id, step_id):
        task = self.get_task(task_id)
        if task is None:
            raise ValueError(f"Task not found: {task_id}")
        for step in task["steps"]:
            if step["id"] == step_id:
                step["completed"] = True
                self.update_task_status(task)
                self.save()
                return task
        raise ValueError(f"Step not found: {step_id}")

    def uncomplete_step(self, task_id, step_id):
        task = self.get_task(task_id)
        if task is None:
            raise ValueError(f"Task not found: {task_id}")
        for step in task["steps"]:
            if step["id"] == step_id:
                step["completed"] = False
                self.update_task_status(task)
                self.save()
                return task
        raise ValueError(f"Step not found {step_id}")
    def update_task_status(self, task):
        steps = task["steps"]
        if not steps:
            task["status"] = "not_started"
            return
        completed = sum(step["completed"] for step in steps)
        if completed == 0:
            task["status"] = "not_started"
        elif completed == len(steps):
            task["status"] = "completed"
        else:
            task["status"] = "in_progress"
    def delete_task(self, task_id):
        original_count = len(self.tasks)
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
        changed = len(self.tasks) != original_count

        if changed:
            self.save()
        return changed