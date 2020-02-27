from unittest.mock import patch

import pandas as pd
import pytest
from requests import HTTPError

from pyamber.flask_amberdata import amberdata
from pyamber.request import TimeInterval
from test.settings import amber_request
import pandas.util.testing as pdt


def test_health(amber_request):
    assert amber_request.health


def test_history(amber_request):
    # this should result in a problem as the test is not aware of a correct key for amberdata
    with pytest.raises(HTTPError):
        amber_request.price_history(pair="eth_usd")


def test_history_mock(amber_request):
    with patch("requests.get") as mock:
        amber_request.price_history(pair="eth_usd", startDate=pd.Timestamp("2020-01-15"), endDate=pd.Timestamp("2020-01-17"), timeInterval=TimeInterval.HOURS)
        mock.assert_called_once_with(headers={'accept': 'application/json', 'x-api-key': 'UAK1'},
                                     params={'timeInterval': 'hours', 'startDate': 1579046400000, 'endDate': 1579219200000, 'timeFormat': 'milliseconds'},
                                     url='https://web3api.io/api/v2/market/prices/eth_usd/historical')


def test_history_mock_2(amber_request, requests_mock):
    requests_mock.get('https://web3api.io/api/v2/market/prices/eth_usd/historical',
                      json={"status": 200, "title": "OK", "description": "Successful request", "payload": {"eth_usd": [{"timestamp": 1578873600000, "price": 146.7310000000000000}, {"timestamp": 1578787200000, "price": 142.3810000000000000}]}})
    f = amber_request.price_history(pair="eth_usd")
    pdt.assert_frame_equal(f, pd.DataFrame(columns=["eth_usd"], index=[pd.Timestamp("2020-01-13"), pd.Timestamp("2020-01-12")], data=[[146.7310000000000000], [142.3810000000000000]]))
