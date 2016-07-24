import pytz


def convert_timezone(x):
    return x.to_datetime().replace(tzinfo=pytz.utc).astimezone(pytz.timezone("Europe/Istanbul"))


def get_year(x):
    return convert_timezone(x).year


def get_month(x):
    return "{}-{:02}".format(convert_timezone(x).year, convert_timezone(x).month)


def get_day(x):
    return convert_timezone(x).day


def get_hour(x):
    return convert_timezone(x).hour


def get_min(x):
    return convert_timezone(x).minute


def get_sec(x):
    return convert_timezone(x).second


def get_day_of_the_week(x):
    return convert_timezone(x).weekday()


def get_exact_date(x):
    converted = convert_timezone(x)
    return "{:02}-{:02}-{}".format(converted.day, converted.month, converted.year)
