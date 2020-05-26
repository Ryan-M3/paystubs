from data.empty_booking import EmptyBooking


def show_last(save, n):
    for entry_id in save.get_most_recent_entry_ids(n):
        booking = EmptyBooking(save)
        booking.load(entry_id)
        print(booking)


def show_containing(save, ref):
    for entry_id in save.get_entries_containing(ref):
        booking = EmptyBooking(save)
        booking.load(entry_id)
        print(booking)
