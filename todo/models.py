# todo/models.py

from datetime import date, datetime

from todo.errors import ValidationError, TaskNotFoundError


PRIORITIES = {
    "high": 1,
    "medium": 2,
    "low": 3
}


def validate_choice(choice):
    """Validate the main menu choice."""

    if choice not in ["1", "2", "3", "4", "5", "6"]:
        raise ValidationError("choose a number from 1 to 6.")

    return int(choice)


def validate_id(task_id):
    """Validate a task ID."""

    try:
        task_id = int(task_id)

    except (ValueError, TypeError):
        raise ValidationError("task ID must be a whole number.")

    if task_id <= 0:
        raise ValidationError("task ID must be positive.")

    return task_id


def validate_date(due):
    """Validate a task due date."""

    try:
        due_date = datetime.strptime(due, "%Y-%m-%d").date()

    except (ValueError, TypeError):
        raise ValidationError("date must be YYYY-MM-DD.")

    if due_date < date.today():
        raise ValidationError("due date cannot be in the past.")

    return due_date.isoformat()


def validate_priority(priority):
    """Validate task priority."""

    priority = priority.strip().lower()

    if priority not in PRIORITIES:
        raise ValidationError(
            "priority must be high, medium or low."
        )

    return priority


def add_task(tasks, title, due, priority):
    """Return a new task list with the added task."""

    title = title.strip()

    if not title:
        raise ValidationError("task title cannot be empty.")

    for task in tasks:
        if (
            task["title"].lower() == title.lower()
            and not task["done"]
        ):
            raise ValidationError(
                f"'{title}' is already an open task."
            )

    due = validate_date(due)
    priority = validate_priority(priority)

    highest_id = max(
        (task["id"] for task in tasks),
        default=0
    )

    new_task = {
        "id": highest_id + 1,
        "title": title,
        "due": due,
        "priority": priority,
        "done": False,
        "created": datetime.now().isoformat()
    }

    return tasks + [new_task], new_task


def complete_task(tasks, task_id):
    """Return updated tasks with the selected task completed."""

    task_id = validate_id(task_id)

    updated = []

    found = None

    for task in tasks:

        if task["id"] == task_id:

            if task["done"]:
                raise ValidationError(
                    "task is already completed."
                )

            changed = task.copy()
            changed["done"] = True

            updated.append(changed)
            found = changed

        else:
            updated.append(task.copy())

    if found is None:
        raise TaskNotFoundError(
            f"no task with ID {task_id}."
        )

    return updated, found


def delete_task(tasks, task_id):
    """Return a task list without the selected task."""

    task_id = validate_id(task_id)

    for task in tasks:

        if task["id"] == task_id:

            updated = [
                item.copy()
                for item in tasks
                if item["id"] != task_id
            ]

            return updated, task

    raise TaskNotFoundError(
        f"no task with ID {task_id}."
    )


def find_task(tasks, task_id):
    """Find a task by ID."""

    task_id = validate_id(task_id)

    for task in tasks:
        if task["id"] == task_id:
            return task

    raise TaskNotFoundError(
        f"no task with ID {task_id}."
    )


def search_tasks(tasks, keyword):
    """Search tasks by partial title."""

    keyword = keyword.strip().lower()

    if not keyword:
        raise ValidationError("search cannot be empty.")

    return [
        task.copy()
        for task in tasks
        if keyword in task["title"].lower()
    ]


def sort_tasks(tasks):
    """Sort open tasks first, then priority and due date."""

    return sorted(
        tasks,
        key=lambda task: (
            task["done"],
            PRIORITIES[task["priority"]],
            task["due"]
        )
    )


def task_status(task):
    """Return the task status."""

    if task["done"]:
        return "done"

    if task["due"] < date.today().isoformat():
        return "OVERDUE"

    return "open"