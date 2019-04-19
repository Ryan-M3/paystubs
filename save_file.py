import sqlite3 as sql
import locale
import os

from acct_types import AcctType
from exceptions import AccountMissingError

locale.setlocale(locale.LC_ALL, '')


class SaveFile:
    def __init__(self, save_path, save_name):
        if save_path[0] == "~":
            save_path = os.path.expanduser("~") + save_path[1:]

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        self.cnx = sql.connect(save_path + save_name)
        self.cursor = self.cnx.cursor()

        self.cursor.execute('PRAGMA foreign_keys = ON;')
        self.cnx.commit()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ChartOfAccounts(
              ref INTEGER PRIMARY KEY,
              account STRING,
              acctType INT
            );
        ''')
        self.cnx.commit()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Journal(
              journalID INTEGER PRIMARY KEY AUTOINCREMENT,
              entryID INTEGER,
              date STRING,
              amt  FLOAT,
              ref  INTEGER REFERENCES ChartOfAccounts(ref)
            );
        ''')
        self.cnx.commit()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Comments(
              commentID INTEGER PRIMARY KEY AUTOINCREMENT,
              entryID INTEGER,
              comment TEXT
            );
        ''')
        self.cnx.commit()

    def add_account(self, ref, acct, category: AcctType):
        self.cursor.execute(
            '''INSERT INTO ChartOfAccounts (ref, account, acctType)
               VALUES (?, ?, ?);''',
            (ref, acct, category.value)
        )
        self.cnx.commit()

    def add_booking(self, booking):
        entry_id = self._last_entry_id() + 1
        journal_id = self._last_journal_id()
        for date, ref, amt in booking.entries:
            journal_id += 1
            self.cursor.execute(
                '''INSERT INTO Journal (journalID, entryID, date, ref, amt)
                   VALUES (?, ?, ?, ?, ?);''',
                (journal_id, entry_id, date, ref, amt)
            )
            self.cnx.commit()
        self.cursor.execute('''INSERT INTO Comments (entryID, comment)
                               VALUES (?, ?);''',
                            (entry_id, booking.comment))
        self.cnx.commit()

    def is_balanced(self):
        self.cursor.execute("SELECT SUM(amt) FROM Journal;")
        return round(self.cursor.fetchall()[0][0], 3) == 0.00

    def account_balance(self, ref):
        self.cursor.execute('''SELECT COALESCE(SUM(amt), 0)
                               FROM Journal
                               WHERE ref=?;''', (ref,))
        return self.cursor.fetchone()[0]

    def get_ref(self, acct_title):
        self.cursor.execute('''SELECT ref
                               FROM ChartOfAccounts
                               WHERE account=?;''',
                            (acct_title,))
        ref = self.cursor.fetchall()
        if not ref:
            raise AccountMissingError
        return ref[0][0]

    def get_acct_title(self, ref):
        self.cursor.execute('''SELECT account
                               FROM ChartOfAccounts
                               WHERE ref=?;''', (ref,))
        return self.cursor.fetchone()[0]

    def summarize_account(self, acct_title, line_char="-", sum_line_char="="):
        # The coalesce here prevents sum from return None if there's no items
        # to sum up, when logically it should be zero here.
        self.cursor.execute("""SELECT COALESCE(SUM(amt), 0)
                               FROM Journal
                               WHERE amt < 0 AND ref=?;
                            """, (self.get_ref(acct_title),))
        dr = self.cursor.fetchone()[0]
        self.cursor.execute("""SELECT COALESCE(SUM(amt), 0)
                               FROM Journal
                               WHERE amt > 0 AND ref=?;
                            """, (self.get_ref(acct_title),))
        cr = self.cursor.fetchone()[0]
        total = dr + cr
        dr_cur = locale.currency(dr * -1, grouping=True)
        cr_cur = locale.currency(cr, grouping=True)
        total_cur = locale.currency(abs(total), grouping=True)
        print()
        print("\t", acct_title.center(23))
        print("\t", line_char * 23)
        print("\t", dr_cur.rjust(10), "|", cr_cur.ljust(10))
        print("\t", line_char * 23)
        if total == 0:
            print("\t", "-0-".center(10), " ", "-0-".center(10))
        elif total < 0:
            print("\t", total_cur.rjust(10))
            print("\t", (sum_line_char * len(total_cur)).rjust(10))
        else:
            print("\t", " " * 10, total_cur.ljust(10))
            print("\t", " " * 13 + (sum_line_char * len(total_cur)).ljust(10))
        print()

    def list_accounts(self):
        self.cursor.execute('SELECT * FROM ChartOfAccounts;')
        for ref, title, acctType in self.cursor.fetchall():
            if acctType == '':
                continue
            print(str(ref).ljust(5), title.ljust(20), AcctType(acctType).name)
        print()

    def accounts_by_type(self, acctType):
        self.cursor.execute('''SELECT ref
                               FROM ChartOfAccounts
                               WHERE acctType=?''', (acctType,))
        return [row[0] for row in self.cursor.fetchall()]

    def account_type_balances(self, acct_type):
        """Return the account balances for every account of a certain type."""
        self.cursor.execute('''SELECT SUM(amt)
                               FROM Journal
                               WHERE ref IN
                                   (SELECT ref
                                    FROM ChartOfAccounts
                                    WHERE acctType=?);
                            ''', (acct_type,))
        return self.cursor.fetchone()[0]

    def get_capital(self, acct_type):
        return self.account_type_balances(0) + self.account_type_balances(1)

    def entries_by_date(self, ref, oldest="1970-01-01", newest="now"):
        self.cursor.execute('''SELECT date, amt
                               FROM Journal
                               WHERE date(date)
                               BETWEEN date(?) AND date(?)
                               AND ref=?;
                            ''', (oldest, newest, ref))
        return self.cursor.fetchall()

    def _last_entry_id(self):
        self.cursor.execute('''SELECT entryID
                               FROM Journal
                               ORDER BY entryID DESC
                               LIMIT 1;''')
        fetched = self.cursor.fetchall()
        if fetched:
            return fetched[0][0]
        else:
            return 0

    def _last_journal_id(self):
        self.cursor.execute('''SELECT journalID
                               FROM Journal
                               ORDER BY journalID
                               DESC LIMIT 1;''')
        fetched = self.cursor.fetchall()
        if fetched:
            return fetched[0][0]
        else:
            return 0

    def __exit__(self):
        self.cnx.close()
