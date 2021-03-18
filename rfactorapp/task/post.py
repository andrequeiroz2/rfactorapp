from rfactorapp.task.accessory import (
    unique_name,
    query_response_success,
    query_response_error,
    check_input,
    save_task,
    get_task
)

def task_post(body):
    name = body["name"]
    description = body["description"]

    if unique_name(name):
        info = ["Task name is already in use"]
        return query_response_error(info)

    info = check_input(body)
    if not info[0]:
        return query_response_error(info[1])
        
    save_task(name, description)
    result = get_task(name, description)
    return query_response_success(result)