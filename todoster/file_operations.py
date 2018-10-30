import json
import io
import os
import re
import copy
import sys

from todoster.global_variables import TODOSTER_DIR

PROJECT_FILE = TODOSTER_DIR + "/projects.json"
TASK_DIR = TODOSTER_DIR + "/tasks/"


def load_project(project_id):
    projects = load_projects()
    for project in projects:
        if project["id"] == project_id:
            return project

    return {}


def load_project_by_shortcode(shortcode):
    projects = load_projects()
    try:
        for project in projects:
            if project["shortcode"] == shortcode:
                return project
        raise FileNotFoundError
    except FileNotFoundError:
        print('The project does not exist.', file=sys.stderr)
        exit(1)


def load_projects():
    try:
        return json.loads(io.open(PROJECT_FILE).read())
    except FileNotFoundError:
        return []


def save_project(project):
    all_projects = load_projects()

    if not project["id"]:
        project["id"] = 1 if not all_projects else all_projects[len(all_projects) - 1]["id"] + 1
        all_projects.append(project)
    else:
        for old_project in all_projects:
            if old_project["id"] == project["id"]:
                old_project["title"] = project["title"]
                old_project["shortcode"] = project["shortcode"]
                old_project["color"] = project["color"]
                old_project["active"] = project["active"]

    _save_projects(all_projects)


def remove_project(project):
    all_projects = load_projects()
    all_projects = list(filter(lambda x: x["id"] != project["id"], all_projects))

    _save_projects(all_projects)


def load_tasks():
    task_dir = TODOSTER_DIR + "/tasks/"
    all_task_files = _load_task_list()
    all_tasks = []

    for task_file in all_task_files:
        try:
            if not re.compile('^\d+.json$').match(task_file):
                continue
            all_tasks.append(json.loads(io.open(task_dir + task_file).read()))
        except FileNotFoundError:
            print("Couldn't open task " + task_file + ".", file=sys.stderr)
        except UnicodeDecodeError:
            print("Error parsing  " + task_file + ".", file=sys.stderr)

    return all_tasks


def load_task(task_id):
    task_dir = TODOSTER_DIR + "/tasks/"
    try:
        return json.loads(io.open(task_dir + task_id + ".json").read())
    except FileNotFoundError:
        print("Could not find task with the id " + task_id + ".", file=sys.stderr)
        exit(1)


def save_task(task):
    task = copy.copy(task)
    if not task["id"]:
        task_list = _load_task_list()
        if task_list:
            task["id"] = max([int(task_file.rstrip(".json")) for task_file in task_list if task_file.rstrip(".json").isdigit()]) + 1
        else:
            task["id"] = 1

    if not isinstance(task["project"], int) and task["project"]:
        task["project"] = task["project"]["id"]

    json_string = json.dumps(task, indent=4)
    file = open(TASK_DIR + str(task["id"]) + ".json", "w")
    file.write(json_string)

    return task["id"]


def remove_task(task):
    os.remove(TASK_DIR + str(task["id"]) + ".json")


def _load_task_list():
    try:
        return os.listdir(TASK_DIR)
    except FileNotFoundError:
        os.mkdir(TASK_DIR)
        return []


def _save_projects(projects):
    json_string = json.dumps(projects, indent=4)
    file = open(PROJECT_FILE, "w")
    file.write(json_string)
