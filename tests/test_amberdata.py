from __future__ import annotations

import json

import pandas as pd
import pandas.testing as pt
import pytest
import requests_mock
from requests import HTTPError

from pyamber.enum import TimeInterval
from pyamber.request import AmberRequest


def read_json(name):
    with open(name) as f:
        return json.load(f)


def test_health():
    assert AmberRequest("a").health


def test_history():
    # this should result in a problem as the test is not aware of a correct key for amberdata
    with pytest.raises(HTTPError):
        AmberRequest(key="a").prices.history(pair="eth_usd")


def test_prices_latest(resource_dir):
    with requests_mock.Mocker() as m:
        m.get(
            "https://web3api.io/api/v2/market/prices/eth_usd/latest",
            json=read_json(resource_dir / "prices_latest.json"),
        )
        for pair, series in AmberRequest(key="a").prices.latest(pair="eth_usd"):
            assert pair == "eth_usd"

            x = pd.read_csv(
                resource_dir / "prices_latest.csv",
                index_col=0,
                parse_dates=True,
                header=None,
            )[1]
            print(x)

            pt.assert_series_equal(
                series,
                x,
                check_names=False,
            )


def test_ohlcv_latest(resource_dir):
    with requests_mock.Mocker() as m:
        m.get(
            "https://web3api.io/api/v2/market/ohlcv/eth_usd/latest",
            json=read_json(resource_dir / "ohlcv_latest.json"),
        )
        for exchange, series in AmberRequest(key="a").ohlcv.latest(pair="eth_usd", exchange="bitfinex"):
            assert exchange == "bitfinex"

            x = pd.read_csv(resource_dir / "ohlcv_latest.csv", index_col=0, header=None).squeeze()
            x["timestamp"] = pd.Timestamp(x["timestamp"])

            for key in {"open", "high", "low", "close", "volume"}:
                x[key] = float(x[key])

            pt.assert_series_equal(series, x, check_names=False)


def test_bid_ask_latest(resource_dir):
    with requests_mock.Mocker() as m:
        m.get(
            "https://web3api.io/api/v2/market/tickers/eth_usd/latest",
            json=read_json(resource_dir / "bidask_latest.json"),
        )
        for exchange, series in AmberRequest(key="a").bid_ask.latest(pair="eth_usd", exchange="bitfinex"):
            assert exchange == "bitfinex"

            x = pd.read_csv(resource_dir / "bidask_latest.csv", index_col=0, header=None).squeeze()
            x["timestamp"] = pd.Timestamp(x["timestamp"])

            for key in {"bid", "ask", "mid", "last"}:
                x[key] = float(x[key])

            pt.assert_series_equal(series, x, check_names=False)


def test_bidask_history(resource_dir):
    with requests_mock.Mocker() as m:
        m.get(
            "https://web3api.io/api/v2/market/tickers/eth_usd/historical",
            json=read_json(resource_dir / "bidask_history.json"),
        )
        for exchange, data in AmberRequest(key="a").bid_ask.history(
            pair="eth_usd",
            exchange="bitfinex",
            start_date=pd.Timestamp("2020-02-12 23:50:00"),
            end_date=pd.Timestamp("2020-02-13"),
        ):
            assert exchange == "bitfinex"
            pt.assert_frame_equal(
                data,
                pd.read_csv(resource_dir / "bidask_history.csv", index_col=0, parse_dates=True),
            )


def test_ohlcv_history(resource_dir):
    with requests_mock.Mocker() as m:
        m.get(
            "https://web3api.io/api/v2/market/ohlcv/eth_usd/historical?timeInterval=days&startDate=1577836800000",
            json=read_json(resource_dir / "ohlcv_history1.json"),
        )
        m.get(
            "https://web3api.io/api/v2/market/ohlcv/eth_usd/historical?timeInterval=days&startDate=1579564800000",
            json=read_json(resource_dir / "ohlcv_history2.json"),
        )
        m.get(
            "https://web3api.io/api/v2/market/ohlcv/eth_usd/historical?timeInterval=days&startDate=1581292800000",
            json=read_json(resource_dir / "ohlcv_history3.json"),
        )

        for exchange, data in AmberRequest(key="a").ohlcv.history(
            pair="eth_usd",
            exchange="bitfinex",
            start_date=pd.Timestamp("2020-01-01"),
            end_date=pd.Timestamp("2020-02-20"),
            time_interval=TimeInterval.DAYS,
        ):
            assert exchange == "bitfinex"
            pt.assert_frame_equal(
                data,
                pd.read_csv(resource_dir / "ohlcv_history.csv", index_col=0, parse_dates=True),
            )


def test_prices_history(resource_dir):
    with requests_mock.Mocker() as m:
        m.get(
            "https://web3api.io/api/v2/market/prices/eth_usd/historical",
            json=read_json(resource_dir / "prices_history.json"),
        )
        x = AmberRequest(key="a").prices.history(
            pair="eth_usd",
            start_date=pd.Timestamp("2020-02-12"),
            end_date=pd.Timestamp("2020-02-13"),
            time_interval=TimeInterval.DAYS,
        )
        pt.assert_frame_equal(
            x,
            pd.read_csv(resource_dir / "prices_history.csv", index_col=0, parse_dates=True),
        )
