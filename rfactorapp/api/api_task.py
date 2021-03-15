import json
from flask import Response
from flask_restful import Resource
from flask import request
from rfactorapp.task.controller import task_post, task_get_all, task_get_id, task_check_json, task_put
from rfactorapp.task.exceptions import TaskDoesNotExist

from mongoengine.errors import (
    FieldDoesNotExist,
    NotUniqueError,
    DoesNotExist,
    ValidationError,
    InvalidQueryError,
)
#from rfactorapp.task.exceptions.
#(
#    DeletingTaskError,
#    SchemaValidationError,
#    TaskAlreadyExistsError,
#    InternalServerError,
#    UpdatingTaskError,
#     TaskDoesNotExist,
#    TaskNotRegistered,
#)


class TaskApi(Resource):

    def post(self):
        body = request.get_json()
        resp = task_post(body)
        resj = json.dumps(resp)
        if 'data' in resp.keys():
            return Response(resj, status=201)
        else:
            return Response(resj, status=400)

    def get(self):
        resp = task_get_all()
        if task_check_json(resp):
            return Response(resp, mimetype="application/json", status=201)
        else:
            return Response(resp, mimetype="application/json", status=400)


class TasksApi(Resource):

    def get(self, id):
        try:
            task = task_get_id(id)
            return Response(task, mimetype="application/json", status=201)
        except DoesNotExist:
            return Response(TaskDoesNotExist, mimetype="application/json", status=400)

    def put(self, id):
        body = request.get_json()
        resp = task_put(id, body)
        resj = json.dumps(resp)
        if 'data' in resp.keys():
            return Response(resj, status=201)
        else:
            return Response(resj, status=400)











class TasksNameApi(Resource):
    from flask import request

    #@app.route('/data')
    #def data():
        # here we want to get the value of user (i.e. ?user=some-value)
    #    user = request.args.get('user')

    def get(self, name):
        try:
            task = task_get_id(name)
            return Response(task, mimetype="application/json", status=201)
        except DoesNotExist:
            return Response(TaskDoesNotExist, mimetype="application/json", status=400)


