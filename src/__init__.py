import os
import logging
from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from logging.handlers import WatchedFileHandler
from src.extensions import (
    db,
    jwt,
    ma,
    b_crypt,
    BLACKLIST,
    oauth
)
from src.commands import create_tables
from src.resources.user import (
    UserRegister,
    UserList,
    UserLogin,
    User,
    Content,
    UserLogout,
    TokenRefresher,
    UserEmail2FA
)
from src.resources.oauth import (
    GithubLogin,
    GithubAuthorize
)
from src.resources.confirmation import Confirmation
from src.resources.posts import CreatePost
from src.configurations import DevelopmentConfig, ProductionConfig, TestingConfig
from dotenv import load_dotenv


def create_app(config_class='configurations.py'):
    app = Flask(__name__)
    app.config.from_object(ProductionConfig)
    load_dotenv()
    jwt.init_app(app)
    api = Api(app)
    db.init_app(app)
    app.cli.add_command(create_tables)  # To interact with app from CLI
    b_crypt.init_app(app)
    ma.init_app(app)
    migrate = Migrate(app, db)
    oauth.init_app(app)

    # USER API
    api.add_resource(UserRegister, '/users/register')
    api.add_resource(UserLogin, '/users/login')
    api.add_resource(UserLogout, '/users/logout')
    api.add_resource(User, '/user/<int:_id>')
    api.add_resource(UserList, '/users/<int:limit>')
    api.add_resource(TokenRefresher, '/users/refreshing')
    api.add_resource(UserEmail2FA, '/users/fa2_auth/<string:token>')

    # OAuth API
    api.add_resource(GithubLogin, "/login/oauth/github")
    api.add_resource(GithubAuthorize, "/login/oauth/github/authorized")

    # CONFIRMATION API
    api.add_resource(Confirmation, '/user_id/<string:confirmation_id>')

    # resources.add_resource(User, '/users/<int:user_id>')
    api.add_resource(CreatePost, '/posts/create')
    api.add_resource(Content, '/content')

    # Logging
    log_level = logging.INFO if app.config['DEBUG'] else logging.ERROR
    handler = WatchedFileHandler('server.log')
    formatter = logging.Formatter('%(asctime)s | %(levelname)s: %(message)s',
                                  '%d-%m-%Y %H:%M:%S')
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(log_level)
    root.addHandler(handler)
    logging.info('\n------------------- Starting Server -------------------')

    return app
