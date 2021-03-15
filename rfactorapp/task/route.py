from rfactorapp.api.api_task import TaskApi, TasksApi, TasksNameApi


def init_route_task(api):
    api.add_resource(TaskApi, "/api/task")
    api.add_resource(TasksApi,"/api/task/<id>")
    api.add_resource(TasksNameApi,"/api/task/<name>")
