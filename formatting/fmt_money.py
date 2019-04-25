from formatting.colors import Colors


def fmt_money(value):
    if type(value) in [int, float] and value < 0:
        # If we don't  add back that extra  space before the parenthesis, the
        # parenthesis  will cause the cents columns to no longer align with
        # previous items.
        return "$" + Colors.RED + " ({:6,.2f})".format(abs(value)) + Colors.ENDC
    else:
        return "${:10,.2f}".format(value)
