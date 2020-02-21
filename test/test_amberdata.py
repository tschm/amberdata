from pyamber.flask_amberdata import amberdata
from test.settings import client


def test_health(client):
    assert amberdata.request.health
