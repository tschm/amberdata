class Features_Request(object):
    def __init__(self, request):
        self.__request = request

    def exchanges(self, pair=None, logger=None):
        url = "https://web3api.io/api/v2/market/exchanges"
        pair = pair or []

        params = {"pair": pair}
        payload = self.__request.get(url=url, params=params, logger=logger)

        for exchange, data in payload.items():
            if data[pair]["ticker"]["startDate"]:
                yield exchange, data
