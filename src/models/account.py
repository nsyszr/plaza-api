# src/models/account.py

import datetime
import sqlalchemy
from marshmallow import fields, Schema
from sqlalchemy.dialects.postgresql import UUID
from . import db
from .organisation import OrganisationSchema

class AccountModel(db.Model):
    __tablename__ = 'accounts'
    __table_args__ = (
        db.UniqueConstraint('name', 'organisation_id', name='unique_account_name_and_organisation_id'),
    )

    uuid = db.Column('id', UUID(as_uuid=True), primary_key=True,
                     server_default=sqlalchemy.text('uuid_generate_v4()'))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    name = db.Column(db.Text, nullable=False, default='Default Account')
    organisation_uuid = db.Column('organisation_id', UUID(), db.ForeignKey('organisations.id'), nullable=False)
    organisation = db.relationship('OrganisationModel', back_populates='accounts', lazy=True)
    # credential = db.relationship("CredentialModel", uselist=False, back_populates="user")

    # class constructor
    def __init__(self, data):
        self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()

        self.name = data.get('name')
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
        return AccountModel.query.all()

    @staticmethod
    def get_by_uuid(uuid):
        return AccountModel.query.get(uuid)

    def __repr(self):
        return '<uuid {}>'.format(self.uuid)


class AccountSchema(Schema):
    _type = fields.Str('AccountV1', dump_to='type', dump_only=True)

    uuid = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_to='createdAt', dump_only=True)
    updated_at = fields.DateTime(dump_to='updatedAt', dump_only=True)

    name = fields.Str()
    organisation_uuid = fields.Str(dump_to='organisationUuid', load_from='organisationUuid', required=True)
    organisation = fields.Nested(OrganisationSchema, dump_only=True)
    # credential = fields.Nested(CredentialSchema, dump_only=True)


account_schema = AccountSchema()
account_list_schema = AccountSchema(many=True, exclude=['organisation'])
