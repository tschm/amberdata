from enum import Enum

import pandas as pd

import requests

from pyamber.intervals import Intervals

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


class _OHLCV_Request(object):
    def __init__(self, request):
        self.__request = request

    def hh(self, pair, exchange, startDate=None, endDate=None, timeInterval=None, max=86400*1000*10):
        startDate = startDate or pd.Timestamp("today")
        endDate = endDate or pd.Timestamp("today")

        periods = Intervals(startDate=startDate, endDate=endDate, max=max)
        d = {e: pd.DataFrame() for e in exchange.split(",")}

        for start, end in periods.intervals:
            for exchange, data in self.history(pair, exchange, startDate=start, endDate=end, timeInterval=timeInterval):
                d[exchange] = pd.concat((d[exchange], data), axis=0)

        return d.items()



    def history(self, pair, exchange, startDate=None, endDate=None, timeInterval=None):
        startDate = (startDate or pd.Timestamp("today")).value_in_milliseconds
        endDate = (endDate or pd.Timestamp("today")).value_in_milliseconds

        timeInterval = timeInterval or TimeInterval.HOURS
        timeFormat = TimeFormat.MILLISECONDS

        url = "https://web3api.io/api/v2/market/ohlcv/{pair}/historical".format(pair=pair)

        params = {"timeInterval": timeInterval.value, "startDate": startDate, "endDate": endDate,
                  "timeFormat": timeFormat.value, "exchange": exchange}

        return AmberRequest._frames(self.__request.get(url=url, params=params))

    def latest(self, pair, exchange):
        url = "https://web3api.io/api/v2/market/ohlcv/{pair}/latest".format(pair=pair)
        params = {"exchange": exchange}

        payload = self.__request.get(url=url, params=params)

        for exchange, data in payload.items():
            if data["timestamp"]:
                data["timestamp"] = pd.Timestamp(int(data["timestamp"]) * 1e6)
                yield exchange, pd.Series(data)


class _Price_Request(object):
    def __init__(self, request):
        self.__request = request

    def latest(self, pair):
        url = "https://web3api.io/api/v2/market/prices/{pair}/latest".format(pair=pair)
        params = {"timeFormat": TimeFormat.MILLISECONDS.value}
        payload = self.__request.get(url=url, params=params)

        for exchange, data in payload.items():
            if data["timestamp"]:
                data["timestamp"] = pd.Timestamp(int(data["timestamp"]) * 1e6)
                yield exchange, pd.Series(data)

    def history(self, pair, startDate=None, endDate=None, timeInterval=None):
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

        payload = self.__request.get(url=url, params=params)
        return __payload2frame(payload)


class _BidAsk_Request(object):
    def __init__(self, request):
        self.__request = request

    def history(self, pair, exchange, startDate=None, endDate=None):
        startDate = (startDate or pd.Timestamp("today")).value_in_milliseconds
        endDate = (endDate or pd.Timestamp("today")).value_in_milliseconds

        url = "https://web3api.io/api/v2/market/tickers/{pair}/historical".format(pair=pair)

        params = {"startDate": startDate, "endDate": endDate, "exchange": exchange}

        payload = self.__request.get(url=url, params=params)

        for exchange, data in AmberRequest._frames(payload):
            data["spread"] = data["ask"] - data["bid"]
            data["rel. spread"] = data["spread"] / data["mid"]
            data["rel. spread in BPs"] = 1e4 * data["rel. spread"]

            yield exchange, data

    def latest(self, pair, exchange):
        url = "https://web3api.io/api/v2/market/tickers/{pair}/latest".format(pair=pair)
        params = {"exchange": exchange}

        payload = self.__request.get(url=url, params=params)

        for exchange, data in payload.items():
            if data["timestamp"]:
                data["timestamp"] = pd.Timestamp(int(data["timestamp"]) * 1e6)
                yield exchange, pd.Series(data)


class AmberRequest(object):
    def __init__(self, key):
        self.__key = key

    @property
    def prices(self):
        return _Price_Request(request=self)

    @property
    def ohlcv(self):
        return _OHLCV_Request(request=self)

    @property
    def bid_ask(self):
        return _BidAsk_Request(request=self)

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

    @staticmethod
    def _frames(x):
        data = x.get("data", {})

        for key, data in data.items():
            frame = pd.DataFrame(columns=x["metadata"]["columns"], data=data)
            frame["timestamp"] = frame["timestamp"].apply(lambda t: pd.Timestamp(int(t) * 1e6))
            yield key, frame.set_index(keys="timestamp")

    def exchanges(self, pair=None):
        url = "https://web3api.io/api/v2/market/exchanges"
        pair = pair or []

        params = {"pair": pair}
        payload = self.get(url=url, params=params)

        return payload.items()
        # yield exchange, data
