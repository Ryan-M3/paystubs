from financial_statement import FinancialStatement, TAB
from acct_types import AcctType
from fmt_money import fmt_money
from colors import Colors
from colors import wrap_color

from collections import defaultdict


class BalanceSheet(FinancialStatement):
    def print(self):
        self.print_header()
        self.print_section("assets", 0)
        self.print_section("liabilities", 1)
        self.print_section("equity", 2)
        self.print_grand_total("Total Equity")
