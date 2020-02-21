from pyamber.request import AmberRequest, TimeInterval, TimeFormat


if __name__ == '__main__':
    pair = "eth_usd"
    request = AmberRequest()
    f = request.price_history(pair=pair)
    print(f)



