def wrap_color(msg, color):
    return color + msg + Colors.ENDC


class Colors:
    RED   = "\033[38;5;1m"
    GREEN = "\033[38;5;2m"
    CYAN  = "\033[38;5;3m"
    ENDC  = "\033[0m"
