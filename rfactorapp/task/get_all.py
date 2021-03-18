import re
import json
from flask import request
from rfactorapp.task.model import Tasks
from mongoengine.queryset.visitor import Q
from rfactorapp.task.accessory import (
    paginate,
    query_response_success,
    query_reponse_paginate_success,
    query_response_error,
    get_paginate
)


def task_get_all():
    status = request.args.get('status')
    order = request.args.get('order')
    sort = request.args.get('sort')
    search = request.args.get('s')
    page = request.args.get('page')
    per_page = request.args.get('limit')

    
    # GET /tasks?page=1&limit=10 (registros do 1 a 10 (10 primeiros registros))
    # GET /tasks?page=2&limit=10 (registros do 11 a 20 (segundo pagina de registros))
    # GET /tasks?page=2&limit=10&s=valmir&status=open&sort=createdAt&order=desc


    if status is None and order is None and sort is None and search is None:
        
        if page is not None or per_page is not None:
            _page = paginate(page, per_page)
            _result = get_paginate(page, per_page)
            return query_reponse_paginate_success(_result, _page)
            #return query_response_success(result)
        
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