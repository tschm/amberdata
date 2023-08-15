from __future__ import annotations

from flask import Flask, current_app

from pyamber.request import AmberRequest


class InvalidSettingsError(Exception):
    pass


class Amberdata:
    """Main class used for initialization of Flask-Amberdata."""

    def __init__(self, app=None, config=None):
        self.app = None
        if app is not None:
            self.init_app(app, config)

    @staticmethod
    def __create_request(config):
        """
        Given Flask application's config dict, extract relevant config vars
        out of it and establish Amberdata's requests based on them.
        """
        # Validate that the config is a dict
        if config is None or not isinstance(config, dict):
            raise InvalidSettingsError("Invalid application configuration")

        # Otherwise, return a single connection
        return AmberRequest(key=config["AMBERDATA"]["x-api-key"])

    def init_app(self, app, config=None):
        if not app or not isinstance(app, Flask):
            raise Exception("Invalid Flask application instance")

        self.app = app

        app.extensions = getattr(app, "extensions", {})

        if "amberdata" not in app.extensions:
            app.extensions["amberdata"] = {}

        if self in app.extensions["amberdata"]:
            # Raise an exception if extension already initialized as
            # potentially new configuration would not be loaded.
            raise Exception("Extension already initialized")

        if not config:
            # If not passed a config then we read the connection settings
            # from the app config.
            config = app.config

        # Obtain db connection(s)
        requests = Amberdata.__create_request(config)

        # Store objects in application instance so that multiple apps do not
        # end up accessing the same objects.
        s = {"app": app, "request": requests}
        app.extensions["amberdata"][self] = s

    @property
    def request(self):
        """
        Return Amberdata request associated with this flask instance.
        """
        return current_app.extensions["amberdata"][self]["request"]


amberdata = Amberdata()
