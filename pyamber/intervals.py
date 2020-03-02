import pandas as pd


def intervals(startDate=None, endDate=None, freq=pd.Timedelta(days=20)):
    stamps = pd.date_range(start=startDate, end=endDate, freq=freq)
    stamps = stamps.insert(-1, endDate).sort_values().drop_duplicates()

    for start, end in zip(stamps[:-1], stamps[1:]):
        yield start, end
