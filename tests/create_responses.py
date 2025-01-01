from __future__ import annotations

import logging
from io import StringIO

import pandas as pd
from flask import Flask

from pyamber.enum import TimeInterval
from pyamber.flask_amberdata import amberdata

if __name__ == "__main__":
    app = Flask(__name__)
    app.config.from_pyfile("/amberdata/config/settings.cfg")
    amberdata.init_app(app)

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    log = logging.getLogger("requests.packages.urllib3")  # works
    log.setLevel(logging.DEBUG)  # needed
    log.propagate = True

    # logging from urllib3 to console
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    log.addHandler(ch)

    with app.app_context():
        request = amberdata.request

        output = StringIO()
        for exchange, series in request.prices.latest(pair="eth_usd", logger=log):
            series.to_csv(output)
            print(output.getvalue())

        output = StringIO()
        y = request.prices.history(
            pair="eth_usd",
            start_date=pd.Timestamp("2020-02-12"),
            end_date=pd.Timestamp("2020-02-13"),
            logger=log,
            time_interval=TimeInterval.DAYS,
        )
        y.to_csv(output, header=True)
        print(output.getvalue())

        output = StringIO()
        for exchange, series in request.ohlcv.latest(pair="eth_usd", exchange="bitfinex", logger=log):
            series.to_csv(output, header=False)
            print(output.getvalue())

        output = StringIO()
        for exchange, series in request.bid_ask.latest(pair="eth_usd", exchange="bitfinex", logger=log):
            series.to_csv(output, header=False)
            print(output.getvalue())

        output = StringIO()
        for exchange, series in request.bid_ask.history(
            pair="eth_usd",
            exchange="bitfinex",
            start_date=pd.Timestamp("2020-02-12 23:50:00"),
            end_date=pd.Timestamp("2020-02-13"),
            logger=log,
        ):
            series.to_csv(output, header=True)
            print(output.getvalue())

        output = StringIO()
        for exchange, series in request.ohlcv.history(
            pair="eth_usd",
            exchange="bitfinex",
            start_date=pd.Timestamp("2020-01-01"),
            end_date=pd.Timestamp("2020-02-20"),
            time_interval=TimeInterval.DAYS,
            logger=log,
        ):
            series.to_csv(output, header=True)
            print(output.getvalue())

        output = StringIO()
        for exchange, data in request.features.exchanges(pair="eth_usd", logger=log):
            print(exchange)
            print(data)
