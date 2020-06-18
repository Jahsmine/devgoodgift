from src import create_app
from src.extensions import db, jwt, BLACKLIST
from libs.serving import set_localization
from flask_jwt_extended import create_access_token

app = create_app()


@app.before_first_request
def create_all():
    db.create_all()


set_localization('ru-ru')
app.run()
