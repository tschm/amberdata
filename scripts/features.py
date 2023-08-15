from __future__ import annotations

from flask import Flask

from pyamber.flask_amberdata import amberdata

if __name__ == "__main__":
    app = Flask(__name__)
    app.config.from_pyfile("/amberdata/config/settings.cfg")
    amberdata.init_app(app)

    with app.app_context():
        # for exchange, pair, dates in amberdata.request.features.ohlcv_pairs():
        #    print(exchange, pair, dates)

        for feature in amberdata.request.features.pairs():
            print(feature)

        for pair in amberdata.request.features.price_pairs():
            print(pair)

        for feature in amberdata.request.features.ticker_pairs(exchange="bitfinex"):
            print(feature)

        for feature in amberdata.request.features.trades(exchange="bitfinex"):
            print(feature)
