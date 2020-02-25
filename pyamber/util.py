import pandas as pd


def dict2series(ts):
    return pd.Series({pd.Timestamp(1e6*int(x["timestamp"])): x["price"] for x in ts})


def payload2frame(payload):
    #todo:
    return pd.DataFrame({name: dict2series(ts) for name, ts in payload.items()})

