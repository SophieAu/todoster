from todoster.file_operations import load_projects
from todoster.output_formatter import format_string

def list_projects(arguments):
    projects = load_projects()

    if not arguments.show_all_projects:
        projects = list(filter(lambda x: x["active"], projects))

    print()
    project_counter = 1
    for project in projects:
        counter = format_string(str(project_counter).rjust(3), dim=True)
        title = format_string(project["title"], dim=(not project["active"]))
        shortcode = format_string("#" + project["shortcode"], color=project["color"])
        print(counter + " " + title + " (" + shortcode + ")")
        project_counter += 1

    print()
