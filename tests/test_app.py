from __future__ import annotations

import pytest

from pyamber.flask_amberdata import Amberdata, InvalidSettingsError, amberdata


def test_app_false(app):
    # move into the app context and initialize the amberdata project
    with pytest.raises(Exception):
        with app.app_context():
            amberdata.init_app(None)


def test_init_amberdata(app):
    a = Amberdata(app=app)
    assert a

    # you need to be in the correct context to use a.request
    with pytest.raises(RuntimeError):
        assert a.request

    with app.app_context():
        assert a.request


def test_incorrect_config(app):
    # config has to be a dictionary
    with pytest.raises(InvalidSettingsError):
        Amberdata(app=app, config=[5.0])


def test_initapp_double(app):
    a = Amberdata(app=app)
    with pytest.raises(Exception):
        a.init_app(app=app)
