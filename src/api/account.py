# /src/api/credential.py

from flask import request, Blueprint
from ..models.account import AccountModel, account_schema, account_list_schema
from .utils import resource_response, empty_response, error_response

account_api = Blueprint('accounts', __name__)

API_CATEGORY = 'accounts'
API_LIST_TYPE = 'AccountListV1'

@account_api.route('/', methods=['GET'])
def find_all():
    models = AccountModel.find_all()

    res_data = account_list_schema.dump(models).data
    return resource_response(res_data, API_CATEGORY, 200, many=True, type=API_LIST_TYPE)


@account_api.route('/', methods=['POST'])
def create():
    req_data = request.get_json()
    data, error = account_schema.load(req_data)

    if error:
        return error_response(error, 400)

    # cred_in_db = AccountModel.get_by_user_uuid(data.get('user_uuid'))
    # if cred_in_db:
    #    return error_response({'error': 'Credential for given user already exist'}, 400)

    model = AccountModel(data)
    model.save()

    res_data = account_schema.dump(model).data
    return resource_response(res_data, API_CATEGORY, 201)


@account_api.route('/<string:uuid>', methods=['GET'])
def get_by_uuid(uuid):
    model = AccountModel.get_by_uuid(uuid)
    if not model:
        return error_response({'error': 'credential not found'}, 404)

    res_data = account_schema.dump(model).data
    return resource_response(res_data, API_CATEGORY, 200)


@account_api.route('/<string:uuid>', methods=['PUT'])
def update(uuid):
    req_data = request.get_json()
    data, error = account_schema.load(req_data, partial=True)
    if error:
        return error_response(error, 400)

    model = AccountModel.get_by_uuid(uuid)
    if not model:
        return error_response({'error': 'credential not found'}, 404)

    model.update(data)

    res_data = account_schema.dump(model).data
    return resource_response(res_data, API_CATEGORY, 200)


@account_api.route('/<string:uuid>', methods=['DELETE'])
def delete(uuid):
    model = AccountModel.get_by_uuid(uuid)
    if not model:
        return error_response({'error': 'credential not found'}, 404)

    model.delete()

    return empty_response(204)
