from flask import Flask

from pyamber.flask_amberdata import amberdata

if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_envvar('APPLICATION_SETTINGS')
    amberdata.init_app(app)

    with app.app_context():
        response = amberdata.request.health


