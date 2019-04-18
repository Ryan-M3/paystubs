#!/usr/bin/env python3

import sys
import locale
from datetime import timedelta

from booking import Booking

locale.setlocale(locale.LC_ALL, '')


def parse_time(string):
    h, m = string.split(":")
    return timedelta(hours=int(h), minutes=int(m))


def calculate_time(times):
    total = timedelta(seconds=0)
    # We take two times at a  time, because I have to record
    # when I started work and when I stopped.
    for i in range(0, len(times), 2):
        # We have to take into  account that I use a 12-hour
        # clock, so we  assume that if I work from  12 to 1,
        # then  that's just  an  hour of  work  and not  13.
        # However, in the rare case  that I actually do work
        # 12 hours straight without a single lunch break, we
        # can just  stop and  then immediately start  at the
        # same time and the program is fine with that.
        if times[i+1] < times[i]:
            total += (times[i+1] + timedelta(hours=12)) - times[i]
        else:
            total += times[i+1] - times[i]
    return total


def calc_wages(dur, rate):
    return float(dur.total_seconds()) / 60**2 * rate


def print_results(total_hrs, wages, taxes):
    print("Wage calculation:")
    # We don't care about seconds, so we ignore the last three characters in
    # total_hrs.
    print("\ttotal: ", str(total_hrs)[:-3])
    print("\twages: ", locale.currency(wages, grouping=True))
    print("\ttaxes: ", locale.currency(taxes, grouping=True))


def dispatch(save, date, hourly_rate, tax_rate, time_args):
    """
    Tie together all the functions of this program into one convenient function.
    """
    times = list(map(parse_time, time_args))
    total_hrs = calculate_time(times)
    wages = calc_wages(total_hrs, hourly_rate)
    taxes = wages * tax_rate
    print_results(total_hrs, wages, taxes)
    entries = [
        (date, save.get_ref("Wages Receivable"), -wages),
        (date, save.get_ref("Tax Expense")     , -taxes),
        (date, save.get_ref("Taxes Payable")   ,  taxes),
        (date, save.get_ref("Wages")           ,  wages)
    ]
    h = total_hrs.seconds // 60**2
    m = total_hrs.seconds % 60
    comment = "Worked {0} hours and {1} minutes.".format(h, m)
    save.add_booking(Booking(entries, comment))
