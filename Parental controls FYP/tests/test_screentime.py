import unittest
from unittest.mock import patch
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk
import schedule
import sched
import time
from datetime import datetime, timedelta
import threading
import pytz
import sqlite3
import ctypes
import re
from ScreenTiming import Screen


class TestScreen(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()

    def test_screen(self):
        screen = Screen(self.root)

        # Test if the screen has been initialized correctly
        self.assertEqual(screen.day_dropdown.get(), "Select Day")
        self.assertEqual(screen.start_time.get(), "")
        self.assertEqual(screen.end_time.get(), "")
        self.assertEqual(screen.schedule_button.cget("text"), "Schedule")
        self.assertEqual(screen.remove_button.cget("text"), "Remove")

    def test_is_valid_time(self):
        screen = Screen(self.root)

        # Test with valid time string
        self.assertTrue(screen.is_valid_time("08:30"))

        # Test with invalid time string
        self.assertFalse(screen.is_valid_time("25:00"))

    @patch("ScreenTiming.Screen.show_screen_timeout")
    def test_schedule_timeout(self, mock_show_screen_timeout):
        screen = Screen(self.root)
        screen.schedule_timeout("08", "30")
        schedule.run_all()

        # Test if show_screen_timeout method is called
        mock_show_screen_timeout.assert_called_once()

    @patch("ScreenTiming.Screen.remove_entry")
    def test_schedule_end(self, mock_remove_entry):
        screen = Screen(self.root)
        screen.schedule_end("09", "30", "Monday", "08:30", "09:30")
        schedule.run_all()

        # Test if remove_entry method is called
        mock_remove_entry.assert_called_once_with("Monday", "08:30", "09:30")

    def tearDown(self):
        self.root.destroy()


if __name__ == '__main__':
    unittest.main()
