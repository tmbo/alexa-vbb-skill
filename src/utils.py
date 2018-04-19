from datetime import datetime

import pytz
from dateutil.relativedelta import relativedelta


def wait_time_in_minutes(time):
    diff = relativedelta(pytz.timezone('Europe/Berlin').localize(time),
                         datetime.now(pytz.timezone("Europe/Berlin")))
    return (diff.days * 24 + diff.hours) * 60 + diff.minutes


def wait_time(time):
    diff = relativedelta(pytz.timezone('Europe/Berlin').localize(time),
                         datetime.now(pytz.timezone("Europe/Berlin")))
    return diff.hours + diff.days * 24, diff.minutes


def wait_time_str(time):
    def proper_suffix(value, unit, multiple):
        if value == 0:
            return ""
        elif value > 1:
            return "{} {}{}".format(value, unit, multiple)
        else:
            return "{} {}".format(value, unit)

    hours, minutes = wait_time(time)
    return (proper_suffix(hours, "Stunde", "n") +
            proper_suffix(minutes, "Minute", "n"))


def voice_join(els, and_word="und"):
    if len(els) == 0:
        return ""
    elif len(els) == 1:
        return els[0]
    else:
        firsts = ", ".join(els[:-1])
        return " ".join([firsts, and_word, els[-1]]).strip()
