from acct_types import AcctType
from fmt_money import fmt_money
from colors import Colors
from colors import wrap_color

from collections import defaultdict


TAB = " " * 4

class FinancialStatement:
    def __init__(self, save, stmt_title="Report", title_width=35, bal_width=9):
        self.save = save
        self.totals = defaultdict(int)
        self.title_width = title_width
        self.bal_width = bal_width
        self.stmt_title = stmt_title.upper()

    def print_header(self):
        stmt_width = self.title_width + self.bal_width
        header = "{0}".format(self.stmt_title).center(stmt_width)
        print()
        print(header)
        print("YTD".center(stmt_width))
        print()

    def print_section(self, section_title, acct_type):
        print(section_title.upper())
        for ref in self.save.accounts_by_type(acct_type):
            balance = self.save.account_balance(ref)
            self.totals[section_title] += balance
            acct_title = self.save.get_acct_title(ref).ljust(self.title_width)
            bal_money = fmt_money(abs(balance)).rjust(self.bal_width)
            print(TAB + acct_title + bal_money)
        total_str = fmt_money(abs(self.totals[section_title]))
        # An extra two spaces is needed for the underlines, but not the total
        # string because fmt_money adds a "$" and a space we don't care about.
        empty_title = " ".ljust(self.title_width)
        print(TAB + empty_title + "  " + "-" * self.bal_width)
        print(TAB + empty_title + total_str.rjust(self.bal_width))
        print(TAB + empty_title + "  " + "-" * self.bal_width)

    def print_grand_total(self, acct_title="Grand Total", dr_bal=True):
        grand_total = sum(self.totals.values())
        if dr_bal:
            grand_total *= -1
        total_str = fmt_money(grand_total).rjust(self.bal_width)
        if grand_total > 0:
            total_str = wrap_color(total_str, Colors.GREEN)
        acct_title = acct_title.ljust(self.title_width) + TAB
        print("\n" + acct_title + total_str)
        empty_title = "    " + " ".ljust(self.title_width)
        print(empty_title + "  " + "=" * self.bal_width)
