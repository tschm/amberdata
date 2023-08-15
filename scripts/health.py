from __future__ import annotations

from pyamber.enum import TimeInterval
from pyamber.request import AmberRequest

if __name__ == "__main__":
    request = AmberRequest(key="...")
    f = request.prices.history(pair="eth_usd", timeInterval=TimeInterval.HOURS)
    print(f)
