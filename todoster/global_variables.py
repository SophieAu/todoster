import os

TODOSTER_DIR = os.getenv("TODOSTER_DIR", os.getenv("HOME") + "/.todoster")

VERSION = "1.0.0"


BASE_HELP = """A simple command line task manager

\033[1mUSAGE\033[0m
    $ todoster [COMMAND]

\033[1mCOMMANDS\033[0m
    None        display default todo list
    task, t     manage tasks
    project, p  manage projects
    show, s     display todo lists
"""

TASK_HELP = """Manage your tasks

\033[1mUSAGE\033[0m
    $ todoster task [COMMAND]

\033[1mCOMMANDS\033[0m
    add          add a task
    edit [ID]    edit a task
    check [ID]   mark a task as completed/not completed
    delete [ID]  delete a task

\033[1mARGUMENTS\033[0m
    ID  id of the task

\033[1mOPTIONS\033[0m (add and edit only)
    -t/--title [TITLE]        set title
    -d/--date [DATE]          set due date
    -p/--project [SHORTCODE]  set project
    -l/--location [LOCATION]  set location
    -i/--important            mark task as important
    \033[1mnote:\033[0m setting an option to "\d" removes that value

\033[1mEXAMPLES\033[0m
    $ todoster task add -t "new task" -d 10.12.2018 -l "Office"
    $ todoster task edit 23 -d 15.12.2018
    $ todoster task edit 23 -i
    $ todoster task check 23
    $ todoster task delete 23
"""

PROJECT_HELP = """Manage your projects

\033[1mUSAGE\033[0m
    todoster project [COMMAND]

\033[1mCOMMANDS\033[0m
    l, list [-a/--all]      list projects (incl. archived if -a flag is set)
    a, add                  create project
    e, edit [SHORTCODE]     edit project
    c, archive [SHORTCODE]  archive project
    d, delete [SHORTCODE]   delete project and all associated tasks

\033[1mARGUMENTS\033[0m
    SHORTCODE  shortcode of the project

\033[1mOPTIONS\033[0m (add and edit only)
    -t/--title [TITLE]          set title
    -s/--shortcode [SHORTCODE]  set shortcode
    -c/--color [COLOR]          set color

\033[1mVALID COLOR VALUES\033[0m
    \033[39mdefault\033[0m
    \033[30mgrey\033[0m
    \033[31mred\033[0m
    \033[32mgreen\033[0m
    \033[33myellow\033[0m
    \033[34mblue\033[0m
    \033[35mpurple\033[0m
    \033[36mcyan\033[0m
    \033[97mwhite\033[0m

\033[1mEXAMPLES\033[0m
    $ todoster project add -t "React Website Tutorial" -s react-tute -c green
    $ todoster project edit react-tute -c purple
    $ todoster project archive react-tute
    $ todoster project delete react-tute
    $ todoster project list -a
"""

SHOW_HELP = """Display your tasks

\033[1mUSAGE\033[0m
    todoster show [COMMAND]

\033[1mCOMMANDS\033[0m
    current   show tasks due in this or the next week
    backlog   show tasks without a due date
    date      show tasks grouped by week
    location  show tasks grouped by location
    priority  show tasks grouped by priority
    project   show tasks grouped by project

\033[1mOPTIONS\033[0m
    -a, --all      show tasks belonging to archived projects
    -c, --checked  show checked tasks with no due date or a due date in the future
    -p, --past     show checked tasks with a due date in the past (only works in combination with -c)
"""
