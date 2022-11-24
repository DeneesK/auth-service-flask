from flask import Flask

def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username}:{password}@{host}/{db_name}'
    print("init_db")
    db.init_app(app)
