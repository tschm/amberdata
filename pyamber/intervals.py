import pandas as pd
import numpy as np


class Intervals(object):
    def __init__(self, startDate=None, endDate=None, max=86400 * 1000 * 10):
        pd.Timestamp.value_in_milliseconds = property(lambda self: int(self.value * 1e-6))
        self.__startDate = startDate or pd.Timestamp("today")
        self.__endDate = endDate or pd.Timestamp("today")
        self.__max = max

    @property
    def gap(self):
        return self.end - self.start

    @property
    def start(self):
        return self.__startDate.value_in_milliseconds

    @property
    def end(self):
        return self.__endDate.value_in_milliseconds

    @property
    def start_date(self):
        return self.__startDate

    @property
    def end_date(self):
        return self.__endDate

    @property
    def intervals(self):
        for t in np.arange(start=self.start, step=self.__max, stop=self.end):
            yield pd.Timestamp(1e6*int(t)), pd.Timestamp(1e6*min(t + self.__max, self.end))

