# Base exception for all domain/business errors.
# This allows handling business errors globally in one place.
class AppException(Exception):
    """Base exception for domain errors"""
    pass

# TASKS 

# Raised when a task with a given ID does not exist
class TaskNotFoundError(AppException):
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with id {task_id} not found")

# REMINDERS 

# Raised when a reminder with a given ID does not exist
class ReminderNotFoundError(AppException):
    def __init__(self, reminder_id: int):
        self.reminder_id = reminder_id
        super().__init__(f"Reminder with id {reminder_id} not found")

# Raised when a reminder date is invalid
# (e.g. past date, wrong format)
class InvalidReminderDateError(AppException):
    def __init__(self, date: str):
        super().__init__(f"Invalid reminder date: {date}")

# USERS

# Raised when a user with a given ID does not exist
class UserNotFoundError(AppException):
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User with id {user_id} not found")

# Raised when a user exists but is inactive
class UserInactiveError(AppException):
    def __init__(self):
        super().__init__("User is inactive")

# AUTH / PERMISSIONS

# Raised when a user tries to perform an action without the required role or permissions
class PermissionDeniedError(AppException):
    def __init__(self):
        super().__init__("You do not have permission to perform this action")

# Raised when an access or refresh token is invalid or expired
class InvalidTokenError(AppException):
    def __init__(self):
        super().__init__("Invalid or expired token")
