import os
import requests


class AmberRequest(object):
    def __init__(self, key=None):
        self.__key = key or os.environ["AMBER_KEY"]

    @property
    def headers(self):
        return {"accept": "application/json", "x-api-key": self.__key}

    def get(self, url, params=None):
        return requests.get(url=url, params=params, headers=self.headers)

    @property
    def health(self):
        return self.get(url="https://web3api.io/health")
