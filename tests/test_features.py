import pytest
import requests_mock

from pyamber.request import AmberRequest
from test.settings import read_json


def test_exchanges():
    with pytest.raises(NotImplementedError):
        AmberRequest(key="a").features.exchanges()


def test_trades():
    with requests_mock.Mocker() as m:
        m.get("https://web3api.io/api/v2/market/trades/information?exchange=binance", json=read_json("trades.json"))
        xxx = [(f.pair, f.exchange) for f in AmberRequest(key="a").features.trades(exchange="binance")]
        assert xxx == [("adx_bnb","binance")]


def test_ticker_pairs():
    with requests_mock.Mocker() as m:
        m.get("https://web3api.io/api/v2/market/tickers/information", json=read_json("ticker_pairs.json"))
        xxx = [f.exchange for f in AmberRequest(key="a").features.ticker_pairs()]
        assert xxx == ["bitfinex"]


def test_ohlcv_pairs():
    with requests_mock.Mocker() as m:
        m.get("https://web3api.io/api/v2/market/ohlcv/information", json=read_json("ohlcv_pairs.json"))
        xxx = set([f.exchange for f in AmberRequest(key="a").features.ohlcv_pairs()])
        assert xxx == {"binance"}


def test_price_pairs():
    with requests_mock.Mocker() as m:
        m.get("https://web3api.io/api/v2/market/prices/pairs", json=read_json("price_pairs.json"))
        xxx = set([f for f in AmberRequest(key="a").features.price_pairs()])
        assert xxx == {"18c_btc", "18c_eth", "1st_btc"}

def test_pairs():
    with requests_mock.Mocker() as m:
        m.get("https://web3api.io/api/v2/market/pairs", json=read_json("pairs.json"))
        xxx = [f.exchange for f in AmberRequest(key="a").features.pairs(pair="eth_usd")]
        assert xxx == ["bitfinex"]
