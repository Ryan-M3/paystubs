from collections import defaultdict

from financial_stmts.abc  import FinancialStatement, TAB
from data.acct_types      import AcctType
from formatting.fmt_money import fmt_money
from formatting.colors    import Colors
from formatting.colors    import wrap_color


class BalanceSheet(FinancialStatement):
    def print(self):
        self.print_header()
        self.print_section("assets", 0)
        self.print_section("liabilities", 1)
        self.print_section("equity", 2)
        self.print_grand_total("Total Equity")
        print()
