import sys

from todoster.file_operations import save_task, load_project_by_shortcode, load_task, remove_task, load_project
from todoster.output_formatter import format_task, format_string
from todoster.date_handler import is_valid_date_format, is_valid_week_format, get_week_from_date, format_date, format_week

def add_task(args):
    if not args.title:
        print("You cannot create an empty task.", file=sys.stderr)
        return

    task = {}
    task["id"] = ""
    task["title"] = args.title
    task["location"] = args.location
    task["project"] = _parse_project(args.project) or ""
    task["highPriority"] = args.highPriority
    task["isDone"] = False
    parsed_date = _parse_date(args.date)
    task["date"] = parsed_date[0] or ""
    task["week"] = parsed_date[1] or ""

    task["id"] = save_task(task)
    print("You've created the following task:")
    print(format_task(task))


def edit_task(args):
    task = load_task(str(args.task_id))

    task_changes = {}
    task_changes["title"] = _parse_title(args.title)
    task_changes["date"], task_changes["week"] = _parse_date(args.date)
    task_changes["location"] = args.location
    task_changes["project"] = _parse_project(args.project)
    if args.highPriority:
        task["highPriority"] = not task["highPriority"]

    for key, value in task_changes.items():
        if not value is None:
            task[key] = value

    if isinstance(task["project"], int):
        task["project"] = load_project(task["project"])

    save_task(task)
    print("You've changed task " + str(args.task_id) + " to the following:")
    print(format_task(task))


def check_task(args):
    task = load_task(str(args.task_id))

    task["isDone"] = not task["isDone"]
    save_task(task)
    print("Task '" + task["title"] + "' has been marked as " + ("" if task["isDone"] else "not ") + "done.")


def delete_task(arguments):
    task = load_task(str(arguments.task_id))

    print("You are about to delete task " + format_string(str(task["id"]), dim=True) + ": '" + task["title"] + "'. Are you sure? [y/N]")
    confirmation = input()
    if confirmation in ["y", "Y", "yes"]:
        remove_task(task)
        print("Task deleted.")
        return

    print("Task not deleted.")


def _parse_title(new_title):
    if new_title == "":
        print("The title of a task cannot be empty. This entry will not be saved.", file=sys.stderr)
        return None

    return new_title


def _parse_date(new_date):
    if new_date is None:
        return None, None

    if not new_date:
        return "", ""

    if is_valid_date_format(new_date):
        try:
            new_date = format_date(new_date)
            return str(new_date), str(get_week_from_date(new_date))
        except BaseException:
            pass

    elif is_valid_week_format(new_date):
        try:
            return "", str(format_week(new_date))
        except BaseException:
            pass

    print("The date you entered (" + new_date + ") is invalid. Please follow ISO standards.", file=sys.stderr)
    return None, None


def _parse_project(new_project):
    if not new_project:
        return new_project

    return load_project_by_shortcode(new_project)
