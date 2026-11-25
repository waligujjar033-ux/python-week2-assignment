# todo/cli.py

from pathlib import Path

from rich.console import Console
from rich.table import Table

from t3_converter import ask_choice, ask_number

from todo.errors import TodoError, ValidationError
from todo.models import (
    add_task,
    complete_task,
    delete_task,
    find_task,
    search_tasks,
    sort_tasks,
    task_status,
    validate_choice,
    validate_title,
    validate_date
)
from todo.storage import load_tasks, save_tasks


console = Console()

TASKS_PATH = Path(__file__).resolve().parent.parent / "tasks.json"


def show_menu():
    """Display the To-Do menu."""

    print("\n===== To-Do =====")
    print("1. Add   2. List   3. Complete   4. Delete   5. Search   6. Exit")


def show_tasks(tasks):
    """Display tasks in a rich table."""

    table = Table(title="To-Do Tasks")

    table.add_column("ID")
    table.add_column("Title")
    table.add_column("Due")
    table.add_column("Priority")
    table.add_column("Status")

    for task in sort_tasks(tasks):

        status = task_status(task)

        table.add_row(
            str(task["id"]),
            task["title"],
            task["due"],
            task["priority"],
            status
        )

    console.print(table)


def handle_add(tasks, last_id): 
    """Ask for task details and add a task."""

    while True:
        title = input("Title: ")

        try:
            title = validate_title(tasks, title)
            break

        except ValidationError as error:
            print("Error:", error)
            
    while True:
        due = input("Due (YYYY-MM-DD): ")
        try:
            validate_date(due)
            break
        except ValidationError as error:
            print("Error:", error)

    while True:
        priority = input("Priority (high/medium/low): ")

        try:
            updated, task = add_task(
                tasks, title, due, priority,last_id
            )

            last_id = task["id"]

            save_tasks(updated, TASKS_PATH, last_id)

            print(f"Added task {task['id']}.")

            return updated, last_id
        except ValidationError as error:
            print("Error:", error)

        except TodoError:
            raise


def handle_complete(tasks, last_id):
    """Complete a task using its ID."""

    task_id = ask_number("Task ID: ")

    updated, task = complete_task(tasks, task_id)

    save_tasks(updated, TASKS_PATH, last_id)

    print("Completed:", task["title"])

    return updated


def handle_delete(tasks, last_id):
    """Delete a task after confirmation."""

    task_id = ask_number("Task ID: ")

    task = find_task(tasks, task_id)

    answer = input(
        f"Delete '{task['title']}'? (y/n): "
    ).strip().lower()

    if answer != "y":
        print("Delete cancelled.")
        return tasks

    updated, deleted = delete_task(tasks, task_id)

    save_tasks(updated, TASKS_PATH, last_id)

    print("Deleted:", deleted["title"])

    return updated


def handle_search(tasks):
    """Search tasks by partial title."""

    keyword = input("Search: ")

    matches = search_tasks(tasks, keyword)

    show_tasks(matches)

    if len(matches) == 1:
        print("1 match.")
    else:
        print(f"{len(matches)} matches.")

def main():
    """Run the main To-Do application."""

    try:
        tasks, last_id, corrupted = load_tasks(TASKS_PATH)

        if corrupted:
            print("Warning: tasks.json is corrupt. Backed up to tasks.json.bak. Starting with an empty task list.")

        print(f"Loaded {len(tasks)} tasks.")
    except TodoError as error:
        print("Error:", error)
        return

    while True:

        try:
            show_menu()

            choice = ask_choice(
                "Choose: ",
                ["1", "2", "3", "4", "5", "6"],
                validator=validate_choice
            )  

            choice = validate_choice(str(choice))

            if choice == 1:
                tasks, last_id = handle_add(tasks,last_id)

            elif choice == 2:

                show_tasks(tasks)

                open_count = sum(
                    not task["done"]
                    for task in tasks
                )

                done_count = sum(
                    task["done"]
                    for task in tasks
                )

                overdue_count = sum(
                    task_status(task) == "OVERDUE"
                    for task in tasks
                )

                print(
                    f"{open_count} open, "
                    f"{done_count} done, "
                    f"{overdue_count} overdue"
                )

            elif choice == 3:
                tasks = handle_complete(tasks, last_id)

            elif choice == 4:
                tasks = handle_delete(tasks, last_id)

            elif choice == 5:
                handle_search(tasks)

            elif choice == 6:
                print("Goodbye!")
                break

        except TodoError as error:
            print("Error:", error)

        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break