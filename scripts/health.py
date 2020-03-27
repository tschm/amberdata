from pyamber.request import AmberRequest
from pyamber.enum import TimeInterval


if __name__ == '__main__':
    request = AmberRequest(key="...")
    f = request.price_history(pair="eth_usd", timeInterval=TimeInterval.HOURS)
    print(f)



