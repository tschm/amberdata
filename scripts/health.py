from pyamber.request import AmberRequest

if __name__ == '__main__':
    a = AmberRequest()
    response = a.get(url="https://web3api.io/health")
    print(response)

    # url = "https://web3api.io/api/v2/market/prices/eth_usd/latest"
    response = a.get(url="https://web3api.io/api/v2/market/prices/eth_usd/historical")
    print(response.text)

