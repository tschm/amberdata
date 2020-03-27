class Features_Request(object):
    def __init__(self, request):
        self.__request = request

    def exchanges(self, exchanges=None, pair=None, logger=None):
        url = "https://web3api.io/api/v2/market/exchanges"
        pair = pair or []
        exchanges = exchanges or []

        params = {"pair": pair, "exchange": exchanges}
        payload = self.__request.get(url=url, params=params, logger=logger)

        for exchange, data in payload.items():

            for pair, x in data.items():
                yield exchange, pair, x

            #if data[pair]["ticker"]["startDate"]:
            #    yield exchange, data


    def price_pairs(self, logger=None):
        # all price pairs on all exchanges
        url = "https://web3api.io/api/v2/market/prices/pairs"

        payload = self.__request.get(url=url, logger=logger)
        for pair in payload:
            yield pair

    def ohlcv_pairs(self, exchange=None, logger=None):
        # ohlcv data at a given exchange
        url = "https://web3api.io/api/v2/market/ohlcv/information"

        exchange = exchange or []
        params = {"exchange": exchange}

        payload = self.__request.get(url=url, params=params, logger=logger)

        for exchange, data in payload.items():
            for pair, dates in data.items():
                yield exchange, pair, dates

    def ticker_pairs(self, exchange=None, logger=None):
        url = "https://web3api.io/api/v2/market/tickers/information"
        exchange = exchange or []
        params = {"exchange": exchange}

        payload = self.__request.get(url=url, params=params, logger=logger)

        for exchange, data in payload.items():
            for pair, dates in data.items():
                yield exchange, pair, dates

    def pairs(self, exchange=None, pair=None, logger=None):
        url = "https://web3api.io/api/v2/market/pairs"

        pair = pair or []
        exchange = exchange or []

        params = {"exchange": exchange, "pair": pair}

        payload = self.__request.get(url=url, params=params, logger=logger)

        for exchange, data in payload.items():
            for pair, dates in data.items():
                yield pair, exchange, dates

    def trades(self, exchange=None, logger=None):
        url = "https://web3api.io/api/v2/market/trades/information"

        exchange = exchange or []

        params = {"exchange": exchange}
        payload = self.__request.get(url=url, params=params, logger=logger)

        for exchange, data in payload.items():
            for pair, data in data.items():
                yield pair, exchange, data