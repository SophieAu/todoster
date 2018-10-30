import argparse
import os

from todoster.project import add_project, delete_project, edit_project, archive_project
from todoster.list_projects import list_projects
from todoster.task import add_task, edit_task, check_task, delete_task
from todoster.show import show

from todoster.global_variables import BASE_HELP, TASK_HELP, PROJECT_HELP, SHOW_HELP, TODOSTER_DIR


def add_task_parser(subparsers):
    parser = subparsers.add_parser('add', aliases=["a"], allow_abbrev=True)
    parser.add_argument('title',
                        help="title of the task")
    parser.add_argument("-d", "--date",
                        dest="date",
                        help="set a due date or week for the task",
                        metavar="DATE")
    parser.add_argument("-l", "--location",
                        dest="location",
                        help="assign a location to the task",
                        metavar="LOC")
    parser.add_argument("-p", "--project",
                        dest="project",
                        help="assign project shortcode to task",
                        default="",
                        metavar="PROJ")
    parser.add_argument("-i", "--important",
                        action='store_true',
                        dest="highPriority",
                        help="mark the task as high priority")
    parser.set_defaults(func=add_task)


def edit_task_parser(subparsers):
    parser = subparsers.add_parser('edit', aliases=["e"], allow_abbrev=True)
    parser.add_argument('task_id',
                        type=int,
                        help="task_id of the task to be marked as completed")
    parser.add_argument("-t", "--title",
                        dest='title',
                        default=None,
                        help="change the title of the task",
                        metavar="TITLE")
    parser.add_argument("-d", "--date",
                        dest="date",
                        default=None,
                        help="set a due date or week for the task",
                        metavar="DATE")
    parser.add_argument("-l", "--location",
                        dest="location",
                        default=None,
                        help="assign a location to the task",
                        metavar="LOC")
    parser.add_argument("-p", "--project",
                        dest="project",
                        default=None,
                        help="assign project shortcode to task",
                        metavar="PROJ")
    parser.add_argument("-i", "--important",
                        dest="highPriority",
                        help="mark the task as high priority")
    parser.set_defaults(func=edit_task)


def list_projects_parser(subparsers):
    parser = subparsers.add_parser('list', aliases=["l"], allow_abbrev=True)
    parser.add_argument("-a", "--all",
                        action='store_true',
                        dest="show_all_projects",
                        default=False,
                        help="show active and inactive projects")
    parser.set_defaults(func=list_projects)


def check_task_parser(subparsers):
    parser = subparsers.add_parser('check', aliases=["c"], allow_abbrev=True)
    parser.add_argument('task_id',
                        type=int,
                        help="task_id of the task to be marked as (not) completed")
    parser.set_defaults(func=check_task)


def delete_task_parser(subparsers):
    parser = subparsers.add_parser('delete', aliases=["d"], allow_abbrev=True)
    parser.add_argument('task_id',
                        type=int,
                        help="task_id of the task to be deleted")
    parser.set_defaults(func=delete_task)


def add_project_parser(subparsers):
    parser = subparsers.add_parser('add', aliases=["a"], allow_abbrev=True)
    parser.add_argument('title',
                        help="title of the project")
    parser.add_argument("-s", "--shortcode",
                        dest="shortcode",
                        help="define the shortcode for the project",
                        metavar="SHORTCODE")
    parser.add_argument("-c", "--color",
                        dest="color",
                        help="assign a color to the project",
                        default="default",
                        metavar="COLOR")
    parser.add_argument("-d", "--deactivate",
                        action='store_false',
                        dest="isActive",
                        default=True,
                        help="mark the project as inactive")
    parser.set_defaults(func=add_project)


def archive_project_parser(subparsers):
    parser = subparsers.add_parser('archive', aliases=["c"], allow_abbrev=True)
    parser.add_argument('shortcode',
                        help="shortcode of the project")
    parser.set_defaults(func=archive_project)


def edit_project_parser(subparsers):
    parser = subparsers.add_parser('edit', aliases=["e"], allow_abbrev=True)
    parser.add_argument('shortcode',
                        help="current shortcode of the project")
    parser.add_argument("-t", "--title",
                        dest="title",
                        help="change the title the project",
                        metavar="TITLE")
    parser.add_argument("-s", "--shortcode",
                        dest="new_shortcode",
                        help="change the shortcode for the project",
                        metavar="SHORTCODE")
    parser.add_argument("-c", "--color",
                        dest="color",
                        help="assign a color to the project",
                        metavar="COLOR")
    parser.set_defaults(func=edit_project)


def delete_project_parser(subparsers):
    parser = subparsers.add_parser('delete', aliases=["d"], allow_abbrev=True)
    parser.add_argument('shortcode',
                        help="shortcode of the project")
    parser.set_defaults(func=delete_project)


def show_parser(parser):
    parser.add_argument(choices=['p', 'project', 'd', 'date', 'l', 'location', 'i', 'priority', 'b', 'backlog'],
                        nargs='?',
                        dest="sorting_by")
    parser.add_argument("-a", "--all",
                        action='store_true',
                        dest="show_all_projects",
                        default=False,
                        help="show tasks belonging to both active and inactive projects")
    parser.add_argument("-c", "--completed",
                        action='store_true',
                        dest="show_completed_tasks",
                        default=False,
                        help="show completed tasks with no due date or a due date in the future")
    parser.add_argument("-p", "--past",
                        action='store_true',
                        dest="show_past_tasks",
                        default=False,
                        help="show completed tasks with a due date in the past (only works with -c/--completed enabled)")
    parser.set_defaults(func=show)


def ensure_path():
    if not os.access(TODOSTER_DIR + "/tasks", os.R_OK):
        os.makedirs(TODOSTER_DIR + "/tasks")


def main():
    ensure_path()

    parser = argparse.ArgumentParser()
    parser.set_defaults(func=show)
    subparsers = parser.add_subparsers()

    task_parsers = subparsers.add_parser('task', aliases=["t"], allow_abbrev=True).add_subparsers()
    add_task_parser(task_parsers)
    edit_task_parser(task_parsers)
    check_task_parser(task_parsers)
    delete_task_parser(task_parsers)

    project_parsers = subparsers.add_parser('project', aliases=["p"], allow_abbrev=True).add_subparsers()
    list_projects_parser(project_parsers)
    add_project_parser(project_parsers)
    edit_project_parser(project_parsers)
    archive_project_parser(project_parsers)
    delete_project_parser(project_parsers)

    show_parser(subparsers.add_parser('show', aliases=["s"], allow_abbrev=True))

    args = parser.parse_args()
    args.func(args)
    exit(0)


main()
