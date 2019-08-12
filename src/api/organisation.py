# /src/api/organisation.py

from flask import request, Blueprint
from ..models.organisation import OrganisationModel, organisation_schema, organisation_list_schema
from ..models.user import user_list_schema
from .utils import resource_response, empty_response, error_response
from .user import API_LIST_TYPE as API_USER_LIST_TYPE

organisation_api = Blueprint('organisations', __name__)

API_CATEGORY = 'organisations'
API_LIST_TYPE = 'OrganisationListV1'

@organisation_api.route('/', methods=['GET'])
def find_all():
    suppliers_only = request.args.get('suppliersOnly')
    models = []

    if suppliers_only:
        models = OrganisationModel.find_suppliers()
    else:
        models = OrganisationModel.find_all()

    res_data = organisation_list_schema.dump(models).data
    return resource_response(res_data, API_CATEGORY, 200, many=True, type=API_LIST_TYPE)


@organisation_api.route('/', methods=['POST'])
def create():
    req_data = request.get_json()
    data, error = organisation_schema.load(req_data)

    if error:
        return error_response(error, 400)

    org_in_db = OrganisationModel.get_by_name_and_country_code(data.get('name'), data.get('country_code'))
    if org_in_db:
        return error_response({'error': 'Organisation already exist, please supply another name'}, 400)

    model = OrganisationModel(data)
    model.save()

    res_data = organisation_schema.dump(model).data
    return resource_response(res_data, API_CATEGORY, 201)


@organisation_api.route('/<string:uuid>', methods=['GET'])
def get_by_uuid(uuid):
    model = OrganisationModel.get_by_uuid(uuid)
    if not model:
        return error_response({'error': 'organisation not found'}, 404)

    res_data = organisation_schema.dump(model).data
    return resource_response(res_data, API_CATEGORY, 200)

@organisation_api.route('/<string:uuid>/users', methods=['GET'])
def get_users(uuid):
    model = OrganisationModel.get_by_uuid(uuid)
    if not model:
        return error_response({'error': 'organisation not found'}, 404)

    res_data = user_list_schema.dump(model.users).data
    return resource_response(res_data, API_CATEGORY, 200, many=True, type=API_USER_LIST_TYPE)

@organisation_api.route('/<string:uuid>/customers', methods=['GET'])
def get_customers(uuid):
    model = OrganisationModel.get_by_uuid(uuid)
    if not model:
        return error_response({'error': 'organisation not found'}, 404)

    res_data = organisation_list_schema.dump(model.customers).data
    return resource_response(res_data, API_CATEGORY, 200, many=True, type=API_LIST_TYPE)

@organisation_api.route('/<string:uuid>', methods=['PUT'])
def update(uuid):
    req_data = request.get_json()
    print("req_data=", req_data)
    data, error = organisation_schema.load(req_data, partial=True)
    if error:
        print("error=", error)
        return error_response(error, 400)

    model = OrganisationModel.get_by_uuid(uuid)
    if not model:
        return error_response({'error': 'organisation not found'}, 404)

    model.update(data)

    res_data = organisation_schema.dump(model).data
    return resource_response(res_data, API_CATEGORY, 200)


@organisation_api.route('/<string:uuid>', methods=['DELETE'])
def delete(uuid):
    model = OrganisationModel.get_by_uuid(uuid)
    if not model:
        return error_response({'error': 'organisation not found'}, 404)

    model.delete()

    return empty_response(204)
