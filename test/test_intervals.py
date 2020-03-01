import pandas as pd

from pyamber.intervals import Intervals

pd.Timestamp.value_in_milliseconds = property(lambda self: int(self.value * 1e-6))


def test_intervals():
    startDate = pd.Timestamp("2020-01-01")
    endDate = pd.Timestamp("2020-12-31")

    k = Intervals(startDate=startDate, endDate=endDate, max=86400*1000*30)

    assert k.start_date == startDate
    assert k.end_date == endDate

    assert k.start == startDate.value_in_milliseconds
    assert k.end == endDate.value_in_milliseconds

    assert k.gap == endDate.value_in_milliseconds - startDate.value_in_milliseconds

    starts = [start for (start, end) in k.intervals]
    ends = [end for (start, end) in k.intervals]

    assert starts[0] == startDate
    assert ends[0] == starts[1]
    assert len(starts) == 13
    assert len(starts) == len(ends)



