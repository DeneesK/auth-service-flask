from os import environ


class Config:
    FLASK_ENV = 'production'
    SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}/{3}'.format(
        environ.get('POSTGRES_USER'),
        environ.get('POSTGRES_PASSWORD'),
        environ.get('POSTGRES_HOST', '127.0.0.1'),
        environ.get('POSTGRES_DB', 'auth_database'),
    )
    REDIS_HOST = environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = environ.get('REDIS_PORT', 6379)
    TOKEN_ACCESS_TTL = 600  # in seconds
    TOKEN_REFRESH_TTL = 604800  # in seconds
    SWAGGER = {
        'title': 'Swagger JWT Authentiation App',
        'uiversion': 3,
        'doc_dir': './api/docs/',
    }


class ProductionConfig(Config):
    # wrap this in the method to execute runtime only
    # to avoid key error if dev config used
    @property
    def SECRET_KEY(self):
        # don't use environ.get() method here
        # to fail loud without secret key on production
        return environ['SECRET_KEY']

    # wrap this in the method to execute runtime only
    # to avoid key error if dev config used
    @property
    def TOKEN_SECRET_KEY(self):
        # don't use environ.get() method here
        # to fail loud without secret key on production
        return environ['TOKEN_SECRET_KEY']


class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    SECRET_KEY = 'flask_secret_key'
    TOKEN_SECRET_KEY = 'secret_key_for_token_encoding'


class TestingConfig(DevelopmentConfig):
    TESTING = True
