from rfactorapp.task.model import Tasks
from rfactorapp.task.accessory import (
    task_get_id,
    query_response_success,
    query_response_error,
    delete_id
)


def task_delete(id):
    if not task_get_id(id):
        info = ["Task not found"]
        return query_response_error(info)
    result = Tasks.objects.get(id=id).to_json()
    delete_id(id)
    return query_response_success(result)