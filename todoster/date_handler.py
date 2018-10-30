import re
import datetime

from isoweek import Week


def is_past_date(date):
    if not date:
        return False

    return date < datetime.date.today().isoformat()


def is_valid_date_format(date):
    dot_notation = '^\d{1,2}\.\d{1,2}((\.)|(\.(\d{4}|\d{2})))?$'
    dash_notation = '^\d{1,2}/\d{1,2}(/(\d{4}|\d{2}))?$'
    iso_notation = '^\d{4}-\d{2}-\d{2}$'

    return re.match(dot_notation + "|" + iso_notation + "|" + dash_notation, date)


def format_date(date):
    if "." in date:
        date_list = date.split(".")
    elif "-" in date:
        date_list = date.split("-")
        date_list.reverse()
    elif "/" in date:
        date_list = date.split("/")

    day = date_list[0].rjust(2, "0")
    month = date_list[1].rjust(2, "0")

    if len(date_list) == 3 and date_list[2]:
        year = date_list[2] if len(date_list[2]) == 4 else "20" + date_list[2]
    else:
        today = datetime.date.today()
        supplied_date = datetime.date(today.year, int(month), int(day))
        year = today.year+1 if supplied_date < today else today.year

    return datetime.date(int(year), int(month), int(day))


def is_valid_week_format(week):
    week_format = '((W|w)\d{1,2})'
    seperator = '(-|/)'
    year_format = '(\d{2}|\d{4})'

    my_notation = '^' + week_format + '(' + seperator + year_format + ')?' + '$'
    my_rev_notation = '^' + year_format + seperator + week + '$'
    iso_notation = '^' + year_format + '-?' + week_format + '$'
    return re.match(my_notation + "|" + my_rev_notation + "|" + iso_notation, week)


def is_past_week(week):
    if not week:
        return False

    return Week.fromstring(week) < Week.thisweek()


def format_week(week):
    week = week.lower()

    if "-" in week:
        week_list = week.split("-")
    elif "/" in week:
        week_list = week.split("/")
    elif "w" in week:
        week_list = week.split("w")
    else:
        week_list = ["", week]

    if "w" in week_list[0]:
        week_number = week_list[0].replace("w", "").rjust(2, "0")
        year = ("20" + week_list[1]) if len(week_list[1]) == 2 else week_list[1]
    else:
        week_number = week_list[1].replace("w", "").rjust(2, "0")
        year = "20" + week_list[0] if len(week_list[0]) == 2 else week_list[0]

    if not year:
        this_week = Week.thisweek()
        if int(week_number) < this_week.week:
            year = str(this_week.year + 1)
        else:
            year = str(this_week.year)

    return Week.fromstring(year + "W" + week_number)


def get_week_from_date(date):
    return Week.withdate(date)
