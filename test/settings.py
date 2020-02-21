import pytest
from flask import Flask
from pyamber.flask_amberdata import amberdata


@pytest.fixture
def client():
    app = Flask(__name__)
    # initialize the config of the app object
    app.config.from_envvar('APPLICATION_SETTINGS')

    # move into the app context and initialize the amberdata project
    with app.app_context():
        amberdata.init_app(app)
        yield app.test_client()
        # you could do some clean ups here...
        # ...
