# general error
class InternalServerError(Exception):
    pass


class SchemaValidationError(Exception):
    pass


# errors task
class TaskAlreadyExistsError(Exception):
    pass


class UpdatingTaskError(Exception):
    pass


class TaskDoesNotExist(Exception):
    pass


class DeletingTaskError(Exception):
    pass


class TaskNotRegistered(Exception):
    pass


errors = {
    "InternalServerError": {"message": "Something went wrong", "status": 500},
    "SchemaValidationError": {
        "message": "Request is missing required fields",
        "status": 400,
    },

    "TaskDoesNotExist": {
        "message": "Task with given name doesn't exists",
        "error": {
            "status": 400
        }

    },
}