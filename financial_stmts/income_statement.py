from financial_stmts.abc import FinancialStatement, TAB


class IncomeStatement(FinancialStatement):
    def print(self):
        self.print_header()
        self.print_section("revenues", 3)
        self.print_section("expenses", 4)
        self.print_section("gains", 5)
        self.print_section("losses", 6)
        self.print_grand_total("Spending Money", dr_bal=False)
        print()
