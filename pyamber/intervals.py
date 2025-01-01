from __future__ import annotations

import pandas as pd


def intervals(
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
    freq: pd.Timedelta = pd.Timedelta(days=20),
):
    """
    Constructs an iterator (start_date, t2), (t2, t3), ..., (t_{n-1}, end_date). This is used to address the pagination
    of amberdata.

    :param start_date: First date
    :param end_date: Last date
    :param freq: Gap between Dates (this parameter is induced by amberdata)
    """
    assert start_date <= end_date

    if start_date == end_date:
        yield start_date, end_date
    else:
        # construct t1 = start_date, t2, t3, ... t_{n-1} <= end_date
        stamps = pd.date_range(start=start_date, end=end_date, freq=freq)
        # it's important to explicitly append the end_date. If end_date == t_{n-1} this step has no impact.
        stamps = stamps.insert(-1, end_date).sort_values().drop_duplicates()

        # stamps is now
        # t1 = start_date, t2, t3, ..., t_{n-1}, t_n = end_date

        yield from zip(stamps[:-1], stamps[1:])
