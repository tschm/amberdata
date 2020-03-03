import logging

import requests

from pyamber.features import Features_Request
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

    @property
    def features(self):
        return Features_Request(request=self)

    def get(self, url, params=None, logger=None):
        log = logger or logging.getLogger(__name__)

        response = requests.get(url=url, params=params, headers=self.headers)
        # check that the response is ok
        response.raise_for_status()

        log.debug(response.json())

        return response.json()["payload"]

    @property
    def health(self):
        return requests.get(url="https://web3api.io/health")

