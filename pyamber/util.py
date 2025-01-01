from __future__ import annotations

import pandas as pd


def frames(x):
    data = x.get("data", {})

    for key, data in data.items():
        frame = pd.DataFrame(columns=x["metadata"]["columns"], data=data)
        frame["timestamp"] = frame["timestamp"].apply(lambda t: pd.Timestamp(int(t) * 1e6))
        yield key, frame.set_index(keys="timestamp")
