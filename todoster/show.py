from collections import defaultdict
import calendar
from datetime import timedelta, date
from isoweek import Week

from todoster.file_operations import load_tasks, load_projects
from todoster.output_formatter import format_task_block, format_string, format_headline
from todoster.date_handler import is_past_date, is_past_week


def show(args):
    try:
        show_done_tasks = args.show_completed_tasks
        show_past_tasks = args.show_past_tasks
        show_inactive_projects = args.show_all_projects
    except AttributeError:
        show_done_tasks = False
        show_past_tasks = False
        show_inactive_projects = False

    try:
        if args.sorting_by in ["p", "project"]:
            category_func = show_by_project
        elif args.sorting_by in ["b", "backlog"]:
            category_func = show_backlog
        elif args.sorting_by in ["d", "date"]:
            category_func = show_by_due_date
        elif args.sorting_by in ["i", "priority"]:
            category_func = show_by_priority
        elif args.sorting_by in ["l", "location"]:
            category_func = show_by_location
        else:
            category_func = show_default
    except AttributeError:
        category_func = show_default

    all_tasks, all_projects = _presort_data(not show_done_tasks, not show_past_tasks, not show_inactive_projects)
    category_func(all_tasks, all_projects)


def show_by_priority(all_tasks, _):
    important_tasks = []
    regular_tasks = []

    for task in all_tasks:
        if task["highPriority"]:
            important_tasks.append(task)
        else:
            regular_tasks.append(task)

    context = "priority"

    print()
    headline = format_headline("High Priority Tasks")
    print(headline)
    print(format_task_block(context, important_tasks))

    headline = format_headline("Regular Tasks")
    print(headline)
    print(format_task_block(context, regular_tasks))


def show_by_location(all_tasks, _):
    location_tasks = defaultdict(list)

    for task in all_tasks:
        location_tasks[task["location"]].append(task)

    context = "location"
    print()
    for location, tasks in location_tasks.items():
        if location:
            headline = format_headline(location)
            print(headline)
            print(format_task_block(context, tasks, print_location=False))

    headline = format_headline("No location specified")
    print(headline)
    print(format_task_block(context, location_tasks[""], print_location=False))


def show_by_project(tasks, projects):
    context = "project"

    tasks_by_project = defaultdict(list)
    for task in tasks:
        if task["project"]:
            task_project = task["project"]["id"]
        else:
            task_project = ""
        tasks_by_project[task_project].append(task)

    print()
    for project in projects:
        tasks = tasks_by_project[project["id"]] if project["id"] in tasks_by_project else []
        headline = format_headline(project["title"])
        headline_app = format_string("#" + project["shortcode"], color=project["color"], bold=True)
        print(format_headline(headline, headline_app))
        print(format_task_block(context, tasks, print_project=False))

    if '' in tasks_by_project:
        headline = format_string("No Project", underlined=True, bold=True, dim=True)
        print(headline)
        print(format_task_block(context, tasks_by_project[''], print_project=False))


def show_backlog(tasks, _):
    tasks = list(filter(lambda x: not (x["date"] or x["week"]), tasks))

    context = "backlog"
    headline = format_headline("Backlog")

    print()
    print(headline)
    print(format_task_block(context, tasks, print_date=True, print_project=True, print_location=True))


def show_by_due_date(all_tasks, _):
    this_week = Week.thisweek()
    next_week = Week.thisweek() + 1

    unscheduled_tasks = []
    overdue_tasks = []
    tasks_this_week = []
    tasks_next_week = []
    future_tasks = defaultdict(list)

    for task in all_tasks:
        if not task["week"]:
            unscheduled_tasks.append(task)
        elif task["week"] < str(this_week):
            overdue_tasks.append(task)
        elif task["week"] == str(this_week):
            tasks_this_week.append(task)
        elif task["week"] == str(next_week):
            tasks_next_week.append(task)
        else:
            future_tasks[task["week"]].append(task)

    context = "timeframe"
    print()

    if overdue_tasks:
        headline = format_headline("!!! Overdue !!!", color="red")
        print(headline)
        print(format_task_block(context, overdue_tasks, print_date=True))

    headline = format_headline("This Week", "Week " + str(this_week.week))
    print(headline)
    print(format_task_block(context, tasks_this_week))

    headline = format_headline("Next Week", "Week " + str(next_week.week) + ", " + next_week.monday().isoformat() + "+")
    print(headline)
    print(format_task_block(context, tasks_next_week))

    for week, tasks in future_tasks.items():
        week = Week.fromstring(week)
        headline = format_headline("Week " + str(week.week), week.monday().isoformat() + "+")
        print(headline)
        print(format_task_block(context, tasks,))

    headline = format_headline("Backlog")
    print(headline)
    print(format_task_block(context, unscheduled_tasks))


