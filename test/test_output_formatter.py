import unittest

from todoster import output_formatter

class Testformat(unittest.TestCase):
    bold = "\033[1m"
    dim = "\033[2m"
    ul = "\033[4m"
    reset = "\033[0m"
    color_default = "\033[39m"
    color_red = "\033[31m"

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_format_headline(self):
        expected_base = self.bold + self.ul

        input_string = "merp"
        self.assertEqual(output_formatter.format_headline(input_string), expected_base + self.color_default + input_string + self.reset)
        self.assertEqual(output_formatter.format_headline(input_string, color="red"), expected_base + self.color_red + input_string + self.reset)

        appendix = "something"
        expected = self.ul + " (" + appendix + ")" + self.reset
        self.assertEqual(output_formatter.format_headline("", appendix), expected_base + self.color_default + self.reset + expected)



    def test_format_task(self): #pylint: disable=R0914
        mock_task = {"id": 2,
                    "title": "finish front-page design",
                    "date": "2018-09-02",
                    "week": "2018W35",
                    "location": "Somewhere",
                    "project": {
                        "shortcode": "project",
                        "color": "blue"
                        },
                    "highPriority": True,
                    "isDone": False
                    }

        prio = "\033[33m★" + self.reset
        done = " " + "☐"
        id_val = " " + self.dim + "  2." + self.reset
        title = " finish front-page design" + self.reset
        date = " " + self.bold + "@2018-09-02" + self.reset
        week = " " + self.bold + "@W35" + self.reset
        location = " " + "->Somewhere" + self.reset
        project = " " + self.bold + "\033[34m" + "#project" + self.reset

        self.assertEqual(output_formatter.format_task(mock_task), prio + done + id_val + title + date + location + project)

        mock_task["isDone"] = True
        done_done = " " + "\033[32m✓" + self.reset
        done_title = " " + self.dim + "finish front-page design" + self.reset
        done_date = " " + self.bold + self.dim + "@2018-09-02" + self.reset
        done_location = " " + self.dim + "->Somewhere" + self.reset
        done_project = " " + self.bold + self.dim + "\033[34m" + "#project" + self.reset
        self.assertEqual(output_formatter.format_task(mock_task), prio + done_done + id_val + done_title + done_date + done_location + done_project)
        mock_task["isDone"] = False

        mock_task["date"] = ""
        self.assertEqual(output_formatter.format_task(mock_task), prio + done + id_val + title + week + location + project)
        mock_task["location"] = ""
        self.assertEqual(output_formatter.format_task(mock_task), prio + done + id_val + title + week + project)
        mock_task["project"] = ""
        self.assertEqual(output_formatter.format_task(mock_task), prio + done + id_val + title + week)
        mock_task["week"] = ""
        self.assertEqual(output_formatter.format_task(mock_task), prio + done + id_val + title)
        mock_task["highPriority"] = False
        self.assertEqual(output_formatter.format_task(mock_task), " " + done + id_val + title)


    def test_format_project(self):
        mock_proj = {
                    "id": 22,
                    "title": "work",
                    "shortcode": "work",
                    "color": "red",
                    "active": True
                    }

        expected = "\"work\" (" + self.color_red + "#work" + self.reset + ")"

        self.assertEqual(output_formatter.format_project(mock_proj), expected)


    def test_format_task_block(self):
        mock_tasks = [{"id": 2,
                    "title": "finish front-page design",
                    "date": "2018-09-02",
                    "week": "2018W35",
                    "location": "Somewhere",
                    "project": {
                        "shortcode": "project",
                        "color": "blue"
                        },
                    "highPriority": True,
                    "isDone": False
                    },
                    {"id": 3,
                    "title": "finish front-page design",
                    "date": "2018-09-02",
                    "week": "2018W35",
                    "location": "Somewhere",
                    "project": {
                        "shortcode": "project",
                        "color": "blue"
                        },
                    "highPriority": True,
                    "isDone": False}]

        context = "this"

        expected_task_format = output_formatter.format_task(mock_tasks[0]) + "\n" + output_formatter.format_task(mock_tasks[1]) + "\n\n"
        expected_empty_message = self.dim + "   --- No tasks for this " + context + " ---" + self.reset + "\n\n"

        self.assertEqual(output_formatter.format_task_block(context, []), expected_empty_message)
        self.assertEqual(output_formatter.format_task_block(context, mock_tasks), expected_task_format)

        mock_no_proj = mock_tasks
        mock_no_proj[0]["project"] = ""
        mock_no_proj[1]["project"] = ""
        expected_task_format = output_formatter.format_task(mock_no_proj[0]) + "\n" + output_formatter.format_task(mock_no_proj[1]) + "\n\n"
        self.assertEqual(output_formatter.format_task_block(context, mock_tasks, print_project=False), expected_task_format)

        mock_no_date = mock_tasks
        mock_no_date[0]["date"] = ""
        mock_no_date[0]["week"] = ""
        mock_no_date[1]["date"] = ""
        mock_no_date[1]["week"] = ""
        expected_task_format = output_formatter.format_task(mock_no_date[0]) + "\n" + output_formatter.format_task(mock_no_date[1]) + "\n\n"
        self.assertEqual(output_formatter.format_task_block(context, mock_tasks, print_date=False), expected_task_format)

        mock_no_loc = mock_tasks
        mock_no_loc[0]["location"] = ""
        mock_no_loc[1]["location"] = ""
        expected_task_format = output_formatter.format_task(mock_no_loc[0]) + "\n" + output_formatter.format_task(mock_no_loc[1]) + "\n\n"
        self.assertEqual(output_formatter.format_task_block(context, mock_tasks, print_location=False), expected_task_format)


if __name__ == '__main__':
    unittest.main()
