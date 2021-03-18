import json
from flask_restful import Resource
from flask import Response, request
from rfactorapp.task.controller import (
    task_post, 
    task_get_all, 
    task_put, 
    get_id,
    task_delete
)


class TaskApi(Resource):

    def post(self):
        body = request.get_json()
        resp = task_post(body)
        val = int(resp['status'])
        resp_j = json.dumps(resp)
        return Response(resp_j, mimetype="application/json", status=val)
        
    def get(self):
        resp = task_get_all()
        val = int(resp['status'])
        resp_j = json.dumps(resp)    
        return Response(resp_j, mimetype="application/json", status=val)
        

class TasksApi(Resource):

    def get(self, id):
        resp = get_id(id)
        val = int(resp['status'])
        resp_j = json.dumps(resp)
        return Response(resp_j, mimetype="application/json", status=val)
        
    def put(self, id):
        body = request.get_json()
        resp = task_put(id, body)
        val = int(resp['status'])
        resp_j = json.dumps(resp)
        return Response(resp_j, mimetype="application/json", status=val)

    def delete(self, id):
        resp = task_delete(id)
        val = int(resp['status'])
        resp_j = json.dumps(resp)
        return Response(resp_j, mimetype="application/json", status=val)

