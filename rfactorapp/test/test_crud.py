import json
from rfactorapp.task.accessory import task_count, get_id_for_name


def test_get_all(client):
    assert client.get("/api/task").status_code == 200
    assert task_count() == 0
    

def test_post(client):
    task = json.dumps({
       "name": "test_post",
       "description": "server off"
    })
    res = client.post("/api/task",
                     headers={'Content-Type': 'application/json'},
                     data=task)

    assert res.status_code == 200
    assert task_count() == 1


def test_put(client):
    task = json.dumps({
       "name": "test_put",
       "description": "server off"
    })
    res = client.post("/api/task",
                     headers={'Content-Type': 'application/json'},
                     data=task)

    task = json.dumps({
        "name": "test_put_mod",
        "description": "server off"
    })

    id = get_id_for_name("test_put")
   
    res = client.get("/api/task/{}".format(id),
                    headers={"Content-Type": "application/json"},
                    data=task)
    
    assert res.status_code == 200


def test_delete(client):
    task = json.dumps({
       "name": "test_delete",
       "description": "server on"
    })
    client.post("/api/task",
                headers={'Content-Type': 'application/json'},
                data=task)

    id = get_id_for_name("test_delete")
   
    res = client.delete("/api/task/{}".format(id),
                    headers={"Content-Type": "application/json"})

    assert res.status_code == 200


def test_get_one(client):
    task = json.dumps({
       "name": "test_get_one",
       "description": "server off"
    })
    rv = client.post("/api/task",
                    headers={'Content-Type': 'application/json'},
                    data=task)

    id = get_id_for_name("test_get_one")
   
    res = client.get("/api/task/{}".format(id),
                    headers={"Content-Type": "application/json"})
    
    assert res.status_code == 200


def test_tear_down(database):
   """
   Delete Database collections after the test is complete
   """
   assert 'tasks' in database.list_collection_names()
   assert database.drop_collection('tasks')
   assert task_count() == 0





# def test_unique_name(client):
#     task = json.dumps({
#         "name": "unique_name",
#         "description": "server off"
#     })
#     res = client.post("/api/task",
#                       headers={'Content-Type': 'application/json'},
#                       data=task)

#     assert res.status_code == 200

#     res1 = client.post("/api/task",
#                       headers={'Content-Type': 'application/json'},
#                       data=task)

#     assert res1.status_code == 400
  

# def test_get_status_open_task(client):
#     """
#     get task close or open
#     :param URL: GET /task?status=closed
#     """
#     res = client.get("/api/task?status=open")
#     assert res.status_code == 201

#     res = client.get("/api/task?status=close")
#     assert res.status_code == 400



# def test_get_name_regex_task(client):
#     task1 = json.dumps({
#         "name": "Valmir",
#         "description": "task1"
#     })
#     task2 = json.dumps({
#         "name": "Andre",
#         "description": "amigo do valmir"
#     })
#     res = client.post("/api/task", headers={'Content-Type': 'application/json'}, data=task1)
#     assert res.status_code == 201
#     res = client.post("/api/task", headers={'Content-Type': 'application/json'}, data=task2)
#     assert res.status_code == 201

#     res = client.get("/api/task?s=valmir")
#     assert res.status_code == 201

#     res1 = client.get("/api/task?s=ZZZZ")
#     assert res1.status_code == 400


#def test_get_id_task(client):
#    """
#    get task id
#    """
#    rs = client.get("/api/task").status_code == 201
#
#    assert client.get("/api/task").status_code == 201





