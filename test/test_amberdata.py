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


def test_bidask_history():
    with requests_mock.Mocker() as m:
        m.get("https://web3api.io/api/v2/market/tickers/eth_usd/historical", json=read_json("bidask_history.json"))
        for exchange, data in AmberRequest(key="a").bid_ask.history(pair="eth_usd", exchange="bitfinex", start_date=pd.Timestamp("2020-02-12 23:50:00"), end_date=pd.Timestamp("2020-02-13")):
            assert exchange == "bitfinex"
            pdt.assert_frame_equal(data, read_pd("bidask_history.csv", index_col=0, parse_dates=True))


def test_ohlcv_history():
    with requests_mock.Mocker() as m:
        m.get("https://web3api.io/api/v2/market/ohlcv/eth_usd/historical?timeInterval=days&startDate=1577836800000", json=read_json("ohlcv_history1.json"))
        m.get("https://web3api.io/api/v2/market/ohlcv/eth_usd/historical?timeInterval=days&startDate=1579564800000", json=read_json("ohlcv_history2.json"))
        m.get("https://web3api.io/api/v2/market/ohlcv/eth_usd/historical?timeInterval=days&startDate=1581292800000", json=read_json("ohlcv_history3.json"))

        for exchange, data in AmberRequest(key="a").ohlcv.history(pair="eth_usd", exchange="bitfinex", start_date=pd.Timestamp("2020-01-01"), end_date=pd.Timestamp("2020-02-20"), time_interval=TimeInterval.DAYS):
            assert exchange == "bitfinex"
            pdt.assert_frame_equal(data, read_pd("ohlcv_history.csv", index_col=0, parse_dates=True))


def test_prices_history():
    with requests_mock.Mocker() as m:
        m.get("https://web3api.io/api/v2/market/prices/eth_usd/historical", json=read_json("prices_history.json"))
        x = AmberRequest(key="a").prices.history(pair="eth_usd", start_date=pd.Timestamp("2020-02-12"), end_date=pd.Timestamp("2020-02-13"), time_interval=TimeInterval.DAYS)
        pdt.assert_frame_equal(x, read_pd("prices_history.csv", index_col=0, parse_dates=True))


def test_exchanges():
    with requests_mock.Mocker() as m:
        m.get("https://web3api.io/api/v2/market/exchanges?pair=eth_usd", json=read_json("exchanges.json"))
        xxx = [exchange for exchange, data in AmberRequest(key="a").features.exchanges(pair="eth_usd")]
        assert xxx == ["bitfinex", "bitstamp", "gdax", "gemini", "kraken"]
