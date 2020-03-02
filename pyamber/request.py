import requests
from pyamber.markets import OHLCV_Request, Price_Request, BidAsk_Request


class AmberRequest(object):
    def __init__(self, key):
        self.__key = key

    @property
    def prices(self):
        return Price_Request(request=self)

    @property
    def ohlcv(self):
        return OHLCV_Request(request=self)

    @property
    def bid_ask(self):
        return BidAsk_Request(request=self)

    @property
    def headers(self):
        return {"accept": "application/json", "x-api-key": self.__key}

    def get(self, url, params=None):
        response = requests.get(url=url, params=params, headers=self.headers)
        # check that the response is ok
        response.raise_for_status()
        return response.json()["payload"]

    @property
    def health(self):
        return requests.get(url="https://web3api.io/health")

    def exchanges(self, pair=None):
        url = "https://web3api.io/api/v2/market/exchanges"
        pair = pair or []

        params = {"pair": pair}
        payload = self.get(url=url, params=params)

        return payload.items()
        # yield exchange, data
