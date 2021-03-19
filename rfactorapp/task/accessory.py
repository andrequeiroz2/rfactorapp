import json
from rfactorapp.task.model import Tasks
from mongoengine.queryset.visitor import Q
from mongoengine.errors import (
    DoesNotExist,
    MultipleObjectsReturned,
)
 

message_200  = {
    "status": 200,
    "msg": "Successfully",
    "data": ""
}

message_400 = {
    "status": 400,
    "msg": "Error",
    "error": "Incorrect parameter",
    "info": ""
}

message_empty = {
    "status": 200,
    "msg": "Search returned zero result",
    "data": [None]
}

message_200_paginate  = {
    "status": 200,
    "msg": "Successfully",
    "data": "",
    "paginate": ""
}


def query_response_success(result):
    task = json.loads(result)
    if not task:
        return message_empty
    message_200["data"] = task
    return message_200
    

def query_reponse_paginate_success(result, paginate):
    task = json.loads(result)
    if not task:
        return message_empty
    message_200_paginate["data"] = task
    message_200_paginate["paginate"] = paginate
    return message_200_paginate
    

def query_response_error(info):
    message_400["info"] = info
    return message_400
    


def paginate(page, per_page):
    _p = {}
    if page == None and int(page) > 0:
        page = 1
    if per_page == None and int(per_page) > 0:
        per_page = 10
            
    t_page = Tasks.objects.paginate(page=int(page), per_page=int(per_page))
    _p['current'] = t_page.page
    _p['total_page'] = t_page.pages
    _p['per_page'] = t_page.per_page
    _p['total_item'] = t_page.total
    return _p


def get_paginate(page, per_page):
    p = int(page)
    per = int(per_page) 

    if page == None and p > 0:
        p = 1
    if per_page == None and per > 0:
        per = 10

    offset = (p - 1) * per
    result = Tasks.objects.skip(offset).limit(int(per)).to_json()
    return result


def unique_name(name):
    try:
        task = Tasks.objects.get(name=name)
        return True
    except (DoesNotExist, MultipleObjectsReturned):
        return False


def check_input(body):
    name = body["name"]
    desc = body["description"]
    
    if len(name) < 3 or len(name) > 30:
        info = "Name min 3 digits and max 30 digits"
        return [False, info]

    if not name and name.isspace():
        info = "Name does not contain valid data"
        return [False, info]

    if len(desc) < 3 or len(desc) > 200:
        info = "Description min 3 digits and max 200 digits"
        return [False, info]

    if not desc and desc.isspace():
        info = "Description does not valid data"
        return [False, info]

    return [True]


def save_task(name, description):
    Tasks(name=name, description=description).save()


def get_task(name, description):
    task = Tasks.objects.get(name=name, description=description).to_json()
    return task


def task_get_id(id):
    try:
        task = Tasks.objects.get(id=id).to_json()
        return True
    except (DoesNotExist, MultipleObjectsReturned):
        return False
    

def task_check_unique_name(id, name):
    count = Tasks.objects(Q(name=name) & Q(id__ne=id)).count()
    if count != 0:
        return False
    return True


def update_task(id, body):
    tasks = Tasks.objects.get(id=id).update(**body)


def delete_id(id):
    Tasks.objects(id=id).delete()


def task_count():
    count = Tasks.objects.count()
    return count


def get_id_for_name(name):
    try:
        res = Tasks.objects.get(name=name).to_json()
        result = json.loads(res) 
        return result["_id"]["$oid"]
    except (DoesNotExist, MultipleObjectsReturned):
        info = ["Task not found"]
        return query_response_error(info)