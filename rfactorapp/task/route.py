from rfactorapp.api.api_task import TaskApi, TasksApi


def init_route_task(api):
    api.add_resource(TaskApi, "/api/task")
    api.add_resource(TasksApi,"/api/task/<id>")
