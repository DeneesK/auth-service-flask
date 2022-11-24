import os

from flask import Flask

from .orm import db_engine


def init_db(app: Flask):
    username = os.environ.get('POSTGRES_USERNAME')
    password = os.environ.get('POSTGRES_PASSWORD')
    host = os.environ.get('POSTGRES_HOST', '127.0.0.1')
    db_name = os.environ.get('POSTGRES_DBNAME', 'auth_database')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username}:{password}@{host}/{db_name}'
    print("init_db")
    db_engine.init_app(app)
    app.app_context().push()

    db_engine.create_all()

    db_engine.session.commit()


