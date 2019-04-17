#!/usr/bin/env python3

import argparse
from datetime import datetime

import wage_calc
from booking    import Booking
from save_file  import SaveFile
from exceptions import AccountMissingError


def parse_terminal():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--book', action='store_true')
    parser.add_argument('-t', '--test', action='store_true')
    parser.add_argument('-s', '--summarize', nargs=1)
    parser.add_argument('-l', '--list', action='store_true')
    parser.add_argument('--coa', action='store_true', help="Chart of Accounts")

    subparsers = parser.add_subparsers()
    wage_parser = subparsers.add_parser("wages")
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
        save.summarize_account(parsed.summarize[0], line_char=chr(9188), sum_line_char=chr(9552))
    elif parsed.list or parsed.coa:
        save.list_accounts()
    elif parsed.test:
        print(save.get_capital(0))
    elif parsed.times and parsed.date and parsed.tax:
        wage_calc.dispatch(
            save,
            parsed.date[0],
            float(parsed.wage[0]),
            float(parsed.tax[0]),
            parsed.times
        )
    else:
        print("Invalid command line arguments.")


if __name__ == "__main__":
    main()
