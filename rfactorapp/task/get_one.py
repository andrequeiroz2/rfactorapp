from rfactorapp.task.model import Tasks
from mongoengine.errors import (
    DoesNotExist,
    MultipleObjectsReturned,
)
from rfactorapp.task.accessory import (
    query_response_success,
    query_response_error
)


def get_id(id):
    try:
        result = Tasks.objects.get(id=id).to_json()
        return query_response_success(result)
    except (DoesNotExist, MultipleObjectsReturned):
        info = ["Task not found"]
        return query_response_error(info)