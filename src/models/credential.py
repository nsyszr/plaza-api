# src/models/credential.py

import datetime
import sqlalchemy
from marshmallow import fields, Schema
from sqlalchemy.dialects.postgresql import UUID
from . import db, bcrypt

class CredentialModel(db.Model):
    __tablename__ = 'credentials'

    uuid = db.Column('id', UUID(as_uuid=True), primary_key=True,
                     server_default=sqlalchemy.text('uuid_generate_v4()'))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    user_uuid = db.Column('user_id', UUID(), db.ForeignKey('users.id'), unique=True, nullable=False)
    user = db.relationship('UserModel', back_populates="credential")
    password = db.Column(db.Text, nullable=False)
    password_set_at = db.Column(db.DateTime)
    is_locked = db.Column(db.Boolean, nullable=False, default=False)
    is_expired = db.Column(db.Boolean, nullable=False, default=False)
    last_login_at = db.Column(db.DateTime)
    last_logout_at = db.Column(db.DateTime)
    user_info_last_login_at = db.Column(db.DateTime)
    user_info_last_login_failed_at = db.Column(db.DateTime)
    user_info_last_login_failed_count = db.Column(db.Integer)

    # class constructor
    def __init__(self, data):
        self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()

        self.user_uuid = data.get('user_uuid')
        self.password = data.get('password')
        self.password_set_at = data.get('password_set_at')
        self.is_locked = data.get('is_locked')
        self.is_expired = data.get('is_expired')
        self.last_login_at = data.get('last_login_at')
        self.last_logout_at = data.get('last_logout_at')
        self.user_info_last_login_at = data.get('user_info_last_login_at')
        self.user_info_last_login_failed_at = data.get('user_info_last_login_failed_at')
        self.user_info_last_login_failed_count = data.get('user_info_last_login_failed_count')

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
        return CredentialModel.query.all()

    @staticmethod
    def get_by_uuid(uuid):
        return CredentialModel.query.get(uuid)

    @staticmethod
    def get_by_user_uuid(user_uuid):
        return CredentialModel.query.filter_by(user_uuid=user_uuid).first()

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode('utf-8')

    def check_hash(self, password):
        '''checks given password against stored password hash'''
        return bcrypt.check_password_hash(self.password, password)

    def __repr(self):
        return '<uuid {}>'.format(self.uuid)


class CredentialSchema(Schema):
    _type = fields.Str('CredentialV1', dump_to='type', dump_only=True)

    uuid = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_to='createdAt', dump_only=True)
    updated_at = fields.DateTime(dump_to='updatedAt', dump_only=True)

    user_uuid = fields.Str(dump_to='userUuid', load_from='userUuid', required=True)
    password = fields.Str(load_only=True)
    password_set_at = fields.DateTime(dump_to='passwordSetAt', dump_only=True)
    is_locked = fields.Email(dump_to='locked', load_from='locked')
    is_expired = fields.Email(dump_to='expired', load_from='expired')
    last_login_at = fields.DateTime(dump_to='lastLoginAt', dump_only=True)
    last_logout_at = fields.DateTime(dump_to='lastLogoutAt', dump_only=True)
    user_info_last_login_at = fields.DateTime(dump_to='userInfoLastLoginAt', dump_only=True)
    user_info_last_login_failed_at = fields.DateTime(dump_to='userInfoLastLoginFailedAt', dump_only=True)
    user_info_last_login_failed_count = fields.DateTime(dump_to='userInfoLastLoginFailedCount', dump_only=True)


credential_schema = CredentialSchema()
credential_list_schema = CredentialSchema(many=True)