def show_default(all_tasks, _):
    today = date.today()
    tomorrow = today + timedelta(days=1)
    this_week = Week.thisweek()
    next_week = this_week+1

    tasks_overdue = []
    tasks_today = []
    tasks_tomorrow = []
    tasks_this_week = []
    tasks_next_week = []

    for task in all_tasks:
        if task["date"] < today.isoformat() and task["date"]:
            tasks_overdue.append(task)
        elif task["date"] == today.isoformat():
            tasks_today.append(task)
        elif task["date"] == tomorrow.isoformat():
            tasks_tomorrow.append(task)
        elif task["week"] < str(this_week) and task["week"]:
            tasks_overdue.append(task)
        elif task["week"] == str(this_week):
            tasks_this_week.append(task)
        elif task["week"] == str(next_week):
            tasks_next_week.append(task)


    is_today_sunday = today == this_week.sunday()
    if is_today_sunday:
        tasks_today.extend(tasks_this_week)

    print()

    context = "timeframe"
    if tasks_overdue:
        headline = format_headline("!!! Overdue !!!", color="red")
        print(headline)
        print(format_task_block(context, tasks_overdue))

    headline = format_headline("Today", _headline_date_string(today))
    print(headline)
    print(format_task_block(context, tasks_today, print_date=False))

    headline = format_headline("Tomorrow", _headline_date_string(tomorrow))
    print(headline)
    print(format_task_block(context, tasks_tomorrow, print_date=False))

    if not is_today_sunday:
        headline = format_headline("This Week", "Week " + str(this_week.week))
        print(headline)
        print(format_task_block(context, tasks_this_week))

    headline = format_headline("Next Week", "Week " + str(next_week.week) + ", " + next_week.monday().isoformat() + "+")
    print(headline)
    print(format_task_block(context, tasks_next_week))


def _headline_date_string(date_string):
    weekday = calendar.day_abbr[date_string.weekday()]
    day = str(date_string.day)
    month = calendar.month_abbr[date_string.month]
    year = str(date_string.year)

    return weekday + ", " + day + " " + month + " " + year


def _presort_data(hide_completed_tasks=True, hide_past_completed_tasks=True, hide_inactive_projects=True):
    tasks = load_tasks()
    projects = load_projects()

    # remove all done tasks
    if hide_completed_tasks:
        tasks = list(filter(lambda x: not x["isDone"], tasks))

    # remove past done tasks
    if hide_past_completed_tasks:
        tasks = list(filter(lambda x: not (x["isDone"] and (is_past_date(x["date"]) or is_past_week(x["week"]))), tasks))

    # remove tasks from inactive projects
    if hide_inactive_projects:
        inactive_project_ids = [project["id"] for project in projects if not project["active"]]
        projects = list(filter(lambda x: x["active"], projects))
        tasks = list(filter(lambda x: x["project"] not in inactive_project_ids, tasks))

    # sort by date
    has_date = []
    no_date = []
    for task in tasks:
        if task["date"]:
            has_date.append(task)
        else:
            no_date.append(task)
    tasks = sorted(has_date, key=lambda k: k["date"])
    tasks.extend(no_date)

    # sort by week
    has_week = []
    no_week = []
    for task in tasks:
        if task["week"]:
            has_week.append(task)
        else:
            no_week.append(task)
    tasks = sorted(has_week, key=lambda k: k["week"])
    tasks.extend(no_week)

    # sort by prio
    tasks = sorted(tasks, key=lambda k: k["highPriority"], reverse=True)


    #assign projects
    for task in tasks:
        if task["project"]:
            task["project"] = list(filter(lambda x: x["id"] == task["project"], projects))[0]

    return tasks, projects
