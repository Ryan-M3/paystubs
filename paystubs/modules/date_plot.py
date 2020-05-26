import itertools
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.dates import WeekdayLocator, SU
from datetime import datetime as dt


def to_datetime(date_string):
    """Convert date strings into datetimes."""
    return dt.strptime(date_string, '%Y-%m-%d')


def plot_dates(date_strs, values, account_title):
    dates = list(map(to_datetime, date_strs))
    plt.plot(dates, values)

    # Format the bottom as dates.
    plt.gcf().autofmt_xdate()
    ax = plt.gca()

    # Only show tic marks forSundays.
    loc = WeekdayLocator(byweekday=SU)
    ax.xaxis.set_major_locator(loc)

    # Set the y-axis to display in dollars format.
    formatter = ticker.FormatStrFormatter('$%1.2f')
    ax.yaxis.set_major_formatter(formatter)

    plt.title(account_title)

    plt.show()


def plot_histogram(date_strs, values):
    raise NotImplementedError


def dispatch( save              ,
              ref               ,
              account_title     ,
              oldest="unixepoch",
              newest="now"      ,
              histogram=False   ):

    if oldest == "unixepoch":
        oldest = '1970-01-01'
    if newest == 'now':
        newest = dt.strftime(dt.now(), '%Y-%m-%d')
    entries = save.entries_by_date(ref, oldest, newest)
    date_strs, values = zip(*save.entries_by_date(ref, oldest, newest))
    if histogram:
        # Debits are represented as negative numbers, so we have to
        # undo that for our plot to be the right way up.
        values = list(map(abs, values))
        plot_histogram(date_strs, values)
    else:
        cum_values = itertools.accumulate(values)
        # Debits are represented as negative numbers, so we have to
        # undo that for our plot to be the right way up.
        cum_values = list(map(abs, cum_values))
        plot_dates(date_strs, cum_values, account_title)
