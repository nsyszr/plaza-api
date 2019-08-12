# src/models/user.py

import datetime
import sqlalchemy
from marshmallow import fields, Schema
from sqlalchemy.dialects.postgresql import UUID
from . import db
from .organisation import OrganisationSchema
from .credential import CredentialSchema

class UserModel(db.Model):
    __tablename__ = 'users'

    uuid = db.Column('id', UUID(as_uuid=True), primary_key=True,
                     server_default=sqlalchemy.text('uuid_generate_v4()'))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    username = db.Column(db.String(320), nullable=False)
    email_address = db.Column(db.String(320), unique=True, nullable=False)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text, nullable=False)
    phone_number = db.Column(db.Text)
    preferred_language = db.Column(db.String(5), default='en_US')
    registered_at = db.Column(db.DateTime)
    confirmation_code = db.Column(db.String(32))
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    organisation_uuid = db.Column('organisation_id', UUID(), db.ForeignKey('organisations.id'), nullable=False)
    organisation = db.relationship('OrganisationModel', back_populates='users', lazy=True)
    credential = db.relationship("CredentialModel", uselist=False, back_populates="user")

    # class constructor
    def __init__(self, data):
        self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()

        self.username = data.get('username')
        self.email_address = data.get('email_address')
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')
        self.phone_number = data.get('phone_number')
        self.preferred_language = data.get('preferred_language')
        self.registered_at = data.get('registered_at')
        self.confirmation_code = data.get('confirmation_code')
        self.is_confirmend = data.get('is_confirmend')
        self.organisation_uuid = data.get('organisation_uuid')

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
        return UserModel.query.all()

    # @staticmethod
    # def find_by_organisation_uuid(value):
    #    return UserModel.query.filter_by(organisation_uuid=value)

    @staticmethod
    def get_by_uuid(uuid):
        return UserModel.query.get(uuid)

    @staticmethod
    def get_by_email_address(value):
        return UserModel.query.filter_by(email_address=value).first()

    def __repr(self):
        return '<uuid {}>'.format(self.uuid)


class UserSchema(Schema):
    _type = fields.Str('UserV1', dump_to='type', dump_only=True)

    uuid = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_to='createdAt', dump_only=True)
    updated_at = fields.DateTime(dump_to='updatedAt', dump_only=True)

    username = fields.Str(required=True)
    email_address = fields.Email(dump_to='emailAddress', load_from='emailAddress', required=True)
    first_name = fields.Str(dump_to='firstName', load_from='firstName')
    last_name = fields.Str(dump_to='lastName', load_from='lastName', required=True)
    phone_number = fields.Str(dump_to='phoneNumber', load_from='phoneNumber')
    preferred_language = fields.Str(dump_to='preferredLanguage', load_from='preferredLanguage')
    registered_at = fields.DateTime(dump_to='registeredAt', dump_only=True)
    organisation_uuid = fields.Str(dump_to='organisationUuid', load_from='organisationUuid', required=True)
    organisation = fields.Nested(OrganisationSchema, dump_only=True)
    credential = fields.Nested(CredentialSchema, dump_only=True)


user_schema = UserSchema()
user_list_schema = UserSchema(many=True, exclude=['organisation', 'credential'])
