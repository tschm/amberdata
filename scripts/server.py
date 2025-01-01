from __future__ import annotations

import pandas as pd
from flask import Flask

from pyamber.enum import TimeInterval
from pyamber.flask_amberdata import amberdata

if __name__ == "__main__":
    app = Flask(__name__)
    app.config.from_pyfile("/amberdata/config/settings.cfg")
    amberdata.init_app(app)

    with app.app_context():
        assert amberdata.request.health

        for pair, data in amberdata.request.prices.latest(pair="eth"):
            print(pair)
            print(data)

        print(
            amberdata.request.prices.history(
                pair="eth_usd",
                time_interval=TimeInterval.DAYS,
                start_date=pd.Timestamp("2020-01-12"),
                end_date=pd.Timestamp("2020-01-13"),
            )
        )

        # assert False

        for exchange, data in amberdata.request.ohlcv.latest(
            "eth_usd", exchange="bitfinex,bitstamp,gdax,gemini,kraken,okex"
        ):
            print(exchange)
            print(data)

        for exchange, data in amberdata.request.ohlcv.history(
            "eth_usd",
            exchange="bitfinex,bitstamp",
            start_date=pd.Timestamp("2020-01-01"),
            end_date=pd.Timestamp("2020-02-13"),
            time_interval=TimeInterval.DAYS,
        ):
            print(exchange)
            print(data)

        # assert False

        for exchange, data in amberdata.request.bid_ask.latest("eth_usd", exchange="bitfinex,bitstamp"):
            print(exchange)
            print(data)

        for exchange, data in amberdata.request.bid_ask.history(
            "eth_usd",
            exchange="bitfinex,bitstamp",
            start_date=pd.Timestamp("2020-01-01"),
            end_date=pd.Timestamp("2020-01-02"),
        ):
            print(exchange)
            print(data)

        # for exchange, data in amberdata.request.exchanges(pair="eth_usd"):
        #    print(exchange)
        #    print(len(data))
