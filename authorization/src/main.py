from os import environ

from api.v1 import bp
from db.init import init_db
from ext.redis import RedisExtension
from flasgger import Swagger
from flask import Flask
from flask_marshmallow import Marshmallow
from werkzeug.utils import import_string

redis = RedisExtension()

app = Flask(__name__)
# instantiate config class to skip execution of SECRET_KEY related code at compile time
cfg = import_string(environ.get('AUTH_CONFIG', 'config.ProductionConfig'))()
app.config.from_object(cfg)

init_db(app)
redis.init_app(app)
ma = Marshmallow(app)
app.register_blueprint(bp)

swagger = Swagger(
    app,
    template={
        'swagger': '2.0',
        'info': {
            'title': 'Auth service',
            'version': '1.0',
        },
        'consumes': [
            'application/json',
        ],
        'produces': [
            'application/json',
        ],
    },
)
