from flask import Flask
from gevent import monkey
from gevent.pywsgi import WSGIServer
from api.v1.user import bp_user
from db.init import init_db

monkey.patch_all()

app = Flask(__name__)
app.register_blueprint(bp_user)

def main():
    init_db(app)
    http_server = WSGIServer(('127.0.0.1', 5000), app)
    http_server.serve_forever()

if __name__ == '__main__':
    main()
