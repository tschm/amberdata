import pytest
from flask import Flask
#from pyamber.flask_amberdata import amberdata
from pyamber.flask_amberdata import amberdata


@pytest.fixture
def amber_request():
    # there's no need to expose the entire client...

    app = Flask(__name__)
    # initialize the config of the app object
    app.config.from_pyfile('config/settings.cfg')

    # move into the app context and initialize the amberdata project
    with app.app_context():
        amberdata.init_app(app)
        yield amberdata.request