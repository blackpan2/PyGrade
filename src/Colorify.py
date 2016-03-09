_author__ = 'George Herde'


def grey(string):
    return "\033[1;30m" + string + "\033[1;m"


def red(string):
    return "\033[1;31m" + string + "\033[1;m"


def green(string):
    return "\033[1;32m" + string + "\033[1;m"


def yellow(string):
    return "\033[1;33m" + string + "\033[1;m"


def blue(string):
    return "\033[1;34m" + string + "\033[1;m"


def magenta(string):
    return "\033[1;35m" + string + "\033[1;m"


def cyan(string):
    return "\033[1;36m" + string + "\033[1;m"


def white(string):
    return "\033[1;37m" + string + "\033[1;m"


def crimson(string):
    return "\033[1;38m" + string + "\033[1;m"


def highlight_red(string):
    return "\033[1;41m" + string + "\033[1;m"


def highlight_green(string):
    return "\033[1;42m" + string + "\033[1;m"


def highlight_brown(string):
    return "\033[1;43m" + string + "\033[1;m"


def highlight_blue(string):
    return "\033[1;44m" + string + "\033[1;m"


def highlight_magenta(string):
    return "\033[1;45m" + string + "\033[1;m"


def highlight_cyan(string):
    return "\033[1;46m" + string + "\033[1;m"


def highlight_grey(string):
    return "\033[1;47m" + string + "\033[1;m"


def highlight_crimson(string):
    return "\033[1;48m" + string + "\033[1;m"
