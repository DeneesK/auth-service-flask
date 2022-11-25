from flask import Flask
from api.v1.user import bp_user
from db.init import init_db

app = Flask(__name__)
init_db(app)
app.register_blueprint(bp_user)
