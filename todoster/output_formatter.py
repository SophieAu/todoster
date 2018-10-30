def format_string(input_string, color="", bold=False, underlined=False, dim=False):
    reset = "\033[0m"
    return _format(color=color, bold=bold, underlined=underlined, dim=dim) + input_string + reset


def format_headline(base, appendix="", color="default"):
    base = _base_headline(base, color=color)
    if appendix:
        appendix = _headline_appendix(appendix)

    return base + appendix


def format_task_block(context, tasks, print_date=True, print_project=True, print_location=True):
    if not tasks:
        return format_string("   --- No tasks for this " + context + " ---", dim=True) + "\n\n"

    task_string = ""
    for task in tasks:
        if not print_date:
            task["date"] = ""
            task["week"] = ""

        if not print_project:
            task["project"] = ""

        if not print_location:
            task["location"] = ""

        task_string = task_string + format_task(task) + "\n"

    return task_string + "\n"


def format_task(task):
    importance = format_string("★", color="yellow") if task["highPriority"] else " "
    status = " " + (format_string("✓", color="green") if task["isDone"] else "☐")
    task_id = " " + format_string(str(task["id"]).rjust(3) + ".", dim=True)
    title = " " + format_string(task["title"], dim=task["isDone"])
    date = ""
    location = (" " + format_string("->" + task["location"], dim=task["isDone"]) if task["location"] else "")
    project = ""

    if task["date"] != "" or task["week"] != "":
        date_value = task["date"] if task["date"] else ("W" + task["week"][5:])
        date = " " + format_string("@" + date_value, bold=True, dim=task["isDone"])

    if task["project"]:
        proj = task["project"]
        project = " " + format_string("#" + proj["shortcode"], color=proj["color"], bold=True, dim=task["isDone"])

    return importance + status + task_id + title + date + location + project


def format_project(project):
    return "\"" + project["title"] + "\" (" + format_string("#" + project["shortcode"], color=project["color"]) + ")"


def _base_headline(headline_text, color="default"):
    return format_string(headline_text, color=color, underlined=True, bold=True)

def _headline_appendix(date_string):
    return format_string(" (" + date_string + ")", underlined=True)

def _format(color="", bold=False, underlined=False, dim=False):
    color_codes = {"default": "39", "black": "29", "grey": "30", "red": "31", "green": "32", "yellow": "33", "blue": "34", "purple": "35", "cyan": "36", "white": "97"}

    color_string = "\033[" + color_codes[color] + "m" if color else ""
    bold_string = "\033[1m" if bold else ""
    underline_string = "\033[4m" if underlined else ""
    dim_string = "\033[2m" if dim else ""

    return bold_string + underline_string + dim_string + color_string
