"""To connect, use http://, not https://"""
from flask import Flask
# from db.init import init_db # doesn't work yet
from gevent import monkey
monkey.patch_all()

from gevent.pywsgi import WSGIServer

app = Flask(__name__)


@app.route('/create-user')
def create_user():
    """Accept login and password here, post method"""
    return 'Create user+'


def main():
    # init_db(app)
    # app.run()
    http_server = WSGIServer(('127.0.0.1', 5000), app)
    http_server.serve_forever()


if __name__ == '__main__':
    main()
