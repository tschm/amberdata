# pyamber
[![Build Status](https://travis-ci.org/tschm/amberdata.svg?branch=master)](https://travis-ci.org/tschm/amberdata)


Some utility code for interacting with amberdata. For more information on amberdata please check out
https://amberdata.io/.

## Installing pyamber
Install with pip
```
pip install pyamber
```

## AmberRequest
AmberRequest is a class hiding the management of your key, the pagination of requests and conversion of your results to standard pandas containers.

```
from pyamber.request import AmberRequest, TimeInterval

if __name__ == '__main__':
    request = AmberRequest(key="...")
    f = request.prices.history(pair="eth_usd", time_interval=TimeInterval.HOURS)
    print(f)

```

## Settings.cfg
We recommend to define a configuration file `(*.cfg)` containing
```
AMBERDATA = {'x-api-key': 'ENTER YOUR KEY HERE'}
```

## Flask-AmberData
A Flask extension that provides integration with AmberData. In particular this flask extension provides
management of the your AmberRequests. You can use configuration files such as settings.cfg to follow standard flask practices.
The configuration is easy, just fetch the extension:
```
import pandas as pd
from flask import Flask

from pyamber.flask_amberdata import amberdata
from pyamber.request import TimeInterval

if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_pyfile('/amberdata/config/settings.cfg')
    amberdata.init_app(app)

    with app.app_context():
        assert amberdata.request.health
        x = amberdata.request.prices.history("eth_usd", time_interval=TimeInterval.DAYS, start_date=pd.Timestamp("2020-01-12"), end_date=pd.Timestamp("2020-01-16"))
        print(x)
```




