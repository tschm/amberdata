import os
import pandas as pd
import json


def resources(name):
    return os.path.join(os.path.dirname(__file__), "resources", name)


def read_json(name):
    with open(resources(name)) as f:
        return json.load(f)


def read_pd(name, **kwargs):
    return pd.read_csv(resources(name), **kwargs)
