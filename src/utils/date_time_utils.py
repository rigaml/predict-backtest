
from datetime import datetime

SECONDS_IN_HOUR = 60 * 60
SECONDS_IN_DAY = 24 * SECONDS_IN_HOUR


def time_fraction_of_day(datetime_str):
    """
    Converts the time in a datetime string to a value between 0 and 1 representing the fraction of a day.
    """
    dt = datetime.fromisoformat(datetime_str)

    seconds_since_start_of_day = dt.hour * SECONDS_IN_HOUR + dt.minute * 60 + dt.second

    fraction_of_day = seconds_since_start_of_day / SECONDS_IN_DAY
    return fraction_of_day
