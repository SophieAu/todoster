import sys

from todoster.file_operations import save_project, load_project_by_shortcode, load_tasks, remove_task, remove_project
from todoster.output_formatter import format_project, format_task

PROJECT_COLORS = ["default", "grey", "red", "green", "yellow", "blue", "purple", "cyan", "white"]

def add_project(args):
    project = {}
    project["id"] = ""
    project["title"] = args.title
    project["shortcode"] = args.shortcode or project["title"].lower().replace(" ", "-")
    project["color"] = _parse_color(args.color) or "default"
    project["active"] = args.isActive

    save_project(project)
    print("You created project " + format_project(project) + ".")


def edit_project(args):
    project = load_project_by_shortcode(args.shortcode)

    project["title"] = _parse_title(args.title) or project["title"]
    project["shortcode"] = _parse_shortcode(args.new_shortcode) or project["shortcode"]
    project["color"] = _parse_color(args.color) or project["color"]

    save_project(project)
    print("You edited project " + format_project(project) + ".")


def archive_project(args):
    project = load_project_by_shortcode(args.shortcode)

    project["active"] = not project["active"]

    save_project(project)
    print("Project '" + project["title"] + "' has been marked as " + ("active" if project["active"] else "archived") + ".")


def delete_project(args):
    project_to_delete = load_project_by_shortcode(args.shortcode)

    print("You've selected project " + format_project(project_to_delete) + " for deletion.")

    tasks_to_delete = _get_deletable_tasks(project_to_delete)
    if tasks_to_delete:
        print("This will also delete the following tasks which are attached to the project:")
        for task in tasks_to_delete:
            print(format_task(task))

    print("\nAre you sure? [y/n]")
    confirmation = input()
    if confirmation in ["y", "Y", "yes"]:
        for task in tasks_to_delete:
            remove_task(task)
        remove_project(project_to_delete)
        print("The project " + ("and all attached tasks were" if tasks_to_delete else "was") + " successfully deleted.")
        return

    print("Nothing was deleted.")


def _parse_title(new_title):
    if new_title == "\\d":
        print("The title of a project cannot be empty. This entry will not be saved.", file=sys.stderr)
        return ""

    return new_title


def _parse_shortcode(new_shortcode):
    if new_shortcode == "\\d":
        print("The shortcode of a project cannot be empty. This entry will not be saved.", file=sys.stderr)
        return ""

    return new_shortcode


def _parse_color(new_color):
    if new_color == "":
        return "default"

    if new_color and new_color not in PROJECT_COLORS:
        print("This is not a valid color. This entry will not be saved.", file=sys.stderr)
        return ""

    return new_color


def _get_deletable_tasks(project):
    filtered_tasks = []

    for task in load_tasks():
        if task["project"] == project["id"]:
            task["project"] = project
            filtered_tasks.append(task)

    return filtered_tasks
