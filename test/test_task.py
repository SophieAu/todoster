import unittest
import unittest.mock

import io

from  todoster import output_formatter
from  todoster import task

class MockArgs:  #pylint: disable=R0903
    task_id = ""
    title = ""
    date = ""
    week = ""
    location = ""
    project = None
    highPriority = False
    isDone = False
    uncheck = False


def _task_from_args(task_id, title, date, week, location, project, high_priority, is_done):  #pylint: disable=R0913
    return {
        "id": task_id,
        "title": title,
        "date": date,
        "week": week,
        "location": location,
        "project": project,
        "highPriority": high_priority,
        "isDone": is_done
    }


class TestTask(unittest.TestCase):
    mock_args = None

    def setUp(self):
        self.mock_args = MockArgs()
        self.mock_args.title = None
        self.mock_args.date = None
        self.mock_args.week = None
        self.mock_args.location = None
        self.mock_args.project = None
        self.mock_args.highPriority = None  #pylint: disable=C0103
        self.mock_args.isDone = False  #pylint: disable=C0103

    def tearDown(self):
        pass


    @unittest.mock.patch('sys.stderr', new_callable=io.StringIO)
    @unittest.mock.patch('todoster.task.save_task')
    def test_add_task_with_empty_title(self, saver_mock, mock_err):
        expected = "You cannot create an empty task.\n"

        task.add_task(self.mock_args)
        self.assertEqual(mock_err.getvalue(), expected)
        saver_mock.assert_not_called()


    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    @unittest.mock.patch('todoster.task.save_task')
    def test_add_task_with_title(self, saver_mock, mock_out):
        saver_mock.return_value = 3

        self.mock_args.title = "New Task"

        formatted_task = output_formatter.format_task(_task_from_args(3, "New Task", "", "", "", "", False, False))
        expected = "You've created the following task:\n" + formatted_task + "\n"

        task.add_task(self.mock_args)
        self.assertEqual(mock_out.getvalue(), expected)
        saver_mock.assert_called()


    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    @unittest.mock.patch('todoster.task.save_task')
    @unittest.mock.patch('todoster.task.load_task')
    def test_edit_task_add_new_date(self, loader_mock, saver_mock, mock_out):
        test_task = {
            "id": 1,
            "title": "design blog section",
            "date": "2018-09-02",
            "week": "2018W35",
            "location": "",
            "project": "",
            "highPriority": False,
            "isDone": True
        }
        self.mock_args.task_id = 1
        saver_mock.return_value = 1
        loader_mock.return_value = dict.copy(test_task)

        self.mock_args.date = "10.10.2018"
        expected_new_test_task = dict.copy(test_task)
        expected_new_test_task["date"] = "2018-10-10"

        formatted_task = output_formatter.format_task(expected_new_test_task)
        expected = "You've changed task 1 to the following:\n" + formatted_task + "\n"
        task.edit_task(self.mock_args)
        self.assertEqual(mock_out.getvalue(), expected)
        saver_mock.assert_called()


    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    @unittest.mock.patch('todoster.task.save_task')
    @unittest.mock.patch('todoster.task.load_task')
    def test_edit_tasks_delete_date(self, loader_mock, saver_mock, mock_out):
        test_task = {
            "id": 1,
            "title": "design blog section",
            "date": "2018-09-02",
            "week": "2018W35",
            "location": "",
            "project": "",
            "highPriority": False,
            "isDone": True
        }
        self.mock_args.task_id = 1
        saver_mock.return_value = 1
        loader_mock.return_value = dict.copy(test_task)
        self.mock_args.date = ""
        expected_new_test_task = dict.copy(test_task)
        expected_new_test_task["date"] = ""
        expected_new_test_task["week"] = ""

        formatted_task = output_formatter.format_task(expected_new_test_task)
        expected = "You've changed task 1 to the following:\n" + formatted_task + "\n"
        task.edit_task(self.mock_args)
        self.assertEqual(mock_out.getvalue(), expected)
        saver_mock.assert_called()


    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    @unittest.mock.patch('todoster.task.save_task')
    @unittest.mock.patch('todoster.task.load_task')
    def test_edit_tasks_add_new_week(self, loader_mock, saver_mock, mock_out):
        test_task = {
            "id": 1,
            "title": "design blog section",
            "date": "2018-09-02",
            "week": "2018W35",
            "location": "",
            "project": "",
            "highPriority": False,
            "isDone": True
        }
        self.mock_args.task_id = 1
        saver_mock.return_value = 1
        loader_mock.return_value = dict.copy(test_task)

        self.mock_args.date = "1998-w12"
        expected_new_test_task = dict.copy(test_task)
        expected_new_test_task["date"] = ""
        expected_new_test_task["week"] = "1998W12"

        formatted_task = output_formatter.format_task(expected_new_test_task)
        expected = "You've changed task 1 to the following:\n" + formatted_task + "\n"
        task.edit_task(self.mock_args)
        self.assertEqual(mock_out.getvalue(), expected)
        saver_mock.assert_called()


    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    @unittest.mock.patch('todoster.task.save_task')
    @unittest.mock.patch('todoster.task.load_task')
    def test_edit_task_edit_title(self, loader_mock, saver_mock, mock_out):
        test_task = {
            "id": 1,
            "title": "design blog section",
            "date": "2018-09-02",
            "week": "2018W35",
            "location": "",
            "project": "",
            "highPriority": False,
            "isDone": True
        }
        self.mock_args.task_id = 1
        saver_mock.return_value = 1
        loader_mock.return_value = dict.copy(test_task)
        self.mock_args.title = "new_title"

        task.edit_task(self.mock_args)

        expected_new_test_task = dict.copy(test_task)
        expected_new_test_task["title"] = "new_title"
        formatted_task = output_formatter.format_task(expected_new_test_task)
        expected = "You've changed task 1 to the following:\n" + formatted_task + "\n"

        self.assertEqual(mock_out.getvalue(), expected)
        saver_mock.assert_called()


    @unittest.mock.patch('sys.stderr', new_callable=io.StringIO)
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    @unittest.mock.patch('todoster.task.save_task')
    @unittest.mock.patch('todoster.task.load_task')
    def test_edit_task_try_to_delete_title(self, loader_mock, saver_mock, mock_out, mock_err):
        test_task = {
            "id": 1,
            "title": "design blog section",
            "date": "2018-09-02",
            "week": "2018W35",
            "location": "",
            "project": "",
            "highPriority": False,
            "isDone": True
        }
        self.mock_args.task_id = 1
        saver_mock.return_value = 1
        loader_mock.return_value = dict.copy(test_task)
        self.mock_args.title = ""

        formatted_task = output_formatter.format_task(test_task)
        expected_err = "The title of a task cannot be empty. This entry will not be saved.\n"
        expected = "You've changed task 1 to the following:\n" + formatted_task + "\n"
        task.edit_task(self.mock_args)
        self.assertEqual(mock_err.getvalue(), expected_err)
        self.assertEqual(mock_out.getvalue(), expected)
        saver_mock.assert_called()


    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    @unittest.mock.patch('todoster.task.save_task')
    @unittest.mock.patch('todoster.task.load_task')
    def test_edit_task_edit_location(self, loader_mock, saver_mock, mock_out):
        test_task = {
            "id": 1,
            "title": "design blog section",
            "date": "2018-09-02",
            "week": "2018W35",
            "location": "",
            "project": "",
            "highPriority": False,
            "isDone": True
        }
        self.mock_args.task_id = 1
        saver_mock.return_value = 1
        loader_mock.return_value = dict.copy(test_task)
        self.mock_args.location = "new_location"

        task.edit_task(self.mock_args)

        expected_new_test_task = dict.copy(test_task)
        expected_new_test_task["location"] = "new_location"
        formatted_task = output_formatter.format_task(expected_new_test_task)
        expected = "You've changed task 1 to the following:\n" + formatted_task + "\n"

        self.assertEqual(mock_out.getvalue(), expected)
        saver_mock.assert_called()

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    @unittest.mock.patch('todoster.task.save_task')
    @unittest.mock.patch('todoster.task.load_task')
    def test_edit_task_remove_location(self, loader_mock, saver_mock, mock_out):
        test_task = {
            "id": 1,
            "title": "design blog section",
            "date": "2018-09-02",
            "week": "2018W35",
            "location": "",
            "project": "",
            "highPriority": False,
            "isDone": True
        }
        self.mock_args.task_id = 1
        saver_mock.return_value = 1
        loader_mock.return_value = dict.copy(test_task)
        self.mock_args.location = ""

        task.edit_task(self.mock_args)

        expected_new_test_task = dict.copy(test_task)
        expected_new_test_task["location"] = ""
        formatted_task = output_formatter.format_task(expected_new_test_task)
        expected = "You've changed task 1 to the following:\n" + formatted_task + "\n"

        self.assertEqual(mock_out.getvalue(), expected)
        saver_mock.assert_called()

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    @unittest.mock.patch('todoster.task.save_task')
    @unittest.mock.patch('todoster.task.load_task')
    @unittest.mock.patch('todoster.task.load_project_by_shortcode')
    def test_edit_task_edit_project(self, project_mock, loader_mock, saver_mock, mock_out):
        test_task = {
            "id": 1,
            "title": "design blog section",
            "date": "2018-09-02",
            "week": "2018W35",
            "location": "",
            "project": "",
            "highPriority": False,
            "isDone": True
        }
        test_project = {
            "id": 1,
            "title": "some proj",
            "shortcode": "some-proj",
            "color": "default",
            "isActive": True
        }
        self.mock_args.task_id = 1
        saver_mock.return_value = 1
        project_mock.return_value = test_project
        loader_mock.return_value = dict.copy(test_task)
        self.mock_args.project = "some-proj"

        task.edit_task(self.mock_args)

        expected_new_test_task = dict.copy(test_task)
        expected_new_test_task["project"] = test_project
        formatted_task = output_formatter.format_task(expected_new_test_task)
        expected = "You've changed task 1 to the following:\n" + formatted_task + "\n"

        self.assertEqual(mock_out.getvalue(), expected)
        saver_mock.assert_called()

    @unittest.mock.patch('todoster.task.save_task')
    @unittest.mock.patch('todoster.task.load_task')
    def test_edit_task_try_to_add_invalid_project(self, loader_mock, saver_mock):
        test_task = {
            "id": 1,
            "title": "design blog section",
            "date": "2018-09-02",
            "week": "2018W35",
            "location": "",
            "project": "",
            "highPriority": False,
            "isDone": True
        }
        self.mock_args.task_id = 1
        saver_mock.return_value = 1
        loader_mock.return_value = dict.copy(test_task)
        self.mock_args.project = "merp"

        with self.assertRaises(SystemExit):
            task.edit_task(self.mock_args)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    @unittest.mock.patch('todoster.task.save_task')
    @unittest.mock.patch('todoster.task.load_task')
    def test_edit_task_remove_project(self, loader_mock, saver_mock, mock_out):
        test_task = {
            "id": 1,
            "title": "design blog section",
            "date": "2018-09-02",
            "week": "2018W35",
            "location": "",
            "project": "",
            "highPriority": False,
            "isDone": True
        }
        self.mock_args.task_id = 1
        saver_mock.return_value = 1
        loader_mock.return_value = dict.copy(test_task)
        self.mock_args.project = ""

        task.edit_task(self.mock_args)

        expected_new_test_task = dict.copy(test_task)
        expected_new_test_task["project"] = ""
        formatted_task = output_formatter.format_task(expected_new_test_task)
        expected = "You've changed task 1 to the following:\n" + formatted_task + "\n"

        self.assertEqual(mock_out.getvalue(), expected)
        saver_mock.assert_called()

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    @unittest.mock.patch('todoster.task.save_task')
    @unittest.mock.patch('todoster.task.load_task')
    def test_edit_task_make_high_prio(self, loader_mock, saver_mock, mock_out):
        test_task = {
            "id": 1,
            "title": "design blog section",
            "date": "2018-09-02",
            "week": "2018W35",
            "location": "",
            "project": "",
            "highPriority": False,
            "isDone": True
        }
        self.mock_args.task_id = 1
        saver_mock.return_value = 1
        loader_mock.return_value = dict.copy(test_task)
        self.mock_args.highPriority = True

        task.edit_task(self.mock_args)

        expected_new_test_task = dict.copy(test_task)
        expected_new_test_task["highPriority"] = True
        formatted_task = output_formatter.format_task(expected_new_test_task)
        expected = "You've changed task 1 to the following:\n" + formatted_task + "\n"

        self.assertEqual(mock_out.getvalue(), expected)
        saver_mock.assert_called()


if __name__ == '__main__':
    unittest.main()
