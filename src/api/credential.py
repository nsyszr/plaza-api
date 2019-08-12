# /src/api/credential.py

from flask import request, Blueprint
from ..models.credential import CredentialModel, credential_schema, credential_list_schema
from .utils import resource_response, empty_response, error_response

credential_api = Blueprint('credentials', __name__)

API_CATEGORY = 'credentials'
API_LIST_TYPE = 'CredentialListV1'

@credential_api.route('/', methods=['GET'])
def find_all():
    models = CredentialModel.find_all()

    res_data = credential_list_schema.dump(models).data
    return resource_response(res_data, API_CATEGORY, 200, many=True, type=API_LIST_TYPE)


@credential_api.route('/', methods=['POST'])
def create():
    req_data = request.get_json()
    data, error = credential_schema.load(req_data)

    if error:
        return error_response(error, 400)

    cred_in_db = CredentialModel.get_by_user_uuid(data.get('user_uuid'))
    if cred_in_db:
        return error_response({'error': 'Credential for given user already exist'}, 400)

    model = CredentialModel(data)
    model.save()

    res_data = credential_schema.dump(model).data
    return resource_response(res_data, API_CATEGORY, 201)


@credential_api.route('/<string:uuid>', methods=['GET'])
def get_by_uuid(uuid):
    model = CredentialModel.get_by_uuid(uuid)
    if not model:
        return error_response({'error': 'credential not found'}, 404)

    res_data = credential_schema.dump(model).data
    return resource_response(res_data, API_CATEGORY, 200)


@credential_api.route('/<string:uuid>', methods=['PUT'])
def update(uuid):
    req_data = request.get_json()
    data, error = credential_schema.load(req_data, partial=True)
    if error:
        return error_response(error, 400)

    model = CredentialModel.get_by_uuid(uuid)
    if not model:
        return error_response({'error': 'credential not found'}, 404)

    model.update(data)

    res_data = credential_schema.dump(model).data
    return resource_response(res_data, API_CATEGORY, 200)


@credential_api.route('/<string:uuid>', methods=['DELETE'])
def delete(uuid):
    model = CredentialModel.get_by_uuid(uuid)
    if not model:
        return error_response({'error': 'credential not found'}, 404)

    model.delete()

    return empty_response(204)
