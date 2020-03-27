import pandas as pd
from flask import Flask

from pyamber.flask_amberdata import amberdata


if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_pyfile('/amberdata/config/settings.cfg')
    amberdata.init_app(app)

    with app.app_context():
        for exchange, pair, data in amberdata.request.features.exchanges(pair="btc_usd"):
            print(exchange, pair, data)

        for exchange, pair, dates in amberdata.request.features.ohlcv_pairs():
            print(exchange, pair, dates)

        for pair, exchange, data in amberdata.request.features.pairs(pair="btc_usd"):
            print(pair, exchange, data)

        for pair in amberdata.request.features.price_pairs():
            print(pair)

        for exchange, pair, data in amberdata.request.features.ticker_pairs(exchange="bitfinex"):
            print(exchange, pair, data)

        for exchange, pair, data in amberdata.request.features.trades(exchange="bitfinex"):
            print(exchange, pair, data)


