from flask import Flask

from .orm import db_engine


def init_db(app: Flask):
    db_engine.init_app(app)
    app.app_context().push()

    db_engine.create_all()

    db_engine.session.commit()
