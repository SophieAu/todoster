import unittest
from unittest.mock import patch
import io

from todoster import output_formatter
from todoster import list_projects

class MockArgs:  #pylint: disable=R0903
    show_all_projects = True

class TestListProjects(unittest.TestCase):
    mock_args = None

    def setUp(self):
        self.mock_args = MockArgs()

    def tearDown(self):
        pass

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('todoster.list_projects.load_projects')
    def test_list_projects(self, loader_mock, mock_out):
        loader_mock.return_value = [{
                    "id": 1,
                    "title": "active",
                    "shortcode": "active",
                    "color": "green",
                    "active": True
                    }, {
                    "id": 2,
                    "title": "inactive",
                    "shortcode": "inactive",
                    "color": "red",
                    "active": False
                    }]
        expected_active = output_formatter.format_string("  1", dim=True) + " " + "active" + "\033[0m" + " (\033[32m#active\033[0m)"
        expected_inactive = output_formatter.format_string("  2", dim=True) + " \033[2m" + "inactive" + "\033[0m" + " (\033[31m#inactive\033[0m)"

        list_projects.list_projects(self.mock_args)
        self.assertEqual(mock_out.getvalue(), "\n" + expected_active + "\n" + expected_inactive + "\n\n")
        mock_out.truncate(0)
        mock_out.seek(0)

        self.mock_args.show_all_projects = False
        list_projects.list_projects(self.mock_args)
        self.assertEqual(mock_out.getvalue(), "\n" + expected_active + "\n\n")
        mock_out.truncate(0)
        mock_out.seek(0)


if __name__ == '__main__':
    unittest.main()
