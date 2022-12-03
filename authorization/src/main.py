from api.v1 import bp
from db.init import init_db
from flask import Flask
from flasgger import Swagger
from flask_marshmallow import Marshmallow

app = Flask(__name__)
init_db(app)
ma = Marshmallow(app)
app.register_blueprint(bp)

swagger = Swagger(
    app,
    template={
        "swagger": "2.0",
        "info": {
            "title": "Auth service",
            "version": "1.0",
        },
        "consumes": [
            "application/json",
        ],
        "produces": [
            "application/json",
        ],
    },
)

app.config["SWAGGER"] = {
    "title": "Swagger JWT Authentiation App",
    "uiversion": 3,
    'doc_dir': './api/docs/'
}
