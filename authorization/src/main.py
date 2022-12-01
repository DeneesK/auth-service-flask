from api.v1 import bp
from db.init import init_db
from flask import Flask
from flask_marshmallow import Marshmallow

app = Flask(__name__)
init_db(app)
ma = Marshmallow(app)
app.register_blueprint(bp)
