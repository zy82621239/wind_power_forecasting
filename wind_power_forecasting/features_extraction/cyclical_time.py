from typing import List

import numpy as np
import pandas as pd

from tsmodeling.features.time import compute_second_of_minute
from wind_power_forecasting.features_extraction.time import compute_minute_of_day


def add_cycle_time_descriptor(df: pd.DataFrame,
                              max_value: int,
                              time_descriptor=None,
                              index_attribute: str = None,
                              trig_func_list: List[np.ufunc] = None,
                              label: str = None,
                              label_prefix: str = 'cyclical_',
                              copy=True):
    if time_descriptor is None and index_attribute is None:
        # TODO
        raise ValueError('TODO')

    if time_descriptor is not None and index_attribute is not None:
        # TODO
        raise ValueError('TODO')

    if index_attribute is not None:
        time_descriptor = getattr(df.index, index_attribute)

    if trig_func_list is None:
        trig_func_list = [np.sin, np.cos]

    if copy:
        df = df.copy()

    if label is None:

        if index_attribute is not None:
            label = 'cyclical_' + index_attribute
        else:
            # TODO
            raise ValueError('TODO')

    for trig_func in trig_func_list:
        trig_func_str = trig_func.__name__
        final_label = label_prefix + label + '_' + trig_func_str
        df[final_label] = cycle_transformation(time_descriptor, max_value, trig_func)

    return df


def add_cyclical_hour_of_day(df, added_label='hour_of_day', copy=False):
    df = add_cycle_time_descriptor(df, max_value=24, index_attribute='hour', label=added_label, copy=copy)

    return df


def add_cyclical_half_hour_of_day(df, added_label='half_hour_of_day', copy=False):
    df = add_cycle_time_descriptor(df, max_value=12, time_descriptor=df.index.hour, label=added_label, copy=copy)

    return df


def add_cyclical_week_of_year(df, added_label='week_of_year', copy=False):
    # TODO manage case when nb weeks == 53
    # from: https://www.timeanddate.com/date/week-numbers.html
    # The weeks of the year are numbered from week 1 to 52 or 53 depending on several factors.
    # Most years have 52 weeks but if the year starts on a Thursday or is a leap year that starts on a Wednesday,
    # that particular year will have 53 numbered weeks.
    # These week numbers are commonly used in some European and Asian countries; but not so much in the United States.
    nb_week = 52
    df = add_cycle_time_descriptor(df, max_value=nb_week, index_attribute='week', label=added_label, copy=copy)

    return df


def add_cyclical_month_of_year(df, added_label='month_of_year', copy=False):
    df = add_cycle_time_descriptor(df, max_value=12, index_attribute='month', label=added_label, copy=copy)

    return df


def add_cyclical_day_of_week(df, added_label='day_of_week', copy=False):
    df = add_cycle_time_descriptor(df, max_value=7, index_attribute='dayofweek', label=added_label, copy=copy)

    return df


def add_cyclical_day_of_month(df, added_label='day_of_month', copy=False):
    df = add_cycle_time_descriptor(df, max_value=df.index.daysinmonth, index_attribute='dayofweek', label=added_label,
                                   copy=copy)

    return df


def add_cyclical_minute_of_hour(df, added_label='minute_of_hour', copy=False):
    df = add_cycle_time_descriptor(df, max_value=60, index_attribute='minute', label=added_label, copy=copy)

    return df


def add_cyclical_minute_of_day(df, added_label='minute_of_day', copy=False):
    min_of_day = compute_minute_of_day(df.index)
    df = add_cycle_time_descriptor(df, max_value=1440, time_descriptor=min_of_day, label=added_label, copy=copy)

    return df


def add_cyclical_second_of_minute(df, added_label='second_of_minute', copy=False):
    sec_min = compute_second_of_minute(df.index)
    df = add_cycle_time_descriptor(df, max_value=60, time_descriptor=sec_min, label=added_label, copy=copy)

    return df


def cycle_transformation(num, denom, trig_func):
    valid_func = [np.sin, np.cos]

    if trig_func not in valid_func:
        raise ValueError(trig_func, valid_func)

    return trig_func(2 * np.pi * num / denom)