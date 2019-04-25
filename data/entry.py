from datetime  import datetime

from formatting.colors    import Colors
from formatting.colors    import wrap_color
from formatting.fmt_money import fmt_money


class Entry:
    def __init__(self, date, title, ref, amt):
        self.date  = self._fmt_date(date)
        self.title = title
        self.ref   = self._fmt_ref(ref)
        self.amt   = self._fmt_amt(amt)

    def _fmt_date(self, date):
        try:
            return datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            error_msg = "Expected a YYYY-MM-DD date, but got " + date
            raise ValueError(wrap_color(error_msg, Colors.RED))

    def _fmt_ref(self, ref):
        try:
            return int(ref)
        except ValueError:
            error_msg = "Got {0}, but expected an integer.".format(ref)
            raise ValueError(wrap_color(error_msg, Colors.RED))

    def _fmt_amt(self, amt):
        try:
            return float(amt)
        except ValueError:
            error_msg = "Expected a floating point "\
                        "number, but got {0}.".format(amt)
            raise ValueError(wrap_color(error_msg, Colors.RED))

    def fmt(self,
            show_date    =  False,
            date_fmt     =  "%D",
            date_pad     =     3,
            title_width  =    27,
            indent_width =     4,
            ref_width    =     6,
            ref_pad      =     3,
            num_width    =    10,
            num_col_pad  =     3):

        s = ""
        date_str = datetime.strftime(self.date, date_fmt)

        if show_date:
            s += date_str
        else:
            s += " " * len(date_str)

        s += " " * date_pad
        is_credit = self.amt > 0.0
        if is_credit:
            s += " " * indent_width
            s += self.title.ljust(title_width - indent_width)
        else:
            s += self.title.ljust(title_width)

        s += str(self.ref).rjust(ref_width) + " " * ref_pad
        if is_credit:
            s += " " * (num_width + num_col_pad)
        s += fmt_money(abs(self.amt))
        return s

    def __str__(self):
        return self.fmt()

    def __repr__(self):
        return self.fmt()
