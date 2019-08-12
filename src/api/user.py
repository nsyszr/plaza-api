# /src/api/user.py

from flask import request, Blueprint
from ..models.user import UserModel, user_schema, user_list_schema
from .utils import resource_response, empty_response, error_response

user_api = Blueprint('users', __name__)

API_CATEGORY = 'users'
API_LIST_TYPE = 'UserListV1'

@user_api.route('/', methods=['GET'])
def find_all():
    models = UserModel.find_all()

    res_data = user_list_schema.dump(models, many=True).data
    return resource_response(res_data, API_CATEGORY, 200, many=True, type=API_LIST_TYPE)


@user_api.route('/', methods=['POST'])
def create():
    req_data = request.get_json()
    data, error = user_schema.load(req_data)

    if error:
        return error_response(error, 400)

    user_in_db = UserModel.get_by_email_address(data.get('email_address'))
    if user_in_db:
        return error_response({'error': 'User already exist, please supply another email address'}, 400)

    model = UserModel(data)
    model.save()

    res_data = user_schema.dump(model).data
    return resource_response(res_data, API_CATEGORY, 201)


@user_api.route('/<string:uuid>', methods=['GET'])
def get_by_uuid(uuid):
    model = UserModel.get_by_uuid(uuid)
    if not model:
        return error_response({'error': 'user not found'}, 404)

    res_data = user_schema.dump(model).data
    return resource_response(res_data, API_CATEGORY, 200)


@user_api.route('/<string:uuid>', methods=['PUT'])
def update(uuid):
    req_data = request.get_json()
    data, error = user_schema.load(req_data, partial=True)
    if error:
        return error_response(error, 400)

    model = UserModel.get_by_uuid(uuid)
    if not model:
        return error_response({'error': 'user not found'}, 404)

    model.update(data)

    res_data = user_schema.dump(model).data
    return resource_response(res_data, API_CATEGORY, 200)


@user_api.route('/<string:uuid>', methods=['DELETE'])
def delete(uuid):
    model = UserModel.get_by_uuid(uuid)
    if not model:
        return error_response({'error': 'user not found'}, 404)

    model.delete()

    return empty_response(204)
