import unittest
from unittest.mock import patch
import io
import copy
from freezegun import freeze_time

from todoster import show


class MockArgs:  #pylint: disable=R0903
    sorting_by = ""
    show_completed_tasks = False
    show_past_tasks = False
    show_all_projects = False

class TestTask(unittest.TestCase):
    task_prio_date_loc = {"id": 1,
            "title": "high prio one, date, location",
            "date": "2018-09-02",
            "week": "2018W35",
            "location": "somewhere",
            "project": "",
            "highPriority": True,
            "isDone": False}
    task_prio_week_noloc = {"id": 2,
            "title": "high prio two, week, no location",
            "date": "",
            "week": "2018W36",
            "location": "",
            "project": "",
            "highPriority": True,
            "isDone": False}
    task_done_and_past = {"id": 3,
            "title": "done and past",
            "date": "",
            "week": "2018W05",
            "location": "",
            "project": "",
            "highPriority": False,
            "isDone": True}
    task_done_and_future = {"id": 4,
            "title": "done and future",
            "date": "",
            "week": "2019W35",
            "location": "",
            "project": "",
            "highPriority": False,
            "isDone": True}
    task_proj_active_date_overdue = {"id": 5,
            "title": "active project, date overdue",
            "date": "2018-08-31",
            "week": "2018W35",
            "location": "",
            "project": 1,
            "highPriority": False,
            "isDone": False}
    task_proj_inactive = {"id": 6,
            "title": "inactive project",
            "date": "",
            "week": "",
            "location": "",
            "project": 2,
            "highPriority": False,
            "isDone": False}
    task_noproj_week_overdue = {"id": 7,
            "title": "no project, week overdue",
            "date": "",
            "week": "2018W30",
            "location": "",
            "project": "",
            "highPriority": False,
            "isDone": False}
    task_nothing = {"id": 8,
            "title": "nothing",
            "date": "",
            "week": "",
            "location": "",
            "project": "",
            "highPriority": False,
            "isDone": False}
    test_tasks = [task_prio_date_loc, task_prio_week_noloc, task_done_and_past, task_done_and_future, task_proj_active_date_overdue, task_proj_inactive, task_noproj_week_overdue, task_nothing]

    project_active = {
        "id": 1,
        "title": "Active Project",
        "shortcode": "active",
        "color": "blue",
        "active": True}
    project_inactive = {
        "id": 2,
        "title": "Inactive Project",
        "shortcode": "inactive",
        "color": "blue",
        "active": False}
    project_no_tasks = {
        "id": 3,
        "title": "No Task Project",
        "shortcode": "no-task",
        "color": "blue",
        "active": True}
    test_projects = [project_active, project_inactive, project_no_tasks]


    def setUp(self):
        self.mock_args = MockArgs()
        self.mock_args.sorting_by = ""
        self.mock_args.show_completed_tasks = False
        self.mock_args.show_past_tasks = False
        self.mock_args.show_all_projects = False

    def tearDown(self):
        pass

    @freeze_time("2018-09-02")
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('todoster.show.load_projects')
    @patch('todoster.show.load_tasks')
    def test_show_sorted_by_priority(self, mock_tasks, mock_projects, mock_out):
        mock_tasks.return_value = copy.deepcopy(self.test_tasks)
        mock_projects.return_value = copy.deepcopy(self.test_projects)
        self.mock_args.sorting_by = "priority"

        show.show(self.mock_args)
        printout = mock_out.getvalue().split("\n\n")
        self.assertEqual(len(printout), 3) # last one is empty

        self.assertNotEqual(printout[0].find("high prio one"), -1)
        self.assertNotEqual(printout[0].find("high prio two"), -1)
        high_prio = printout[0].split("\n")
        self.assertEqual(len(high_prio), 4) # empty line, header, two tasks

        normal_prio = printout[1].split("\n")
        self.assertEqual(len(normal_prio), 5) # empty line, header, 3 tasks (no done and inactive proj)

    @freeze_time("2018-09-02")
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('todoster.show.load_projects')
    @patch('todoster.show.load_tasks')
    def test_show_done_tasks(self, mock_tasks, mock_projects, mock_out):
        mock_tasks.return_value = copy.deepcopy(self.test_tasks)
        mock_projects.return_value = copy.deepcopy(self.test_projects)
        self.mock_args.sorting_by = "priority"
        self.mock_args.show_completed_tasks = True

        show.show(self.mock_args)
        printout = mock_out.getvalue().split("\n\n")
        self.assertEqual(len(printout), 3)

        normal_prio = printout[1].split("\n")
        self.assertEqual(len(normal_prio), 6) # empty line, header, 4 tasks (no past done and inactive proj)
        self.assertNotEqual(printout[1].find('done and future'), -1)

    @freeze_time("2018-09-02")
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('todoster.show.load_projects')
    @patch('todoster.show.load_tasks')
    def test_show_past_done_tasks(self, mock_tasks, mock_projects, mock_out):
        mock_tasks.return_value = copy.deepcopy(self.test_tasks)
        mock_projects.return_value = copy.deepcopy(self.test_projects)
        self.mock_args.sorting_by = "priority"
        self.mock_args.show_completed_tasks = True
        self.mock_args.show_past_tasks = True

        show.show(self.mock_args)
        printout = mock_out.getvalue().split("\n\n")
        self.assertEqual(len(printout), 3)

        normal_prio = printout[1].split("\n")
        self.assertEqual(len(normal_prio), 7) # empty line, header, 5 tasks (no inactive proj)
        self.assertNotEqual(printout[1].find('done and past'), -1)

    @freeze_time("2018-09-02")
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('todoster.show.load_projects')
    @patch('todoster.show.load_tasks')
    def test_show_tasks_from_inactive_projects(self, mock_tasks, mock_projects, mock_out):
        mock_tasks.return_value = copy.deepcopy(self.test_tasks)
        mock_projects.return_value = copy.deepcopy(self.test_projects)
        self.mock_args.sorting_by = "priority"
        self.mock_args.show_all_projects = True

        show.show(self.mock_args)
        printout = mock_out.getvalue().split("\n\n")
        self.assertEqual(len(printout), 3)

        normal_prio = printout[1].split("\n")
        self.assertEqual(len(normal_prio), 6) # empty line, header, 5 tasks (no done)
        self.assertNotEqual(printout[1].find('inactive project'), -1)

    @freeze_time("2018-09-01")
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('todoster.show.load_projects')
    @patch('todoster.show.load_tasks')
    def test_show_sorted_by_default(self, mock_tasks, mock_projects, mock_out):
        mock_tasks.return_value = copy.deepcopy(self.test_tasks)
        mock_projects.return_value = copy.deepcopy(self.test_projects)
        self.mock_args.sorting_by = ""

        show.show(self.mock_args)
        printout = mock_out.getvalue().split("\n\n")
        self.assertEqual(len(printout), 6)
        self.assertNotEqual(printout[0].find("!!! Overdue !!!"), -1)
        self.assertNotEqual(printout[1].find("Today"), -1)
        self.assertNotEqual(printout[2].find("Tomorrow"), -1)
        self.assertNotEqual(printout[3].find("This Week"), -1)
        self.assertNotEqual(printout[4].find("Next Week"), -1)

        overdue = printout[0].split("\n")
        self.assertEqual(len(overdue), 4) # empty line, header, 2 tasks
        self.assertNotEqual(overdue[2].find('week overdue'), -1)
        self.assertNotEqual(overdue[3].find('date overdue'), -1)

        today = printout[1].split("\n")
        self.assertEqual(len(today), 3) # empty line, header, no task
        self.assertNotEqual(today[1].find("Sat, 1 Sep 2018"), -1)
        self.assertNotEqual(today[2].find("--- No tasks for this timeframe ---"), -1)

        tomorrow = printout[2].split("\n")
        self.assertEqual(len(tomorrow), 3) # empty line, header, one task
        self.assertNotEqual(tomorrow[1].find("Sun, 2 Sep 2018"), -1)
        self.assertNotEqual(tomorrow[2].find("high prio one, date, location"), -1)

        this_week = printout[3].split("\n")
        self.assertEqual(len(this_week), 3) # empty line, header, no task
        self.assertNotEqual(this_week[1].find("Week 35"), -1)
        self.assertNotEqual(this_week[2].find("--- No tasks for this timeframe ---"), -1)

        next_week = printout[4].split("\n")
        self.assertEqual(len(next_week), 3) # empty line, header, one task
        self.assertNotEqual(next_week[1].find("Week 36, 2018-09-03+"), -1)
        self.assertNotEqual(next_week[2].find("high prio two, week, no location"), -1)

    @freeze_time("2018-09-02")
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('todoster.show.load_projects')
    @patch('todoster.show.load_tasks')
    def test_show_sorted_by_default_today_is_sunday(self, mock_tasks, mock_projects, mock_out):
        mock_tasks.return_value = copy.deepcopy(self.test_tasks)
        mock_projects.return_value = copy.deepcopy(self.test_projects)
        self.mock_args.sorting_by = ""

        show.show(self.mock_args)
        printout = mock_out.getvalue().split("\n\n")
        self.assertEqual(len(printout), 5)
        self.assertNotEqual(printout[0].find("!!! Overdue !!!"), -1)
        self.assertNotEqual(printout[1].find("Today"), -1)
        self.assertNotEqual(printout[2].find("Tomorrow"), -1)
        self.assertNotEqual(printout[3].find("Next Week"), -1)

    @freeze_time("2018-09-01")
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('todoster.show.load_projects')
    @patch('todoster.show.load_tasks')
    def test_show_sorted_by_location(self, mock_tasks, mock_projects, mock_out):
        mock_tasks.return_value = copy.deepcopy(self.test_tasks)
        mock_projects.return_value = copy.deepcopy(self.test_projects)
        self.mock_args.sorting_by = "location"

        show.show(self.mock_args)

        printout = mock_out.getvalue().split("\n\n")
        self.assertEqual(len(printout), 3) # 1 location, 1 no location, 1 empty line
        self.assertNotEqual(printout[0].find("somewhere"), -1)
        self.assertNotEqual(printout[1].find("No location specified"), -1)

        location = printout[0].split("\n")
        self.assertEqual(len(location), 3) # empty line, header, 1 task
        self.assertNotEqual(location[2].find('location'), -1)

        no_location = printout[1].split("\n")
        self.assertEqual(len(no_location), 6) # empty line, header, 4 tasks

    @freeze_time("2018-09-01")
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('todoster.show.load_projects')
    @patch('todoster.show.load_tasks')
    def test_show_sorted_by_project(self, mock_tasks, mock_projects, mock_out):
        mock_tasks.return_value = copy.deepcopy(self.test_tasks)
        mock_projects.return_value = copy.deepcopy(self.test_projects)
        self.mock_args.sorting_by = "project"

        show.show(self.mock_args)
        printout = mock_out.getvalue().split("\n\n")
        self.assertEqual(len(printout), 4)
        self.assertNotEqual(printout[0].find("Active"), -1)
        self.assertNotEqual(printout[1].find("No Task"), -1)
        self.assertNotEqual(printout[2].find("No Project"), -1)

        active_proj = printout[0].split("\n")
        self.assertEqual(len(active_proj), 3) # empty line, header, 1 task
        self.assertNotEqual(active_proj[2].find('active project, date overdue'), -1)

        empty_proj = printout[1].split("\n")
        self.assertEqual(len(empty_proj), 3) # empty line, header, no task
        self.assertNotEqual(empty_proj[2].find("--- No tasks for this project ---"), -1)

        no_proj = printout[2].split("\n")
        self.assertEqual(len(no_proj), 6) # empty line, header, 4 tasks

    @freeze_time("2018-09-01")
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('todoster.show.load_projects')
    @patch('todoster.show.load_tasks')
    def test_show_sorted_by_project_with_inactive_project(self, mock_tasks, mock_projects, mock_out):
        mock_tasks.return_value = copy.deepcopy(self.test_tasks)
        mock_projects.return_value = copy.deepcopy(self.test_projects)
        self.mock_args.sorting_by = "project"
        self.mock_args.show_all_projects = True

        show.show(self.mock_args)
        printout = mock_out.getvalue().split("\n\n")
        self.assertEqual(len(printout), 5)
        self.assertNotEqual(printout[0].find("Active"), -1)
        self.assertNotEqual(printout[1].find("Inactive"), -1)
        self.assertNotEqual(printout[2].find("No Task"), -1)
        self.assertNotEqual(printout[3].find("No Project"), -1)

        inactive_proj = printout[1].split("\n")
        self.assertEqual(len(inactive_proj), 3) # empty line, header, 1 task
        self.assertNotEqual(inactive_proj[2].find("inactive project"), -1)


    @freeze_time("2018-09-01")
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('todoster.show.load_projects')
    @patch('todoster.show.load_tasks')
    def test_show_only_backlog(self, mock_tasks, mock_projects, mock_out):
        mock_tasks.return_value = copy.deepcopy(self.test_tasks)
        mock_projects.return_value = copy.deepcopy(self.test_projects)
        self.mock_args.sorting_by = "backlog"

        show.show(self.mock_args)
        printout = mock_out.getvalue().split("\n\n")
        self.assertEqual(len(printout), 2)
        self.assertNotEqual(printout[0].find("Backlog"), -1)

        backlog = printout[0].split("\n")
        self.assertEqual(len(backlog), 3) # empty line, header, 1 tasks


    @freeze_time("2018-09-01")
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('todoster.show.load_projects')
    @patch('todoster.show.load_tasks')
    def test_show_sorted_by_due_date(self, mock_tasks, mock_projects, mock_out):
        mock_tasks.return_value = copy.deepcopy(self.test_tasks)
        mock_projects.return_value = copy.deepcopy(self.test_projects)
        self.mock_args.sorting_by = "date"

        show.show(self.mock_args)
        printout = mock_out.getvalue().split("\n\n")
        self.assertEqual(len(printout), 5)
        self.assertNotEqual(printout[0].find("!!! Overdue !!"), -1)
        self.assertNotEqual(printout[1].find("This Week"), -1)
        self.assertNotEqual(printout[2].find("Next Week"), -1)
        self.assertNotEqual(printout[3].find("Backlog"), -1)
