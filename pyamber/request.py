import os
from enum import Enum

import requests
import pandas as pd

pd.Timestamp.value_in_milliseconds = property(lambda self: int(self.value * 1e-6))


class TimeFormat(Enum):
    MILLISECONDS = "milliseconds"
    MS = "ms"
    ISO = "iso"
    ISO8611 = "iso8611"


class TimeInterval(Enum):
    DAYS = "days"
    HOURS = "hours"
    MINUTES = "minutes"


class AmberRequest(object):
    def __init__(self, key):
        self.__key = key

    @property
    def headers(self):
        return {"accept": "application/json", "x-api-key": self.__key}

    def get(self, url, params=None):
        response = requests.get(url=url, params=params, headers=self.headers)
        # check that the response is ok
        response.raise_for_status()
        return response

    @property
    def health(self):
        return self.get(url="https://web3api.io/health")

    def price_history(self, pair, timeInterval=None, startDate=None, endDate=None):
        # todo: pagination

        def __dict2series(ts):
            return pd.Series({pd.Timestamp(1e6 * int(x["timestamp"])): x["price"] for x in ts})

        def __payload2frame(payload):
            return pd.DataFrame({name: __dict2series(ts) for name, ts in payload.items()})

        startDate = (startDate or pd.Timestamp("today")).value_in_milliseconds
        endDate = (endDate or pd.Timestamp("today")).value_in_milliseconds

        # gap = endDate - startDate
        timeInterval = timeInterval or TimeInterval.HOURS
        timeFormat = TimeFormat.MILLISECONDS

        url = "https://web3api.io/api/v2/market/prices/{pair}/historical".format(pair=pair)
        params = {"timeInterval": timeInterval.value, "startDate": startDate, "endDate": endDate,
                  "timeFormat": timeFormat.value}

        response = self.get(url=url, params=params)

        request = response.json()["payload"]
        return __payload2frame(request)

    def ohlcv_history(self, pair, exchange, startDate=None, endDate=None, timeInterval=None):
        startDate = (startDate or pd.Timestamp("today")).value_in_milliseconds
        endDate = (endDate or pd.Timestamp("today")).value_in_milliseconds

        timeInterval = timeInterval or TimeInterval.HOURS
        timeFormat = TimeFormat.MILLISECONDS

        url = "https://web3api.io/api/v2/market/ohlcv/{pair}/historical".format(pair=pair)
        params = {"timeInterval": timeInterval.value, "startDate": startDate, "endDate": endDate,
                  "timeFormat": timeFormat.value, "exchange": exchange}

        response = self.get(url=url, params=params)

        x = response.json()["payload"]
        columns = x["metadata"]["columns"]

        #columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']

        for key, data in x["data"].items():
            xx = pd.DataFrame(columns=columns, data=data)
            xx["timestamp"] = xx["timestamp"].apply(lambda x: pd.Timestamp(int(x) * 1e6))

            yield key, xx.set_index(keys="timestamp")

    def bid_ask_history(self, pair, exchange, startDate=None, endDate=None): #, timeInterval=None):
        startDate = (startDate or pd.Timestamp("today")).value_in_milliseconds
        endDate = (endDate or pd.Timestamp("today")).value_in_milliseconds

        #timeInterval = timeInterval or TimeInterval.HOURS

        url = "https://web3api.io/api/v2/market/tickers/{pair}/historical".format(pair=pair)

        params = {"startDate": startDate, "endDate": endDate, "exchange": exchange} #, "timeInterval": timeInterval.value}

        response = self.get(url=url, params=params)

        x = response.json()["payload"]
        columns = x["metadata"]["columns"]

        for key, data in x["data"].items():
            xx = pd.DataFrame(columns=columns, data=data)
            xx["timestamp"] = xx["timestamp"].apply(lambda x: pd.Timestamp(int(x) * 1e6))
            xx["spread"] = xx["ask"] - xx["bid"]
            xx["rel. spread"] = xx["spread"]/xx["mid"]
            xx["rel. spread in BPs"] = 1e4*xx["rel. spread"]

            yield key, xx.set_index(keys="timestamp")
