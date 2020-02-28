from enum import Enum

import pandas as pd
import requests

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
        return response.json()["payload"]

    @property
    def health(self):
        return requests.get(url="https://web3api.io/health")

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

        payload = self.get(url=url, params=params)
        return __payload2frame(payload)


    @staticmethod
    def __frames(x):
        data = x.get("data", {})

        for key, data in data.items():
            frame = pd.DataFrame(columns=x["metadata"]["columns"], data=data)
            frame["timestamp"] = frame["timestamp"].apply(lambda t: pd.Timestamp(int(t) * 1e6))
            yield key, frame.set_index(keys="timestamp")

    def ohlcv_history(self, pair, exchange, startDate=None, endDate=None, timeInterval=None):
        startDate = (startDate or pd.Timestamp("today")).value_in_milliseconds
        endDate = (endDate or pd.Timestamp("today")).value_in_milliseconds

        timeInterval = timeInterval or TimeInterval.HOURS
        timeFormat = TimeFormat.MILLISECONDS

        url = "https://web3api.io/api/v2/market/ohlcv/{pair}/historical".format(pair=pair)
        params = {"timeInterval": timeInterval.value, "startDate": startDate, "endDate": endDate,
                  "timeFormat": timeFormat.value, "exchange": exchange}

        payload = self.get(url=url, params=params)

        for exchange, data in self.__frames(payload):
            yield exchange, data

    def ohlcv_latest(self, pair, exchange):
        url = "https://web3api.io/api/v2/market/ohlcv/{pair}/latest".format(pair=pair)
        params = {"exchange": exchange}

        payload = self.get(url=url, params=params)

        for exchange, data in payload.items():
            if data["timestamp"]:
                #x = pd.Series(data)
                data["timestamp"] = pd.Timestamp(int(data["timestamp"])*1e6)
                yield exchange, pd.Series(data)

        #print(payload)

        #assert False



    def bid_ask_history(self, pair, exchange, startDate=None, endDate=None):
        startDate = (startDate or pd.Timestamp("today")).value_in_milliseconds
        endDate = (endDate or pd.Timestamp("today")).value_in_milliseconds

        url = "https://web3api.io/api/v2/market/tickers/{pair}/historical".format(pair=pair)

        params = {"startDate": startDate, "endDate": endDate, "exchange": exchange}

        payload = self.get(url=url, params=params)

        for exchange, data in self.__frames(payload):
            data["spread"] = data["ask"] - data["bid"]
            data["rel. spread"] = data["spread"] / data["mid"]
            data["rel. spread in BPs"] = 1e4 * data["rel. spread"]

            yield exchange, data

    def exchanges(self, pair=None):

        url = "https://web3api.io/api/v2/market/exchanges"
        pair = pair or []

        params = {"pair": pair}
        payload = self.get(url=url, params=params)

        return payload.items()
            #yield exchange, data

