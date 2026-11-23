# todo/errors.py


class TodoError(Exception):
    """Base exception for the To-Do application."""
    pass


class ValidationError(TodoError):
    """Raised when task data is invalid."""
    pass


class TaskNotFoundError(TodoError):
    """Raised when a task ID does not exist."""
    pass


class StorageError(TodoError):
    """Raised when tasks cannot be loaded or saved."""
    pass