import json
from pathlib import Path
TASK_FILE = Path(__file__).resolve().parents[1] / "data" / "tasks.json"
def _load():
    try:
        return json.loads(TASK_FILE.read_text(encoding="utf-8")) if TASK_FILE.exists() else []
    except (OSError, json.JSONDecodeError):
        return []
def add_task(task):
    if not task:
        return "Please provide a task."
    tasks = _load()
    tasks.append({"task": task, "done": False})
    TASK_FILE.parent.mkdir(parents=True, exist_ok=True)
    TASK_FILE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")
    return f"Added your task: {task}."
def list_tasks():
    tasks = _load()
    if not tasks:
        return "You have no saved tasks."
    return "Your tasks: " + "; ".join(
        f"{i}. {item['task']}" for i, item in enumerate(tasks, 1)
    )
def clear_tasks():
    TASK_FILE.parent.mkdir(parents=True, exist_ok=True)
    TASK_FILE.write_text("[]", encoding="utf-8")
    return "All tasks cleared."
