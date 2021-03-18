from rfactorapp.task.accessory import (
    task_get_id,
    query_response_success,
    query_response_error,
    task_check_unique_name,
    update_task,
    get_task
)


def task_put(id, body):
    name = body['name']
    desc = body['description']

    if not task_get_id(id):
        info = ["Task not found"]
        return query_response_error(info)
    
    if not task_check_unique_name(id, name):
        info = ["Task name is already in use"]
        return query_response_error(info)

    update_task(id, body)
    result = get_task(name, desc)
    return query_response_success(result)