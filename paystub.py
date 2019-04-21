#!/usr/bin/env python3

import argparse
from datetime import datetime

import wage_calc
import date_plot
from booking          import Booking
from save_file        import SaveFile
from exceptions       import AccountMissingError
from balance_sheet    import BalanceSheet
from income_statement import IncomeStatement
from acct_types       import AcctType


def parse_terminal():
    parser = argparse.ArgumentParser()
    parser.set_defaults(which='main')
    parser.add_argument('-b', '--book', action='store_true')
    parser.add_argument('-t', '--test', action='store_true')
    parser.add_argument('-s', '--summarize', nargs=1)
    parser.add_argument('-l', '--list', action='store_true')
    parser.add_argument('-I', '--income-statement', action='store_true')
    parser.add_argument('-B', '--balance-sheet', action='store_true')
    parser.add_argument('-#', '--ref', nargs=1)
    parser.add_argument(
        '--account-type',
        nargs=1,
        type=int,
        help="Specifies the account type. Key:"
             "\n\t0 - Asset"
             "\n\t1 - Liability"
             "\n\t2 - Capital"
             "\n\t3 - Revenue"
             "\n\t4 - Expense"
             "\n\t5 - Gain"
             "\n\t6 - Loss"
             "\n\t7 - Contra"
             "\n\t8 - Adjunct"
    )
    parser.add_argument(
        '--add-account',
        nargs=1,
        help="Add a new account. Requires the --ref argument "
             "and the --account-type argument."
    )

    subparsers = parser.add_subparsers()
    wage_parser = subparsers.add_parser("wages")
    wage_parser.set_defaults(which='wages')
    wage_parser.add_argument(
        '-d', '--date',
        nargs=1,
        help='The date on which wages were earned (not paid). Must be in the'
             'format of "2025-12-31."'
    )
    wage_parser.add_argument(
        '-w', '--wage',
        nargs=1,
        help="hourly wage rate"
    )
    wage_parser.add_argument(
        '-x', '--tax',
        nargs=1,
        help="estimate tax rate"
    )
    wage_parser.add_argument(
        '-t', '--times',
        nargs="*",
        help="List of start and stop times, one after the other in "
             "chronological order, that you were at work."
    )

    plot_parser = subparsers.add_parser('plot')
    plot_parser.set_defaults(which='plot')
    plot_parser.add_argument('-H', '--histogram', action='store_true')
    plot_parser.add_argument(
        '-s', '--start-date',
        nargs=1,
        help = "The oldest entry to plot in the format of YYYY-MM-DD. "
               "'unixepoch' is also an acceptable date."
    )
    plot_parser.add_argument(
        '-e', '--end-date',
        nargs=1,
        help = "The newest entry to plot. Must be in the format of YYYY-MM-DD. "
               "'now' is also an acceptable date."
    )
    plot_parser.add_argument('-#', '--ref', nargs=1)
    return parser.parse_args()


def parse_entry(date, text, save_file):
    tokens = text.split()
    if len(tokens) < 3:
        raise RuntimeError("Invalid debit or credit entry.")

    ref = None
    try:
        ref = int(tokens[1])
    except ValueError:
        ref = save_file.get_ref(" ".join(tokens[1:-1]))
    if ref is None:
        raise AccountMissingError

    amt = float(tokens[-1])

    if amt < 0:
        print("\033[202mWarning: negative value entered. "
              "This is very rare in accounting.")

    if tokens[0] in ["dr.", "dr", "debit", "debitere"]:
        amt *= -1
    elif tokens[0] not in ["cr.", "cr", "credit", "creditere"]:
        return RuntimeError("All entries must be debits or credits.")

    return (date, ref, amt)


def get_booking_from_terminal(save):
        date = input("Enter date (blank for today): ")
        if not date:
            now   = datetime.now()
            year  = now.year
            month = str(now.month).zfill(2)
            day   = str(now.day).zfill(2)
            date  = "{0}-{1}-{2}".format(year, month, day)

        print("Enter dr./cr. entries one-by-one, followed by a blank line.")
        entries = []
        while True:
            got = input("\t# ")
            if got == "":
                break
            entries.append(parse_entry(date, got, save))

        comment = input("Enter Comment:\n\t")

        return Booking(entries, comment)


def main():
    save = SaveFile("~/.config/paystubs/", "books.db")
    parsed = parse_terminal()
    if parsed.book:
        save.add_booking(get_booking_from_terminal(save))
    elif parsed.summarize:
        save.summarize_account(parsed.summarize[0])
    elif parsed.list:
        save.list_accounts()
    elif parsed.test:
        print(save.entries_by_date(parsed.ref[0]))
    elif parsed.income_statement:
        income_stmt = IncomeStatement(save, "Income Statement", title_width=25)
        income_stmt.print()
    elif parsed.balance_sheet:
        bs = BalanceSheet(save, "Balance Sheet", title_width=25)
        bs.print()
    elif parsed.which == "wages":
        wage_calc.dispatch(
            save,
            parsed.date[0],
            float(parsed.wage[0]),
            float(parsed.tax[0]),
            parsed.times
        )
    elif parsed.add_account:
        ref = parsed.ref[0]
        acct = parsed.add_account[0]
        category = parsed.account_type[0]
        save.add_account(ref, acct, AcctType(category))
    elif parsed.which == "plot":
        date_plot.dispatch(
            save,
            parsed.ref[0],
            save.get_acct_title(parsed.ref[0]),
            parsed.start_date[0],
            parsed.end_date[0],
            parsed.histogram
        )
    else:
        print("Invalid command line arguments.")


if __name__ == "__main__":
    main()
