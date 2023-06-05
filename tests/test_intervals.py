import pandas as pd

from pyamber.intervals import intervals


def test_intervals():
    startDate = pd.Timestamp("2020-01-01")
    endDate = pd.Timestamp("2020-12-31")

    starts = [start for (start, _) in intervals(start_date=startDate, end_date=endDate, freq=pd.Timedelta(days=20))]
    ends = [end for (_, end) in intervals(start_date=startDate, end_date=endDate, freq=pd.Timedelta(days=20))]

    assert starts[0] == startDate
    assert ends[0] == starts[1]
    assert len(starts) == 19
    assert len(starts) == len(ends)


def test_intervals_single():
    startDate = pd.Timestamp("2020-01-01")
    endDate = pd.Timestamp("2020-01-10")

    starts = [start for (start, _) in intervals(start_date=startDate, end_date=endDate, freq=pd.Timedelta(days=20))]
    ends = [end for (_, end) in intervals(start_date=startDate, end_date=endDate, freq=pd.Timedelta(days=20))]

    assert starts[0] == startDate
    assert ends[0] == endDate
    assert len(starts) == 1
    assert len(starts) == len(ends)


def test_intervals_single_match():
    startDate = pd.Timestamp("2020-01-01")
    endDate = pd.Timestamp("2020-01-21")

    starts = [start for (start, _) in intervals(start_date=startDate, end_date=endDate, freq=pd.Timedelta(days=20))]
    ends = [end for (_, end) in intervals(start_date=startDate, end_date=endDate, freq=pd.Timedelta(days=20))]

    assert starts[0] == startDate
    assert ends[0] == endDate
    assert len(starts) == 1
    assert len(starts) == len(ends)


def test_intervals_match():
    startDate = pd.Timestamp("2020-01-01")
    endDate = pd.Timestamp("2020-01-01")

    starts = [start for (start, _) in intervals(start_date=startDate, end_date=endDate, freq=pd.Timedelta(days=20))]
    ends = [end for (_, end) in intervals(start_date=startDate, end_date=endDate, freq=pd.Timedelta(days=20))]

    assert starts[0] == startDate
    assert ends[0] == endDate
    assert len(starts) == 1
    assert len(starts) == len(ends)


def test_one_day():
    startDate = pd.Timestamp("2020-01-01")
    endDate = pd.Timestamp("2020-01-02")

    starts = [start for (start, _) in intervals(start_date=startDate, end_date=endDate, freq=pd.Timedelta(days=1))]
    ends = [end for (_, end) in intervals(start_date=startDate, end_date=endDate, freq=pd.Timedelta(days=1))]

    assert starts[0] == startDate
    assert ends[0] == endDate
    assert len(starts) == 1
    assert len(starts) == len(ends)

