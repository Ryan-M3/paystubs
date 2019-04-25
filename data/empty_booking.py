import textwrap
from data.entry   import Entry
from data.booking import Booking


class EmptyBooking:
    def __init__(self, savef):
        self.savef   = savef
        self.entries = []
        self.comment = ""

    def load(self, entry_id):
        for date, amt, ref in self.savef.get_entries_by_entry_id(entry_id):
            title = self.savef.get_acct_title(ref)
            self.entries.append(Entry(date, title, ref, amt))
        self.comment = self.savef.get_comment(entry_id)

    def set(self, entries, comment):
        self.entries += entries
        self.comment = comment

    def save(self, entry_id):
        self.savef.add_booking(Booking(self.entries, self.comment))

    def __str__(self):
        self.entries = sorted(self.entries, key=lambda k: k.amt)
        s = ""
        s += self.entries[0].fmt(show_date=True) + "\n"
        for entry in self.entries[1:]:
            s += entry.fmt() + "\n"
        s += "\033[1;2m"
        for line in textwrap.wrap(self.comment):
            s += line.center(80)
        s += "\033[0m"
        s += "\n\n"
        return s

    def __repr__(self):
        return self.__str__()
