import pandas as pd

from pyamber.intervals import intervals


def test_intervals():
    startDate = pd.Timestamp("2020-01-01")
    endDate = pd.Timestamp("2020-12-31")

    starts = [start for (start, _) in intervals(startDate=startDate, endDate=endDate, freq=pd.Timedelta(days=20))]
    ends = [end for (_, end) in intervals(startDate=startDate, endDate=endDate, freq=pd.Timedelta(days=20))]

    assert starts[0] == startDate
    assert ends[0] == starts[1]
    assert len(starts) == 19
    assert len(starts) == len(ends)



