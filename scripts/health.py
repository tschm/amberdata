from pyamber.request import AmberRequest, TimeInterval


if __name__ == '__main__':
    pair = "eth_usd"
    request = AmberRequest(key="...")
    f = request.price_history(pair=pair, timeInterval=TimeInterval.HOURS)
    print(f)



