import re
import json
from flask import request
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

def query_response_success(result):
    task = json.loads(result)
    if not task:
        return message_empty
    return response_success(task)


def response_success(task):
    message_200["data"] = task
    return message_200


def query_response_error(info):
    return response_error(info)


def response_error(info):
    message_400["info"] = info
    return message_400
    

def task_get_all():
    status = request.args.get('status')
    order = request.args.get('order')
    sort = request.args.get('sort')
    search = request.args.get('s')
    page = request.args.get('page')

    per_page = request.args.get('limit')

    print(page)

    p = paginate(page, per_page)
    print(p)
    # GET /tasks?page=1&limit=10 (registros do 1 a 10 (10 primeiros registros))
    # GET /tasks?page=2&limit=10 (registros do 11 a 20 (segundo pagina de registros))
    # GET /tasks?page=2&limit=10&s=valmir&status=open&sort=createdAt&order=desc


    if status is None and order is None and sort is None and search is None:
        
        result = Tasks.objects.all().to_json()
        return query_response_success(result)

    

    if status is not None and order is None and sort is None and search is None:
        if status != 'open' and status != 'closed':
            info = ["Values for status: open or closed"]
            return query_response_error(info)

        result = Tasks.objects(status=status).to_json()
        return query_response_success(result)
        

    if status is None and order is not None and sort is not None and search is None:
        if sort != 'id' and sort != 'name' and sort != 'description' and sort != 'status' and sort != 'createtad':
            info = ["Values for sort: id or description"]
            return query_response_error(info)

        if order != 'asc' and order != 'desc':
            info = ["Values for order: asc or desc"]
            return query_response_error(info)

        if order == 'asc':
            sort = ('-'+sort)
            result = Tasks.objects().order_by(sort).to_json()
            return query_response_success(result)

        if order == 'desc':
            result = Tasks.objects().order_by(sort).to_json()
            return query_response_success(result)
    

    if status is not None and order is not None and sort is not None and search is None:
        if status != 'open' and status != 'closed':
            info = ["Values for status: open or closed"]
            return query_response_error(info)

        if sort != 'id' and sort != 'name' and sort != 'description' and sort != 'status' and sort != 'createtad':
            info = ["Values for sort: id or description or createtad"]
            return query_response_error(info)

        if order != 'asc' and order != 'desc':
            info = ["Values for order: asc or desc"]
            return query_response_error(info)
    
        if order == 'asc':
            sort_asc = ('-'+sort)
            result = Tasks.objects(status=status, sort=sort).order_by(sort_asc).to_json()
            return query_response_success(result)

        result = Tasks.objects(status=status, sort=sort).order_by(sort).to_json()
        return query_response_success(result)
        

    if status is None and order is None and sort is None and search is not None:
        result = Tasks.objects(Q(name=re.compile('.*'+ search +'.*', re.IGNORECASE)) | Q(description=re.compile('.*'+ search +'.*', re.IGNORECASE))).to_json()
        return query_response_success(result)


    if status is not None and order is not None and sort is not None and search is None:
        if sort != 'id' and sort != 'name' and sort != 'description' and sort != 'status' and sort != 'createtad':
            info = ["Values for order: asc or desc"]
            return query_response_error(info)

        if status != 'open' and status != 'closed':
            info = ["Values for status: open or closed"]
            return query_response_error(info)

        if order != 'asc' and order != 'desc':
            info = ["Values for order: asc or desc"]
            return query_response_error(info)

        if order == 'asc':
            sort_asc = ('-' + sort)
            result = Tasks.objects(Q(name=re.compile('.*' + search + '.*', re.IGNORECASE)) | Q(description=re.compile('.*' + search + '.*', re.IGNORECASE)) & Q(status=status)).order_by(sort_asc).to_json()
            return query_response_success(result)
        
        result = Tasks.objects(Q(name=re.compile('.*' + search + '.*', re.IGNORECASE)) | Q(description=re.compile('.*' + search + '.*', re.IGNORECASE)) & Q(status=status)).order_by(sort).to_json()
        return query_response_success(result)
        

def task_get_name(name):
    task = Tasks.objects(name=name).to_json()
    return task


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
    

def unique_name(name):
    try:
        task = Tasks.objects.get(name=name)
    except DoesNotExist:
        return False
    except MultipleObjectsReturned:
        return False
    return True


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


def task_count():
    count = Tasks.objects.count()
    return count


def get_id(id):
    try:
        result = Tasks.objects.get(id=id).to_json()
        return query_response_success(result)
    except (DoesNotExist, MultipleObjectsReturned):
        info = ["Task not found"]
        return query_response_error(info)
    

def get_id_for_name(name):
    try:
        res = Tasks.objects.get(name=name).to_json()
        result = json.loads(res) 
        return result["_id"]["$oid"]
    except (DoesNotExist, MultipleObjectsReturned):
        info = ["Task not found"]
        return query_response_error(info)
    

def task_delete(id):
    if not task_get_id(id):
        info = ["Task not found"]
        return query_response_error(info)
    result = Tasks.objects.get(id=id).to_json()
    delete_id(id)
    return query_response_success(result)


def delete_id(id):
    Tasks.objects(id=id).delete()


def paginate(page, per_page):
    _p = {}
    if page == None:
        page = 1
    if per_page == None:
        per_page = 10

    t_page = Tasks.objects.paginate(page=page, per_page=per_page)

    _p['current'] = t_page.page
    _p['total_page'] = t_page.pages
    _p['per_page'] = t_page.per_page
    _p['total_item'] = t_page.total
    _p['items'] = t_page.items
    return _p