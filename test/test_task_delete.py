import unittest
from unittest.mock import patch
import io

from todoster import task

class MockArgs:  #pylint: disable=R0903
    task_id = ""


class TestTask(unittest.TestCase):
    mock_args = None

    def setUp(self):
        self.mock_args = MockArgs()

    def tearDown(self):
        pass


    @patch('builtins.input', side_effect=['y'])
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('todoster.task.remove_task')
    @patch('todoster.task.load_task')
    def test_delete_task_say_yes(self, loader_mock, remove_mock, mock_out, _):
        self.mock_args.task_id = 1
        loader_mock.return_value = {
            "id": 1,
            "title": "design blog section",
            "date": "2018-09-02",
            "week": "2018W35",
            "location": "",
            "project": "",
            "highPriority": False,
            "isDone": False
        }

        expected_deletable_task = "design blog section"
        expected_outcome = "Task deleted."
        task.delete_task(self.mock_args)
        self.assertNotEqual(mock_out.getvalue().find(expected_deletable_task), -1)
        self.assertNotEqual(mock_out.getvalue().find(expected_outcome), -1)
        remove_mock.assert_called()

    @patch('builtins.input', side_effect=['n'])
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('todoster.task.remove_task')
    @patch('todoster.task.load_task')
    def test_delete_task_say_no(self, loader_mock, remove_mock, mock_out, _):
        self.mock_args.task_id = 1
        loader_mock.return_value = {
            "id": 1,
            "title": "design blog section",
            "date": "2018-09-02",
            "week": "2018W35",
            "location": "",
            "project": "",
            "highPriority": False,
            "isDone": False
        }

        expected_deletable_task = "design blog section"
        expected_outcome = "Task not deleted."
        task.delete_task(self.mock_args)
        self.assertNotEqual(mock_out.getvalue().find(expected_deletable_task), -1)
        self.assertNotEqual(mock_out.getvalue().find(expected_outcome), -1)
        remove_mock.assert_not_called()

if __name__ == '__main__':
    unittest.main()
