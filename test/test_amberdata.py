import pandas as pd
import pytest
from requests import HTTPError

import requests_mock

from pyamber.enum import TimeInterval
from pyamber.request import AmberRequest
import pandas.util.testing as pdt

from test.settings import read_json, read_pd


def test_health():
    assert AmberRequest("a").health


def test_history():
    # this should result in a problem as the test is not aware of a correct key for amberdata
    with pytest.raises(HTTPError):
        AmberRequest(key="a").prices.history(pair="eth_usd")



# @patch.object(AmberRequest, 'get')
# def test_history_ohlcv(get_ohlcv):
#     for exchange, data in AmberRequest(key="a").ohlcv.history(pair="eth_usd", start_date=pd.Timestamp("2020-01-15"), end_date=pd.Timestamp("2020-01-17"), time_interval=TimeInterval.HOURS, exchange="bitfinex"):
#         pass
#
#     get_ohlcv.assert_called_once_with(params={'timeInterval': 'hours', 'startDate': 1579046400000, 'endDate': 1579219200000, 'timeFormat': 'milliseconds', 'exchange': "bitfinex"},
#                                       url='https://web3api.io/api/v2/market/ohlcv/eth_usd/historical')
#
#
# @patch.object(AmberRequest, 'get')
# def test_history_bid_ask(get_bid_ask):
#     for exchange, data in AmberRequest(key="a").bid_ask.history(pair="eth_usd", start_date=pd.Timestamp("2020-01-12"), end_date=pd.Timestamp("2020-01-13"), exchange="bitfinex"):
#         pass
#
#     get_bid_ask.assert_called_once_with(params={'endDate': 1578873600000, 'startDate': 1578787200000, 'exchange': "bitfinex"},
#                                         url='https://web3api.io/api/v2/market/tickers/eth_usd/historical')
#
#
# def test_history_bid_ask_2():
#     with requests_mock.Mocker() as m:
#         m.get("https://web3api.io/api/v2/market/tickers/eth_usd/historical",
#                           json={"status": 200,
#                                 "payload": {"metadata":
#                                                 {"columns": ["timestamp", "bid", "ask", "mid", "last"]},
#                                             "data":
#                                                 {"bitfinex": [[1578873600000, 100, 102, 101, 101.5],
#                                                               [1578787200000, 101, 102, 101.5, 101.2]]}
#                                             }})
#
#         d = {exchange: data for exchange, data in AmberRequest(key="a").bid_ask.history(pair="eth_usd", start_date=pd.Timestamp("2020-01-12"), end_date=pd.Timestamp("2020-01-13"), exchange="bitfinex")}
#         assert set(d.keys()) == {"bitfinex"}
#         assert list(d["bitfinex"].index) == [pd.Timestamp("2020-01-13"), pd.Timestamp("2020-01-12")]
#         assert d["bitfinex"]["rel. spread"][pd.Timestamp("2020-01-13")] == pytest.approx(2.0/101.0, 1e-10)


def test_prices_latest():
    with requests_mock.Mocker() as m:
        m.get("https://web3api.io/api/v2/market/prices/eth_usd/latest", json=read_json("prices_latest.json"))
        for pair, series in AmberRequest(key="a").prices.latest(pair="eth_usd"):
            assert pair == "eth_usd"
            pdt.assert_series_equal(series, read_pd("prices_latest.csv", squeeze=True, index_col=0, parse_dates=True, header=None), check_names=False)


def test_ohlcv_latest():
    with requests_mock.Mocker() as m:
        m.get("https://web3api.io/api/v2/market/ohlcv/eth_usd/latest", json=read_json("ohlcv_latest.json"))
        for exchange, series in AmberRequest(key="a").ohlcv.latest(pair="eth_usd", exchange="bitfinex"):
            assert exchange == "bitfinex"

            x = read_pd("ohlcv_latest.csv", squeeze=True, index_col=0, header=None)
            x["timestamp"] = pd.Timestamp(x["timestamp"])

            for key in {"open", "high", "low", "close", "volume"}:
                x[key] = float(x[key])

            pdt.assert_series_equal(series, x, check_names=False)


def test_bid_ask_latest():
    with requests_mock.Mocker() as m:
        m.get("https://web3api.io/api/v2/market/tickers/eth_usd/latest", json=read_json("bidask_latest.json"))
        for exchange, series in AmberRequest(key="a").bid_ask.latest(pair="eth_usd", exchange="bitfinex"):
            assert exchange == "bitfinex"

            x = read_pd("bidask_latest.csv", squeeze=True, index_col=0, header=None)
            x["timestamp"] = pd.Timestamp(x["timestamp"])

            for key in {"bid", "ask", "mid", "last"}:
                x[key] = float(x[key])

            pdt.assert_series_equal(series, x, check_names=False)



def test_prices_history():
    with requests_mock.Mocker() as m:
        m.get("https://web3api.io/api/v2/market/prices/eth_usd/historical", json=read_json("prices_history.json"))
        x = AmberRequest(key="a").prices.history(pair="eth_usd", start_date=pd.Timestamp("2020-02-12"), end_date=pd.Timestamp("2020-02-13"), time_interval=TimeInterval.DAYS)
        pdt.assert_frame_equal(x, read_pd("prices_history.csv", index_col=0, parse_dates=True))
