import unittest
import unittest.mock

import io
from  todoster import output_formatter
from  todoster import project

class MockArgs:  #pylint: disable=R0903
    id = 0
    title = ""
    shortcode = ""
    new_shortcode = ""
    color = "red"
    isActive = True

class TestProjects(unittest.TestCase):
    mock_args = None

    def setUp(self):
        self.mock_args = MockArgs
        self.mock_args.title = ""
        self.mock_args.shortcode = ""
        self.mock_args.new_shortcode = ""
        self.mock_args.color = "red"
        self.mock_args.isActive = True

    def tearDown(self):
        pass


    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    @unittest.mock.patch('todoster.project.save_project')
    def test_add_project(self, saver_mock, mock_out):
        saver_mock.return_value = None

        self.mock_args.title = "new_project"
        self.mock_args.shortcode = "new-proj"
        expected_print = "You created project \"" + "new_project" + "\" (" + output_formatter.format_string("#new-proj", color="red") + ").\n"

        project.add_project(self.mock_args)
        self.assertEqual(mock_out.getvalue(), expected_print)


    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    @unittest.mock.patch('sys.stderr', new_callable=io.StringIO)
    @unittest.mock.patch('todoster.project.save_project')
    def test_add_project_with_invalid_color(self, saver_mock, mock_err, mock_out):
        saver_mock.return_value = None

        self.mock_args.title = "new_project"
        self.mock_args.shortcode = "new-proj"
        self.mock_args.color = "turquoise"

        expected_error_start = "This is not a valid color. This entry will not be saved.\n"
        expected_print = "You created project \"" + "new_project" + "\" (" + output_formatter.format_string("#new-proj", color="default") + ").\n"

        project.add_project(self.mock_args)
        self.assertEqual(mock_err.getvalue(), expected_error_start)
        self.assertEqual(mock_out.getvalue(), expected_print)


    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    @unittest.mock.patch('todoster.project.save_project')
    def test_add_project_without_shortcode_specified(self, saver_mock, mock_out):
        saver_mock.return_value = None

        self.mock_args.title = "No Shortcode Project"

        expected_print = "You created project \"" + "No Shortcode Project" + "\" (" + output_formatter.format_string("#no-shortcode-project", color="red") + ").\n"
        project.add_project(self.mock_args)
        self.assertEqual(mock_out.getvalue(), expected_print)


    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    @unittest.mock.patch('todoster.project.save_project')
    @unittest.mock.patch('todoster.project.load_project_by_shortcode')
    def test_edit_project(self, loader_mock, saver_mock, mock_out):
        saver_mock.return_value = None
        loader_mock.return_value = {
                    "id": 1,
                    "title": "active",
                    "shortcode": "active",
                    "color": "green",
                    "active": True
                    }

        self.mock_args.title = "New Title"
        self.mock_args.new_shortcode = "new-code"
        self.mock_args.color = None

        expected_print = "You edited project \"" + "New Title" + "\" (" + output_formatter.format_string("#new-code", color="green") + ").\n"

        project.edit_project(self.mock_args)
        self.assertEqual(mock_out.getvalue(), expected_print)
        mock_out.truncate(0)
        mock_out.seek(0)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    @unittest.mock.patch('todoster.project.save_project')
    @unittest.mock.patch('todoster.project.load_project_by_shortcode')
    def test_archive_project(self, loader_mock, saver_mock, mock_out):
        saver_mock.return_value = None
        loader_mock.return_value = {
                    "id": 1,
                    "title": "active",
                    "shortcode": "active",
                    "color": "green",
                    "active": True
                    }

        expected_print = "Project 'active' has been marked as archived.\n"

        project.archive_project(self.mock_args)
        self.assertEqual(mock_out.getvalue(), expected_print)
        mock_out.truncate(0)
        mock_out.seek(0)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    @unittest.mock.patch('todoster.project.save_project')
    @unittest.mock.patch('todoster.project.load_project_by_shortcode')
    def test_activate_project(self, loader_mock, saver_mock, mock_out):
        saver_mock.return_value = None
        loader_mock.return_value = {
                    "id": 1,
                    "title": "active",
                    "shortcode": "active",
                    "color": "green",
                    "active": False
                    }

        expected_print = "Project 'active' has been marked as active.\n"

        project.archive_project(self.mock_args)
        self.assertEqual(mock_out.getvalue(), expected_print)
        mock_out.truncate(0)
        mock_out.seek(0)

    @unittest.mock.patch('builtins.input', side_effect=['y'])
    @unittest.mock.patch('todoster.project.remove_project')
    @unittest.mock.patch('todoster.project.remove_task')
    @unittest.mock.patch('todoster.project.load_tasks')
    @unittest.mock.patch('todoster.project.load_project_by_shortcode')
    def test_delete_project_say_yes(self, loader_mock, task_mock, dt_mock, dp_mock, mock_in):
        loader_mock.return_value = {
                    "id": 1,
                    "title": "active",
                    "shortcode": "active",
                    "color": "green",
                    "active": True
                    }
        task_mock.return_value = [{"id": 2,
                    "title": "finish front-page design",
                    "date": "2018-09-02",
                    "week": "2018W35",
                    "location": "Somewhere",
                    "project": 1,
                    "highPriority": True,
                    "isDone": False
                    },
                    {"id": 3,
                    "title": "finish front-page design",
                    "date": "2018-09-02",
                    "week": "2018W35",
                    "location": "Somewhere",
                    "project": 1,
                    "highPriority": True,
                    "isDone": False}]

        project.delete_project(self.mock_args)
        self.assertEqual(dt_mock.call_count, 2)
        self.assertEqual(dp_mock.call_count, 1)


    @unittest.mock.patch('builtins.input', side_effect=['n'])
    @unittest.mock.patch('todoster.project.remove_project')
    @unittest.mock.patch('todoster.project.remove_task')
    @unittest.mock.patch('todoster.project.load_tasks')
    @unittest.mock.patch('todoster.project.load_project_by_shortcode')
    def test_delete_project_say_np(self, loader_mock, task_mock, dt_mock, dp_mock, mock_in):
        loader_mock.return_value = {
                    "id": 1,
                    "title": "active",
                    "shortcode": "active",
                    "color": "green",
                    "active": True
                    }
        task_mock.return_value = [{"id": 2,
                    "title": "finish front-page design",
                    "date": "2018-09-02",
                    "week": "2018W35",
                    "location": "Somewhere",
                    "project": 1,
                    "highPriority": True,
                    "isDone": False
                    },
                    {"id": 3,
                    "title": "finish front-page design",
                    "date": "2018-09-02",
                    "week": "2018W35",
                    "location": "Somewhere",
                    "project": 1,
                    "highPriority": True,
                    "isDone": False}]

        project.delete_project(self.mock_args)
        dt_mock.assert_not_called()
        dp_mock.assert_not_called()


if __name__ == '__main__':
    unittest.main()
