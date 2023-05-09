import unittest
from unittest.mock import MagicMock
import sqlite3
from io import StringIO
from webMonitor import WebMonitoring


class TestWebMonitoring(unittest.TestCase):

    def setUp(self):
        # Set up a dummy Tkinter master for testing
        self.master = MagicMock()
        self.web_monitoring = WebMonitoring(self.master)

    def test_order_ascending(self):
        self.web_monitoring.order_ascending()
        rows = self.web_monitoring.tree.get_children()
        last_visit_time_prev = None
        for row in rows:
            last_visit_time = self.web_monitoring.tree.item(row)['values'][0]
            if last_visit_time_prev:
                self.assertLessEqual(last_visit_time_prev, last_visit_time)
            last_visit_time_prev = last_visit_time

    def test_order_descending(self):
        self.web_monitoring.order_descending()
        rows = self.web_monitoring.tree.get_children()
        last_visit_time_prev = None
        for row in rows:
            last_visit_time = self.web_monitoring.tree.item(row)['values'][0]
            if last_visit_time_prev:
                self.assertGreaterEqual(last_visit_time_prev, last_visit_time)
            last_visit_time_prev = last_visit_time

    def test_total_visits(self):
        self.web_monitoring.total_visits = MagicMock(return_value=42)
        total_visits = self.web_monitoring.total_visits()
        self.assertEqual(total_visits, 42)

    def test_average_visits(self):
        self.web_monitoring.average_visits = MagicMock(return_value=3.5)
        average_visits = self.web_monitoring.average_visits()
        self.assertAlmostEqual(average_visits, 3.5)

    def test_switch_browser(self):
        self.web_monitoring.switch_browser()
        self.assertEqual(self.web_monitoring.browser, "edge")

        self.web_monitoring.switch_browser()
        self.assertEqual(self.web_monitoring.browser, "chrome")

    def test_load_history(self):
        # Mock the database connection and cursor
        mock_conn = MagicMock(spec=sqlite3.Connection)
        mock_cursor = MagicMock(spec=sqlite3.Cursor)
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []

        with unittest.mock.patch("sqlite3.connect", return_value=mock_conn):
            self.web_monitoring.load_history()
            mock_cursor.execute.assert_called_once()
            mock_cursor.fetchall.assert_called_once()


if __name__ == "__main__":
    unittest.main()
