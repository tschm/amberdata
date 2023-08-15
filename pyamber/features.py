from __future__ import annotations

from collections import namedtuple

Feature = namedtuple("Feature", "exchange pair data")


class Features_Request:
    def __init__(self, request):
        self.__request = request

    def exchanges(self, exchanges=None, pair=None, logger=None):
        raise NotImplementedError("Please use the function 'pairs'")

    def price_pairs(self, logger=None):
        # all price pairs on all exchanges
        url = "https://web3api.io/api/v2/market/prices/pairs"

        payload = self.__request.get(url=url, logger=logger)
        yield from payload

    def ohlcv_pairs(self, exchange=None, logger=None):
        # ohlcv data at a given exchange
        url = "https://web3api.io/api/v2/market/ohlcv/information"

        exchange = exchange or []
        params = {"exchange": exchange}

        payload = self.__request.get(url=url, params=params, logger=logger)

        for exchange, x in payload.items():
            for pair, data in x.items():
                yield Feature(exchange=exchange, pair=pair, data=data)

    def ticker_pairs(self, exchange=None, logger=None):
        url = "https://web3api.io/api/v2/market/tickers/information"
        exchange = exchange or []
        params = {"exchange": exchange}

        payload = self.__request.get(url=url, params=params, logger=logger)

        for exchange, x in payload.items():
            for pair, data in x.items():
                yield Feature(exchange=exchange, pair=pair, data=data)

    def pairs(self, exchange=None, pair=None, logger=None):
        url = "https://web3api.io/api/v2/market/pairs"

        pair = pair or []
        exchange = exchange or []

        params = {"exchange": exchange, "pair": pair}

        payload = self.__request.get(url=url, params=params, logger=logger)

        for pair, x in payload.items():
            for exchange, data in x.items():
                yield Feature(pair=pair, exchange=exchange, data=data)

    def trades(self, exchange=None, logger=None):
        url = "https://web3api.io/api/v2/market/trades/information"

        exchange = exchange or []

        params = {"exchange": exchange}
        payload = self.__request.get(url=url, params=params, logger=logger)

        for exchange, x in payload.items():
            for pair, data in x.items():
                yield Feature(pair=pair, exchange=exchange, data=data)
