from flask import Flask
# from db.init import init_db # doesn't work yet

app = Flask(__name__)


@app.route('/create-user')
def create_user():
    """Accept login and password here, post method"""
    return 'Create user'


def main():
    # init_db(app)
    app.run()


if __name__ == '__main__':
    main()
