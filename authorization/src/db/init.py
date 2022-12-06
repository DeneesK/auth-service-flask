import os

from flask import Flask

from .orm import db_engine


def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{0}:{1}@{2}/{3}'.format(
        os.environ.get('POSTGRES_USER'),
        os.environ.get('POSTGRES_PASSWORD'),
        os.environ.get('POSTGRES_HOST', '127.0.0.1'),
        os.environ.get('POSTGRES_DB'),
    )
    db_engine.init_app(app)
    app.app_context().push()

    db_engine.create_all()

    db_engine.session.commit()
