import json
from rfactorapp.task.controller import task_count, get_order_insert

url = "/api/tasks"


def test_get_all_task(client):
    """
    get all tasks
    """
    assert client.get("/api/task").status_code == 201
    assert task_count() == 0
    #falta paginacao
    #tem que retornar 200 so create retorna 201

def test_post_task(client):
    """
    post tasks
    """
    task = json.dumps({
       "name": "server123",
       "description": "server on"
    })
    res = client.post("/api/task",
                     headers={'Content-Type': 'application/json'},
                     data=task)

    assert res.status_code == 201
    assert task_count() == 1


def test_unique_name_task(client):
    """
    check post unique name
    """
    task = json.dumps({
        "name": "server123",
        "description": "server on"
    })
    res = client.post("/api/task",
                      headers={'Content-Type': 'application/json'},
                      data=task)

    assert res.status_code == 400
    assert task_count() == 1


def test_post_many_task(client):
    """
    post 3 tasks
    """
    task1 = json.dumps({
        "name": "task1",
        "description": "task1"
    })
    task2 = json.dumps({
        "name": "task2",
        "description": "task2"
    })
    task3 = json.dumps({
        "name": "task3",
        "description": "task3"
    })
    res = client.post("/api/task", headers={'Content-Type': 'application/json'}, data=task1)
    assert res.status_code == 201
    res = client.post("/api/task", headers={'Content-Type': 'application/json'}, data=task2)
    assert res.status_code == 201
    res = client.post("/api/task", headers={'Content-Type': 'application/json'}, data=task3)
    assert res.status_code == 201
    assert task_count() == 4


def test_get_status_open_task(client):
    """
    get task close or open
    :param URL: GET /task?status=closed
    """
    res = client.get("/api/task?status=open")
    assert res.status_code == 201

    res = client.get("/api/task?status=close")
    assert res.status_code == 400

# GET /tasks?status=closed  (retornar varias tasks, porém apenas as com status=closed) controller ok // test ok
# GET /tasks?sort=status&order=asc  (vai trazer ) query {sort: {status: -1} // ok
# GET /tasks?sort=status&order=desc  (vai trazer ) query {sort: {status: 1} ok
# GET /tasks?sort=name&order=asc  (ordenar ALFABETICA pelo nome da task  ) query {sort: {name: -1} ok
# GET /tasks?status=open&sort=name&order=asc  (ordenar ALFABETICA pelo nome da task  ) query {sort: {name: -1} ok
# GET /tasks?s=valmir  (search pelo palavra valmir, onde nome ou descricao contenha esta referencia) dica mongo (REGEX) controller ok // test ok
# GET /tasks?s=valmir&status=open&sort=createdAt&order=desc ok

def test_get_name_regex_task(client):
    task1 = json.dumps({
        "name": "Valmir",
        "description": "task1"
    })
    task2 = json.dumps({
        "name": "Andre",
        "description": "amigo do valmir"
    })
    res = client.post("/api/task", headers={'Content-Type': 'application/json'}, data=task1)
    assert res.status_code == 201
    res = client.post("/api/task", headers={'Content-Type': 'application/json'}, data=task2)
    assert res.status_code == 201

    res = client.get("/api/task?s=valmir")
    assert res.status_code == 201

    res1 = client.get("/api/task?s=ZZZZ")
    assert res1.status_code == 400


#def test_get_id_task(client):
#    """
#    get task id
#    """
#    rs = client.get("/api/task").status_code == 201
#
#    assert client.get("/api/task").status_code == 201


def test_tear_down(database):
    """
    Delete Database collections after the test is complete
    """
    assert 'tasks' in database.list_collection_names()
    assert database.drop_collection('tasks')
    assert task_count() == 0


