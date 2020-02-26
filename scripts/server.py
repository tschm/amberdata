import pandas as pd
from flask import Flask

from pyamber.flask_amberdata import amberdata
from pyamber.request import TimeInterval

if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_envvar('APPLICATION_SETTINGS')
    amberdata.init_app(app)

    with app.app_context():
        assert amberdata.request.health
        x = amberdata.request.price_history("eth_usd", timeInterval=TimeInterval.DAYS, startDate=pd.Timestamp("2020-01-12"), endDate=pd.Timestamp("2020-01-12"))
        print(x)

