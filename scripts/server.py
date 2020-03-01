import pandas as pd
from flask import Flask

from pyamber.flask_amberdata import amberdata
from pyamber.request import TimeInterval

if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_pyfile('/amberdata/config/settings.cfg')
    amberdata.init_app(app)

    with app.app_context():
        assert amberdata.request.health

        #for pair, data in amberdata.request.prices.latest(pair="eth"):
        #    print(pair)
        #    print(data)

        #print(amberdata.request.prices.history(pair="eth_usd", timeInterval=TimeInterval.DAYS,
        #                                       startDate=pd.Timestamp("2020-01-12"),
        #                                       endDate=pd.Timestamp("2020-01-13")))

        # for exchange, data in amberdata.request.ohlcv.latest("eth_usd", exchange="bitfinex,bitstamp,gdax,gemini,kraken,okex"):
        #     print(exchange)
        #     print(data)
        #
        # for exchange, data in amberdata.request.ohlcv.history("eth_usd", exchange="bitfinex,bitstamp", startDate=pd.Timestamp("2020-01-12"),endDate=pd.Timestamp("2020-01-13")):
        #     print(exchange)
        #     print(data)

        #for exchange, data in amberdata.request.bid_ask.latest("eth_usd", exchange="bitfinex,bitstamp"):
        #    print(exchange)
        #    print(data)

        for exchange, data in amberdata.request.ohlcv.hh("eth_usd", exchange="bitfinex,bitstamp", startDate=pd.Timestamp("2019-01-01"),endDate=pd.Timestamp("2019-07-01"), timeInterval=TimeInterval.DAYS, max=86400*1000*20):
            print(exchange)
            print(data)

        #for exchange, data in amberdata.request.exchanges(pair="eth_usd"):
        #    print(exchange)
        #    print(len(data))
