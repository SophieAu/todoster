import unittest
import unittest.mock

import io

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


class TestTask(unittest.TestCase):
    mock_args = None

    def setUp(self):
        self.mock_args = MockArgs()
        self.mock_args.title = ""
        self.mock_args.date = ""
        self.mock_args.week = ""
        self.mock_args.location = ""
        self.mock_args.project = None
        self.mock_args.highPriority = False  #pylint: disable=C0103
        self.mock_args.isDone = False  #pylint: disable=C0103

    def tearDown(self):
        pass


    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    @unittest.mock.patch('todoster.task.save_task')
    @unittest.mock.patch('todoster.task.load_task')
    def test_mark_task_as_completed(self, loader_mock, saver_mock, mock_out):
        test_task = {
            "id": 1,
            "title": "design blog section",
            "date": "2018-09-02",
            "week": "2018W35",
            "location": "",
            "project": "",
            "highPriority": False,
            "isDone": False
        }
        self.mock_args.task_id = 1
        saver_mock.return_value = 1
        loader_mock.return_value = dict.copy(test_task)

        expected_new_test_task = dict.copy(test_task)
        expected_new_test_task["isDone"] = True

        expected = "Task '" + test_task["title"] + "' has been marked as done.\n"
        task.check_task(self.mock_args)
        self.assertEqual(mock_out.getvalue(), expected)
        saver_mock.assert_called()


    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    @unittest.mock.patch('todoster.task.save_task')
    @unittest.mock.patch('todoster.task.load_task')
    def test_mark_task_as_not_completed(self, loader_mock, saver_mock, mock_out):
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

        self.mock_args.uncheck = True

        expected_new_test_task = dict.copy(test_task)
        expected_new_test_task["isDone"] = True

        expected = "Task '" + test_task["title"] + "' has been marked as not done.\n"
        task.check_task(self.mock_args)
        self.assertEqual(mock_out.getvalue(), expected)
        saver_mock.assert_called()


if __name__ == '__main__':
    unittest.main()
