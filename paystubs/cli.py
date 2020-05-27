from curses import wrapper


class CursesJournalEntryBox:
    def __init__(self, stdscr):
        self.x = 0
        self.y = 0
        self.state = 0
        self.entries = []
        self.scr = stdscr
        self.scr.clear()
        self.is_debit = True
        self.acct = ""
        self.amt = ""
        self.has_decimal = False
        self.comment = ""

    def get_side(self):
        """ Get either 'debit' or 'credit' from the user. """
        key = self.scr.getkey()
        if key == 'd':
            self.scr.addstr(self.y, self.x, 'dr. ')
            self.x = len('dr.')
            self.state += 1
            self.is_debit = True
        elif key == 'c':
            self.scr.addstr(self.y, self.x, '    cr. ')
            self.x = len('    cr.')
            self.state += 1
            self.is_debit = False
        elif key == '\n':
            self.state = 3
        else:
            self.scr.addstr(self.y, self.x, '?')
        self.scr.refresh()

    def get_acct(self):
        key = self.scr.getkey()
        if key == '\n':
            self.state += 1
            if self.is_debit:
                # The third column should start after we can safely
                # print at least the following COGS credit entry.
                self.x = len('        cr. COST OF GOODS SOLD ')
            else:
                # The fourth column should start after the the debit
                # column and after we can safely display a 5 figure
                # number
                self.x = len('        cr. COST OF GOODS SOLD $12,345.67 ')
            self.scr.addstr(self.y, self.x, '$')
            self.x += 1

        elif key == 'KEY_BACKSPACE':
            # Don't let the user backspace beyond just entering the account.
            if self.is_debit and self.x == len('dr.'):
                return
            elif not self.is_debit and self.x == len('    cr.'):
                return
            self.scr.addstr(self.y, self.x, ' ')
            self.x -= 1
            self.acct = self.acct[:-1]

        else:
            self.acct += key
            self.x += 1
            self.scr.addstr(self.y, self.x, key)
        self.scr.refresh()

    def display_amt(self):
        if not self.amt:
            return
        amt = 0
        if self.amt[-1] == '.':
            amt = float(self.amt[:-1])
        else:
            amt = float(self.amt)
        self.scr.addstr(self.y, self.x, '{:,.2f}'.format(amt).rjust(len('10,000.00')))

    def get_amt(self):
        key = self.scr.getkey()
        if key == '.' and self.has_decimal:
            return
        elif key == '.' and not self.has_decimal:
            self.has_decimal = True
            self.amt += key
        elif key == 'KEY_BACKSPACE':
            if self.amt and self.amt[-1] == '.':
                self.has_decimal = False
            if self.amt:
                self.amt = self.amt[:-1]
        elif key == '\n':
            if self.is_debit:
                self.entries.append(("dr.", self.acct, float(self.amt)))
            else:
                self.entries.append(("cr.", self.acct, float(self.amt)))
            self.amt = ''
            self.acct = ''
            self.has_decimal = False
            self.x = 0
            self.y += 1
            self.state = 0
            self.display_amt()
            self.scr.addstr('\n')
            return
        elif key in [str(i) for i in range(10)]:
            self.amt += key
        self.display_amt()
        self.scr.refresh()

    def display_comment_prompt(self):
        self.scr.addstr(self.y, self.x, "Comment: ")
        self.x += len("Comment:")
        self.state = 4

    def get_comment(self):
        key = self.scr.getkey()

        if key == '\n':
            self.state += 1
            self.y += 2
            self.scr.addstr(self.y, 0, 'Adding journal entry database.')

        elif key == 'KEY_BACKSPACE':
            # Don't let the user backspace too much.
            if self.x == len('Comment:'):
                return
            self.scr.addstr(self.y, self.x, ' ')
            self.x -= 1
            self.acct = self.comment[:-1]
            self.scr.refresh()

        else:
            self.comment += key
            self.x += 1
            self.scr.addstr(self.y, self.x, key)
            self.scr.refresh()


def entry_cli(stdscr):
    entry = CursesJournalEntryBox(stdscr)

    while True:
        if entry.state == 0:
            entry.get_side()
        elif entry.state == 1:
            entry.get_acct()
        elif entry.state == 2:
            entry.get_amt()
        elif entry.state == 3:
            entry.display_comment_prompt()
        elif entry.state == 4:
            entry.get_comment()
        else:
            break

    return entry


def get_booking():
    return wrapper(entry_cli)
