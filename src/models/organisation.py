# src/models/organisation.py

import datetime
import sqlalchemy
from marshmallow import fields, Schema
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import or_
from . import db

ROLE_PLATFORM_OPERATOR = 'PLATFORM_OPERATOR'
ROLE_CUSTOMER = 'CUSTOMER'
ROLE_SUPPLIER = 'SUPPLIER'
ROLE_RESELLER = 'RESELLER'
ROLE_BROKER = 'BROKER'

class OrganisationModel(db.Model):
    __tablename__ = 'organisations'
    __table_args__ = (
        db.UniqueConstraint('name', 'country_code', name='unique_organisation_name_and_country_code'),
    )

    uuid = db.Column('id', UUID(as_uuid=True), primary_key=True,
                     server_default=sqlalchemy.text('uuid_generate_v4()'))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    name = db.Column(db.Text, nullable=False)
    roles = db.Column(ARRAY(db.Text))
    supplier_uuid = db.Column(UUID(), db.ForeignKey('organisations.id'))
    email_address = db.Column(db.String(320))
    customer_number = db.Column(db.Text)
    phone_number = db.Column(db.Text)
    address1 = db.Column(db.Text)
    address2 = db.Column(db.Text)
    postal_code = db.Column(db.String(10))
    city = db.Column(db.Text, nullable=False)
    state = db.Column(db.Text)
    country_code = db.Column(db.String(2), nullable=False)
    is_validated = db.Column(db.Boolean, nullable=False, default=False)
    users = db.relationship('UserModel', back_populates='organisation', lazy=True)
    accounts = db.relationship('AccountModel', back_populates='organisation', lazy=True)
    customers = db.relationship('OrganisationModel', lazy=True)
    # db.relationship('UserModel', backref='organisations', lazy=True)

    # class constructor
    def __init__(self, data):
        self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()

        self.name = data.get('name')
        self.roles = data.get('roles')
        if not self.roles:
            self.roles = list()
        if ROLE_CUSTOMER not in self.roles:
            self.roles.append(ROLE_CUSTOMER)
        self.supplier_uuid = data.get('supplier_uuid')
        self.email_address = data.get('email_address')
        self.customer_number = data.get('customer_number')
        self.phone_number = data.get('phone_number')
        self.address1 = data.get('address1')
        self.address2 = data.get('address2')
        self.postal_code = data.get('postal_code')
        self.city = data.get('city')
        self.state = data.get('state')
        self.country_code = data.get('country_code')
        self.is_validated = data.get('is_validated')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.updated_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def find_all():
        return OrganisationModel.query.all()

    @staticmethod
    def find_suppliers():
        return OrganisationModel.query.filter(
            or_(OrganisationModel.roles.any('PLATFORM_OPERATOR'),
                OrganisationModel.roles.any('SUPPLIER'))).all()

    @staticmethod
    def get_by_uuid(uuid):
        return OrganisationModel.query.get(uuid)

    @staticmethod
    def get_by_name_and_country_code(name, country_code):
        return OrganisationModel.query.filter_by(name=name, country_code=country_code,).first()

    def __repr(self):
        return '<uuid {}>'.format(self.uuid)


class OrganisationSchema(Schema):
    _type = fields.Str('OrganisationV1', dump_to='type', dump_only=True)

    uuid = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_to='createdAt', dump_only=True)
    updated_at = fields.DateTime(dump_to='updatedAt', dump_only=True)

    name = fields.Str(required=True)
    roles = fields.List(fields.Str())
    supplier_uuid = fields.Str(dump_to='supplierUuid', load_from='supplierUuid', required='True')
    email_address = fields.Email(dump_to='emailAddress', load_from='emailAddress', allow_none=True)
    customer_number = fields.Str(dump_to='customerNumber', load_from='customerNumber', allow_none=True)
    phone_number = fields.Str(dump_to='phoneNumber', load_from='phoneNumber', allow_none=True)
    address1 = fields.Str(allow_none=True)
    address2 = fields.Str(allow_none=True)
    postal_code = fields.Str(dump_to='postalCode', load_from='postalCode', allow_none=True)
    city = fields.Str(required=True)
    state = fields.Str(allow_none=True)
    country_code = fields.Str(dump_to='countryCode', load_from='countryCode', required=True)
    is_validated = fields.Bool(dump_to='validated', load_from='validated')


organisation_schema = OrganisationSchema()
organisation_list_schema = OrganisationSchema(many=True)
