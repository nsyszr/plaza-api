# /src/api/utils.py

from flask import json, Response

def resource_response(res, category, status_code, *args, **kwargs):
    if kwargs.get('many', False):
        resource_list = {
            'category': category,
            'type': kwargs.get('type', 'UnknownList'),
            'count': len(res),
            'total': len(res),
            'start': 1,
            'members': res
        }
        return Response(
            mimetype='application/json',
            response=json.dumps(resource_list),
            status=status_code
        )
    else:
        meta = {
            'category': category
        }
        return Response(
            mimetype='application/json',
            response=json.dumps({**meta, **res}),
            status=status_code
        )

def empty_response(status_code):
    return Response(
        mimetype='application/json',
        status=status_code
    )

def error_response(error, status_code):
    return Response(
        mimetype='application/json',
        response=json.dumps(error),
        status=status_code
    )
