from exceptions import UnbalancedEntriesError
from exceptions import MismatchingDatesError
from exceptions import MissingCommentError


class Booking:
    def __init__(self, entries, comment):
        if round(sum([entry[-1] for entry in entries]), 2) != 0:
            raise UnbalancedEntriesError

        if not all([entry[0] == entries[0][0] for entry in entries]):
            raise MismatchingDatesError

        # All entries must be commented.
        if not len(comment):
            raise MissingCommentError

        self.entries = entries
        self.comment = comment

    def __iter__(self):
        for entry in self.entries:
            yield entry
