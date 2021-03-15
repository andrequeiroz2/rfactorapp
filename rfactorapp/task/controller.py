import json
from flask import request
from mongoengine.queryset.visitor import Q
import re

from rfactorapp.task.model import Tasks


def task_get_all():
    status = request.args.get('status')
    order = request.args.get('order')
    sort = request.args.get('sort')
    search = request.args.get('s')
    error = {}

    # GET /tasks?status=closed  (retornar varias tasks, porém apenas as com status=closed) controller ok // test ok
    # GET /tasks?sort=status&order=asc  (vai trazer ) query {sort: {status: -1} // ok
    # GET /tasks?sort=status&order=desc  (vai trazer ) query {sort: {status: 1} ok
    # GET /tasks?sort=name&order=asc  (ordenar ALFABETICA pelo nome da task  ) query {sort: {name: -1} ok
    # GET /tasks?status=open&sort=name&order=asc  (ordenar ALFABETICA pelo nome da task  ) query {sort: {name: -1} ok
    # GET /tasks?s=valmir  (search pelo palavra valmir, onde nome ou descricao contenha esta referencia) dica mongo (REGEX) controller ok // test ok
    # GET /tasks?s=valmir&status=open&sort=createdAt&order=desc ok

    if status is None and order is None and sort is None and search is None:
        tasks = Tasks.objects.all().to_json()
        task_list = json.loads(tasks)
        if not task_list:
            error['message'] = "Search returned zero result"
            return json.dumps(error)
        else:
            return tasks

    if status is not None and order is None and sort is None and search is None:
        if status == 'open' or status == 'closed':
            tasks = Tasks.objects(status=status).to_json()
            task_list = json.loads(tasks)
            if not task_list:
                error['message'] = "Search returned zero result"
                return json.dumps(error)
            else:
                return tasks
        else:
            error['message'] = "Error invalid request"
            error['error'] = ["status unrecognized value "]
            error['info'] = ["accepted values for status: open (open tasks) or closed (closed tasks)"]
            return json.dumps(error)

    if status is None and order is not None and sort is not None and search is None:
        if sort == 'id' or sort == 'name' or sort == 'description' or sort == 'status' or sort == 'createtad':
            if order == 'asc':
                sort_asc = ('-'+sort)
                tasks = Tasks.objects().order_by(sort_asc).to_json()
                task_list = json.loads(tasks)
                if not task_list:
                    error['message'] = "Search returned zero result"
                    return json.dumps(error)
                else:
                    return tasks
            elif order == 'desc':
                tasks = Tasks.objects().order_by(sort).to_json()
                task_list = json.loads(tasks)
                if not task_list:
                    error['message'] = "Search returned zero result"
                    return json.dumps(error)
                else:
                    return tasks
            else:
                error['message'] = "Error invalid request"
                error['error'] = ["order unrecognized value "]
                error['info'] = ["accepted values for order: asc (ascending) or desc (descending)"]
                return json.dumps(error)
        else:
            error['message'] = "Error invalid request"
            error['error'] = ["sort unrecognized value "]
            error['info'] = ["accepted values for sort: id (sort id) or description (sort description) or createtad (sort createtad)"]
            return json.dumps(error)

    if status is not None and order is not None and sort is not None and search is None:
        if status != 'open' or status != 'closed':
            error['message'] = "Error invalid request"
            error['error'] = ["status unrecognized value "]
            error['info'] = ["accepted values for status: open (open tasks) or closed (closed tasks)"]
            return json.dumps(error)
        elif sort != 'id' or sort != 'name' or sort != 'description' or sort != 'status' or sort != 'createtad':
            error['message'] = "Error invalid request"
            error['error'] = ["sort unrecognized value "]
            error['info'] = ["accepted values for sort: id (sort id) or description (sort description) or createtad (sort createtad)"]
            return json.dumps(error)
        elif order != 'asc' or order != 'desc':
            error['message'] = "Error invalid request"
            error['error'] = ["order unrecognized value "]
            error['info'] = ["accepted values for order: asc (ascending) or desc (descending)"]
            return json.dumps(error)
        else:
            if order == 'asc':
                sort_asc = ('-' + sort)
                tasks = Tasks.objects(status=status, sort=sort).order_by(sort_asc).to_json()
                task_list = json.loads(tasks)
                if not task_list:
                    error['message'] = "Search returned zero result"
                    return json.dumps(error)
                else:
                    return tasks
            else:
                tasks = Tasks.objects(status=status, sort=sort).order_by(sort).to_json()
                task_list = json.loads(tasks)
                if not task_list:
                    error['message'] = "Search returned zero result"
                    return json.dumps(error)
                else:
                    return tasks

    if status is None and order is None and sort is None and search is not None:
        tasks = Tasks.objects(Q(name=re.compile('.*'+ search +'.*', re.IGNORECASE)) | Q(description=re.compile('.*'+ search +'.*', re.IGNORECASE))).to_json()
        task_list = json.loads(tasks)
        if not task_list:
            error['message'] = "Search returned zero result"
            error['error'] = ["value "+search+" not found"]
            return json.dumps(error)
        else:
            return tasks

    if status is not None and order is not None and sort is not None and search is None:
        if sort != 'id' or sort != 'name' or sort != 'description' or sort != 'status' or sort != 'createtad':
            error['message'] = "Error invalid request"
            error['error'] = ["order unrecognized value "]
            error['info'] = ["accepted values for order: asc (ascending) or desc (descending)"]
            return json.dumps(error)

        elif status != 'open' or status != 'closed':
            error['message'] = "Error invalid request"
            error['error'] = ["status unrecognized value "]
            error['info'] = ["accepted values for status: open (open tasks) or closed (closed tasks)"]
            return json.dumps(error)

        elif order != 'asc' or order != 'desc':
            error['message'] = "Error invalid request"
            error['error'] = ["order unrecognized value "]
            error['info'] = ["accepted values for order: asc (ascending) or desc (descending)"]
            return json.dumps(error)

        else:
            if order == 'asc':
                sort_asc = ('-' + sort)
                tasks = Tasks.objects(Q(name=re.compile('.*' + search + '.*', re.IGNORECASE)) | Q(description=re.compile('.*' + search + '.*', re.IGNORECASE)) & Q(status=status)).order_by(sort_asc).to_json()
                task_list = json.loads(tasks)
                if not task_list:
                    error['message'] = "Search returned zero result"
                    return json.dumps(error)
                else:
                    return tasks
            else:
                tasks = Tasks.objects(Q(name=re.compile('.*' + search + '.*', re.IGNORECASE)) | Q(description=re.compile('.*' + search + '.*', re.IGNORECASE)) & Q(status=status)).order_by(sort).to_json()
                task_list = json.loads(tasks)
                if not task_list:
                    error['message'] = "Search returned zero result"
                    return json.dumps(error)
                else:
                    return tasks


