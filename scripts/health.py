from pyamber.request import AmberRequest, TimeInterval

if __name__ == '__main__':
    pair = "eth_usd"
    request = AmberRequest(key="123")
    f = request.price_history(pair="eth_usd", timeInterval=TimeInterval.HOURS)
    print(f)
