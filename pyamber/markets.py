from __future__ import annotations

import pandas as pd

from pyamber.enum import TimeFormat, TimeInterval
from pyamber.intervals import intervals
from pyamber.util import frames

pd.Timestamp.value_in_milliseconds = property(lambda self: int(self.value * 1e-6))


class OhlcvRequest:
    def __init__(self, request):
        self.__request = request

    def history(
        self,
        pair,
        exchange,
        start_date=None,
        end_date=None,
        time_interval=None,
        logger=None,
    ):
        start_date = start_date or pd.Timestamp("today")
        end_date = end_date or pd.Timestamp("today")

        assert isinstance(start_date, pd.Timestamp)
        assert isinstance(end_date, pd.Timestamp)

        d = {e: pd.DataFrame() for e in exchange.split(",")}
        time_interval = time_interval or TimeInterval.HOURS

        url = "https://web3api.io/api/v2/market/ohlcv/{pair}/historical".format(pair=pair)

        # loop over the intervals
        for start, end in intervals(start_date=start_date, end_date=end_date):
            # loop over the exchanges
            params = {
                "timeInterval": time_interval.value,
                "startDate": start.value_in_milliseconds,
                "endDate": end.value_in_milliseconds,
                "timeFormat": TimeFormat.MILLISECONDS.value,
                "exchange": exchange,
            }

            for e, data in frames(self.__request.get(url=url, params=params, logger=logger)):
                d[e] = pd.concat((d[e], data), axis=0)

        # {exchange : data...}
        for e, data in d.items():
            if not data.empty:
                yield e, data.sort_index(ascending=False)

    def latest(self, pair, exchange, logger=None):
        url = "https://web3api.io/api/v2/market/ohlcv/{pair}/latest".format(pair=pair)
        params = {"exchange": exchange}

        payload = self.__request.get(url=url, params=params, logger=logger)

        for exchange, data in payload.items():
            if data["timestamp"]:
                data["timestamp"] = pd.Timestamp(int(data["timestamp"]) * 1e6)
                yield exchange, pd.Series(data)


class PriceRequest:
    def __init__(self, request):
        self.__request = request

    def latest(self, pair, logger=None):
        def __dict2series(x):
            return pd.Series({pd.Timestamp(1e6 * int(x["timestamp"])): x["price"]})

        url = "https://web3api.io/api/v2/market/prices/{pair}/latest".format(pair=pair)
        params = {"timeFormat": TimeFormat.MILLISECONDS.value}
        payload = self.__request.get(url=url, params=params, logger=logger)

        for exchange, data in payload.items():
            if data["timestamp"]:
                yield exchange, __dict2series(data).apply(float)

    def history(self, pair, start_date=None, end_date=None, time_interval=None, logger=None):
        def __dict2series(ts):
            return pd.Series({pd.Timestamp(1e6 * int(x["timestamp"])): float(x["price"]) for x in ts})

        def __payload2frame(payload):
            return pd.DataFrame({name: __dict2series(ts) for name, ts in payload.items()})

        start_date = start_date or pd.Timestamp("today")
        end_date = end_date or pd.Timestamp("today")

        assert isinstance(start_date, pd.Timestamp)
        assert isinstance(end_date, pd.Timestamp)

        time_interval = time_interval or TimeInterval.HOURS

        url = "https://web3api.io/api/v2/market/prices/{pair}/historical".format(pair=pair)

        frame = pd.DataFrame(columns=[pair])

        for start, end in intervals(start_date=start_date, end_date=end_date, freq=pd.Timedelta(days=1)):
            params = {
                "timeInterval": time_interval.value,
                "startDate": start.value_in_milliseconds,
                "endDate": end.value_in_milliseconds,
                "timeFormat": TimeFormat.MILLISECONDS.value,
            }
            payload = self.__request.get(url=url, params=params, logger=logger)
            frame = pd.concat((frame, __payload2frame(payload)), axis=0)

        return frame.sort_index(ascending=False)


class BidAskRequest:
    def __init__(self, request):
        self.__request = request

    def history(self, pair, exchange, start_date=None, end_date=None, logger=None):
        start_date = start_date or pd.Timestamp("today")
        end_date = end_date or pd.Timestamp("today")

        assert isinstance(start_date, pd.Timestamp)
        assert isinstance(end_date, pd.Timestamp)

        url = "https://web3api.io/api/v2/market/tickers/{pair}/historical".format(pair=pair)

        d = {e: pd.DataFrame() for e in exchange.split(",")}

        # loop over the intervals
        for start, end in intervals(start_date=start_date, end_date=end_date):
            params = {
                "startDate": start.value_in_milliseconds,
                "endDate": end.value_in_milliseconds,
                "exchange": exchange,
            }
            payload = self.__request.get(url=url, params=params, logger=logger)

            for e, data in frames(payload):
                data["spread"] = data["ask"] - data["bid"]
                data["rel. spread"] = data["spread"] / data["mid"]
                data["rel. spread in BPs"] = 1e4 * data["rel. spread"]

                d[e] = pd.concat((d[e], data), axis=0)

        for e, data in d.items():
            if not data.empty:
                yield e, data.sort_index(ascending=False)

    def latest(self, pair, exchange, logger=None):
        url = "https://web3api.io/api/v2/market/tickers/{pair}/latest".format(pair=pair)
        params = {"exchange": exchange}

        payload = self.__request.get(url=url, params=params, logger=logger)

        for exchange, data in payload.items():
            if data["timestamp"]:
                data["timestamp"] = pd.Timestamp(int(data["timestamp"]) * 1e6)
                yield exchange, pd.Series(data)
