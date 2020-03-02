from unittest.mock import patch

import pandas as pd
import pytest
from requests import HTTPError

import requests_mock

from pyamber.enum import TimeInterval
from pyamber.request import AmberRequest
import pandas.util.testing as pdt


def test_health():
    assert AmberRequest("a").health


def test_history():
    # this should result in a problem as the test is not aware of a correct key for amberdata
    with pytest.raises(HTTPError):
        AmberRequest(key="a").prices.history(pair="eth_usd")


def test_history_mock_2():
    with requests_mock.Mocker() as m:
        m.get('https://web3api.io/api/v2/market/prices/eth_usd/historical',
                json={"status": 200, "payload": {"eth_usd":
                                                     [{"timestamp": 1578873600000, "price": 146.7310000000000000},
                                                      {"timestamp": 1578787200000, "price": 142.3810000000000000}]
                                                 }})

        f = AmberRequest(key="a").prices.history(pair="eth_usd")
        pdt.assert_frame_equal(f, pd.DataFrame(columns=["eth_usd"], index=[pd.Timestamp("2020-01-13"), pd.Timestamp("2020-01-12")], data=[[146.7310000000000000], [142.3810000000000000]]))


@patch.object(AmberRequest, 'get')
def test_history_ohlcv(get_ohlcv):
    for exchange, data in AmberRequest(key="a").ohlcv.history(pair="eth_usd", start_date=pd.Timestamp("2020-01-15"), end_date=pd.Timestamp("2020-01-17"), time_interval=TimeInterval.HOURS, exchange="bitfinex"):
        pass

    get_ohlcv.assert_called_once_with(params={'timeInterval': 'hours', 'startDate': 1579046400000, 'endDate': 1579219200000, 'timeFormat': 'milliseconds', 'exchange': "bitfinex"},
                                      url='https://web3api.io/api/v2/market/ohlcv/eth_usd/historical')


@patch.object(AmberRequest, 'get')
def test_history_bid_ask(get_bid_ask):
    for exchange, data in AmberRequest(key="a").bid_ask.history(pair="eth_usd", start_date=pd.Timestamp("2020-01-12"), end_date=pd.Timestamp("2020-01-13"), exchange="bitfinex"):
        pass

    get_bid_ask.assert_called_once_with(params={'endDate': 1578873600000, 'startDate': 1578787200000, 'exchange': "bitfinex"},
                                        url='https://web3api.io/api/v2/market/tickers/eth_usd/historical')


def test_history_bid_ask_2():
    with requests_mock.Mocker() as m:
        m.get("https://web3api.io/api/v2/market/tickers/eth_usd/historical",
                          json={"status": 200,
                                "payload": {"metadata":
                                                {"columns": ["timestamp", "bid", "ask", "mid", "last"]},
                                            "data":
                                                {"bitfinex": [[1578873600000, 100, 102, 101, 101.5],
                                                              [1578787200000, 101, 102, 101.5, 101.2]]}
                                            }})

        d = {exchange: data for exchange, data in AmberRequest(key="a").bid_ask.history(pair="eth_usd", start_date=pd.Timestamp("2020-01-12"), end_date=pd.Timestamp("2020-01-13"), exchange="bitfinex")}
        assert set(d.keys()) == {"bitfinex"}
        assert list(d["bitfinex"].index) == [pd.Timestamp("2020-01-13"), pd.Timestamp("2020-01-12")]
        assert d["bitfinex"]["rel. spread"][pd.Timestamp("2020-01-13")] == pytest.approx(2.0/101.0, 1e-10)


@patch.object(AmberRequest, 'get')
def test_history_mock(get_history):

    AmberRequest(key="a").prices.history(pair="eth_usd", start_date=pd.Timestamp("2020-01-12"), end_date=pd.Timestamp("2020-01-13"), time_interval=TimeInterval.HOURS)
    get_history.assert_called_once_with(params={'timeInterval': 'hours', 'endDate': 1578873600000, 'startDate': 1578787200000, 'timeFormat': 'milliseconds'},
                                     url='https://web3api.io/api/v2/market/prices/eth_usd/historical')
