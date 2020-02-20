from pyamber.request import AmberRequest
from pyamber.util import  payload2frame

import pandas as pd

if __name__ == '__main__':
    def f(t):
        return int(t.value*1e-6)

    def f_inv(i):
        return pd.Timestamp(1e6*int(i))

    # start at the beginning of Feb 2020
    startDate = f(pd.Timestamp("2020-02-01"))
    assert startDate == 1580515200000

    # add the maximal gap to the startDate
    maxGap = 2678400000 - 1000
    endDate = startDate + maxGap

    print(endDate)
    print(f_inv(endDate))

    request = AmberRequest()

    # url = "https://web3api.io/api/v2/market/prices/eth_usd/latest"
    response = request.get(url="https://web3api.io/api/v2/market/prices/eth_usd/historical",
                           params={"timeInterval":"hours", "startDate": str(startDate), "endDate": str(endDate)})



    print(response.text)

    request = response.json()["payload"]
    print(payload2frame(request))









