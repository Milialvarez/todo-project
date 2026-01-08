class AppException(Exception):
    """Base exception for domain errors"""
    pass

class TaskNotFoundError(AppException):
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with id {task_id} not found")

class ReminderNotFoundError(AppException):
    def __init__(self, reminder_id: int):
        self.reminder_id = reminder_id
        super().__init__(f"Reminder with id {reminder_id} not found")

class InvalidReminderDateError(AppException):
    def __init__(self, date: str):
        super().__init__(f"Invalid reminder date: {date}")

class UserNotFoundError(AppException):
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User with id {user_id} not found")

class UserInactiveError(AppException):
    def __init__(self):
        super().__init__("User is inactive")

class PermissionDeniedError(AppException):
    def __init__(self):
        super().__init__("You do not have permission to perform this action")

class InvalidTokenError(AppException):
    def __init__(self):
        super().__init__("Invalid or expired token")
