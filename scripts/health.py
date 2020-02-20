import pandas as pd

from pyamber.request import AmberRequest
from pyamber.util import dict2series, payload2frame

if __name__ == '__main__':
    payload = AmberRequest()

    # url = "https://web3api.io/api/v2/market/prices/eth_usd/latest"
    response = payload.get(url="https://web3api.io/api/v2/market/prices/eth_usd/historical")
    print(response.text)

    payload = response.json()["payload"]
    print(payload2frame(payload))








