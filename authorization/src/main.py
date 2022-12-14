from os import environ
from logging.config import dictConfig

from api.v1 import bp
from core.flask import Flask
from db.init import init_db
from ext.redis import RedisExtension
from flasgger import Swagger
from flask_marshmallow import Marshmallow
from werkzeug.utils import import_string

redis = RedisExtension()

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://sys.stdout',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

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
