from formatting.colors import Colors, wrap_color


class UnbalancedEntriesError(Exception):
    def __str__(self):
        error_msg = "The sum of debits must equal the sum of credits."
        return wrap_color(error_msg, Colors.RED)
    pass


class MismatchingDatesError(Exception):
    def __str__(self):
        error_msg = "Matching debits and credits in a booking must "\
                    "be on the same day."
        return wrap_color(error_msg, Colors.RED)


class MissingCommentError(Exception):
    def __str__(self):
        error_msg = "All bookings must contain a comment."
        return wrap_color(error_msg, Colors.RED)


class AccountMissingError(Exception):
    def __str__(self):
        error_msg = "The account does not exist or cannot be found."
        return wrap_color(error_msg, Colors.RED)
