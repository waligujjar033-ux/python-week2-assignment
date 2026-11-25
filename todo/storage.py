# todo/storage.py

import json
from pathlib import Path

from todo.errors import StorageError


STARTER_TASKS = [
    {
        "id": 1,
        "title": "Submit Week 2 assignment",
        "due": "2026-11-22",
        "priority": "high",
        "done": False,
        "created": "2026-11-16T10:00:00"
    },
    {
        "id": 2,
        "title": "Pay internet bill",
        "due": "2026-11-18",
        "priority": "medium",
        "done": False,
        "created": "2026-11-16T10:05:00"
    },
    {
        "id": 3,
        "title": "Read PEP 8",
        "due": "2026-11-30",
        "priority": "low",
        "done": False,
        "created": "2026-11-16T10:10:00"
    },
    {
        "id": 4,
        "title": "Set up .venv",
        "due": "2026-11-16",
        "priority": "high",
        "done": True,
        "created": "2026-11-16T10:15:00"
    }
]


def load_tasks(path):
    """Load tasks from JSON or create starter tasks."""

    path = Path(path)

    if not path.exists():
        tasks = [task.copy() for task in STARTER_TASKS]
        last_id = 4
        save_tasks(tasks, path, last_id)
        return tasks, last_id

    try:
        with path.open("r", encoding="utf-8") as file:
                data = json.load(file)

        if isinstance(data, list):
            tasks = data
            last_id = None

        elif isinstance(data, dict):
            tasks = data.get("tasks")
            last_id = data.get("last_id")

            if type(last_id) is not int or last_id < 0:
                raise ValueError("Invalid last ID.")

        else:
            raise ValueError("Invalid JSON structure.")

        if not isinstance(tasks, list):
            raise ValueError("JSON must contain a list.")

        required = {
            "id", "title", "due",
            "priority", "done", "created"
        }

        ids = set()

        for task in tasks:

            if not isinstance(task, dict):
                raise ValueError("Invalid task.")

            if not required.issubset(task.keys()):
                raise ValueError("Missing task fields.")

            if (
                type(task["id"]) is not int
                or task["id"] <= 0
                or task["id"] in ids
                or not isinstance(task["title"], str)
                or not task["title"].strip()
                or not isinstance(task["due"], str)
                or not isinstance(task["created"], str)
                or task["priority"] not in ("high", "medium", "low")
                or type(task["done"]) is not bool
            ):
             raise ValueError("Invalid task data.")

            ids.add(task["id"])

        highest_id = max(ids, default=0)

        if last_id is None:
               last_id = highest_id

        elif last_id < highest_id:
               raise ValueError("Invalid last ID.")

        return tasks, last_id
    except (json.JSONDecodeError, ValueError, TypeError):
         backup = path.with_name("tasks.json.bak")

    try:
            if backup.exists():
                backup.unlink()

            path.rename(backup)

    except OSError as error:
            raise StorageError(
                f"could not back up invalid tasks file: {error}"
            ) from error

            return [], 0
    except OSError as error:
     raise StorageError(
            f"could not load tasks: {error}"
        ) from error


def save_tasks(tasks, path, last_id):  
    """Save tasks to a JSON file."""

    path = Path(path)

    try:
        with path.open("w", encoding="utf-8") as file:
            data = {
                "last_id": last_id,
                "tasks": tasks
            }

            json.dump(data, file, indent=4)
    except (OSError, TypeError, ValueError) as error:
        raise StorageError(
            f"could not save tasks: {error}"
        ) from error