def task_get_name(name):
    task = Tasks.objects(name=name).to_json()
    return task


def get_order_insert(order):
    if order == 1 or order == -1:
        task = Tasks.find().sort({id: 1}).to_json()
        print(task)
        return task
    else:
        return "error: "


def task_post(body):
    resp = {}
    _name = body["name"]
    _description = body["description"]

    if task_check_unique_name_post(_name):
        check = task_check_input(body)
        if not bool(check):
            Tasks(name=_name, description=_description).save()
            task = task_get_name(_name)
            resp["message"] = "Successfully registered task"
            resp["data"] = json.loads(task)
            return resp
        else:
            resp["message"] = "Error task not registered"
            resp["error"] = ["Name task "+check+" em uso"]
            return resp
    else:
        resp["message"] = "Error task not registered"
        resp["error"] = ["Task name is already in use"]
        return resp


def task_post2(body):
    resp = {}
    _name = body["name"]
    _description = body["description"]

    if not task_check_unique_name_post(_name):
        resp["message"] = "Error task not registered"
        resp["error"] = ["Task name is already in use"]
        return resp

    check = task_check_input(body)
    if not bool(check):
        resp["message"] = "Error task not registered"
        resp["error"] = ["Name task "+check+" em uso"]
        return resp

    Tasks(name=_name, description=_description).save()
    task = task_get_name(_name)
    resp["message"] = "Successfully registered task"
    resp["data"] = json.loads(task)
    return resp


def task_check_input(body):
    _name = body["name"]
    _desc = body["description"]
    analyzer = {}

    if len(_name) >= 3:
        pass
    else:
        analyzer["name"] = "Name must contain 3 or more digits"

    if len(_name) <= 30:
        pass
    else:
        analyzer["name"] = "Name must contain less than 30 digits"

    if _name and not _name.isspace():
        pass
    else:
        analyzer["name"] = "Name does not contain valid information"

    if len(_desc) >= 3:
        pass
    else:
        analyzer["description"] = "Description must contain 3 or more digits"

    if len(_name) <= 200:
        pass
    else:
        analyzer["description"] = "Description must contain less than 200 digits"

    if _desc and not _desc.isspace():
        pass
    else:
        analyzer["description"] = "Description does not contain valid information"

    tca = task_check_analyzer(analyzer)
    return tca


def task_check_analyzer(analyzer):
    error = {}
    if not bool(analyzer):
        return error
    else:
        error["error"] = analyzer
        return error

def task_check_json(json_obj):
    _json = json.loads(json_obj)
    if 'error' not in _json:
        return True
    else:
        return False


def task_put(id, body):
    resp = {}
    task = task_get_id(id)
    print('Task ID :', task)
    task_list = json.loads(task)
    if not task_list:
        resp["message"] = "Error Task not updated"
        resp["error"] = ["Task id not found"]
        return json.dumps(resp)
    else:
        name = body['name']
        print('Name Task :', name)
        if task_check_unique_name(id, name):
            tasks_up = Tasks.objects.get(id=id).update(**body)
            tasks = Tasks.objects.get(id=id, name=name).to_json()
            resp["message"] = "Successfully task updated"
            resp["data"] = json.loads(tasks)
            return resp
        else:
            resp["message"] = "Error Task not updated"
            resp["error"] = ["Task name is already in use"]
            return resp


def task_get_id(id):
    task = Tasks.objects.get(id=id).to_json()
    return task


def task_check_unique_name_post(name):
    task = Tasks.objects(name=name)
    if not bool(task):
        return True
    else:
        return False


def task_check_unique_name(id, name):
    count = Tasks.objects(Q(name=name) & Q(id__ne=id)).count()
    if count == 0:
        return True
    else:
        return False


def task_count():
    count = Tasks.objects.count()
    return count