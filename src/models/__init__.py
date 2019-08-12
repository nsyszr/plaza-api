# src/models/__init__.py

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# initialize our db
db = SQLAlchemy()
bcrypt = Bcrypt()

from .user import UserModel, UserSchema  # noqa: E402,F401
from .credential import CredentialModel, CredentialSchema  # noqa: E402,F401
from .organisation import OrganisationModel, OrganisationSchema  # noqa: E402,F401
