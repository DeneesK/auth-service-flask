"""To connect, use http://, not https://"""
from flask import Flask
# from db.init import init_db # doesn't work yet
from gevent import monkey
from gevent.pywsgi import WSGIServer
from api.v1.user import bp_user

monkey.patch_all()


app = Flask(__name__)
app.register_blueprint(bp_user)
# for debug:
print(app.url_map)


def main():
    # init_db(app)
    # app.run()
    http_server = WSGIServer(('127.0.0.1', 5000), app)
    http_server.serve_forever()


if __name__ == '__main__':
    main()
