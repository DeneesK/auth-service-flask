from api.v1.user import bp_user
from db.init import init_db
from flask import Flask

app = Flask(__name__)
init_db(app)
app.register_blueprint(bp_user)
