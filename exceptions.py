class UnbalancedEntriesError(Exception):
    def __str__(self):
        return "The sum of debits must equal the sum of credits."
    pass


class MismatchingDatesError(Exception):
    def __str__(self):
        return "Matching debits and credits in a booking must "\
               "be on the same day."


class MissingCommentError(Exception):
    def __str__(self):
        return "All bookings must contain a comment."


class AccountMissingError(Exception):
    def __str__(self):
        return "The account does not exist or cannot be found."
