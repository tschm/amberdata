from pyamber.request import AmberRequest
from pyamber.util import payload2frame
from enum import Enum

import pandas as pd
pd.Timestamp.value_in_milliseconds = property(lambda self: int(self.value*1e-6))


class TimeFormat(Enum):
    MILLISECONDS = "milliseconds"
    MS = "ms"
    ISO = "iso"
    ISO8611 = "iso8611"


class TimeInterval(Enum):
    DAYS = "days"
    HOURS = "hours"
    MINUTES = "minutes"


def historical(pair, timeInterval=None, startDate=None, endDate=None, timeFormat=None):
    pd.Timestamp.value_in_milliseconds = property(lambda self: int(self.value*1e-6))

    startDate = (startDate or pd.Timestamp("today")).value_in_milliseconds
    endDate = (endDate or pd.Timestamp("today")).value_in_milliseconds

    gap = endDate - startDate
    timeInterval = timeInterval or TimeInterval.HOURS
    timeFormat = timeFormat or TimeFormat.MILLISECONDS

    url="https://web3api.io/api/v2/market/prices/{pair}/historical".format(pair=pair)
    params = {"timeInterval": timeInterval.value, "startDate": startDate, "endDate": endDate, "timeFormat": timeFormat.value}


    request = AmberRequest()
    response = request.get(url=url, params=params)

    request = response.json()["payload"]
    return payload2frame(request)


if __name__ == '__main__':
    def f(t):
        return int(t.value * 1e-6)

    x = pd.Timestamp("today")
    pd.Timestamp.value_in_milliseconds = property(lambda self: int(self.value * 1e-6))
    print(x.value_in_milliseconds)

    pair = "eth_usd"

    #print(historical(pair=pair, startDate=pd.Timestamp("today"), endDate=pd.Timestamp("today") + pd.DateOffset(days=1)))

    #print(response.text)

    #request = response.json()["payload"]
    #print(payload2frame(request))
