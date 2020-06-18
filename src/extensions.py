from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_httpauth import HTTPBasicAuth
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
jwt = JWTManager()
auth = HTTPBasicAuth()
ma = Marshmallow()
b_crypt = Bcrypt()
BLACKLIST = set()


"""
    / ** ** ** ** ** ** ** ** / / / JWT SETTINGS / ** ** ** ** ** ** ** ** /
"""


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST
