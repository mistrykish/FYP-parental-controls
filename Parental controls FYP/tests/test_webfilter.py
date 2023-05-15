import unittest
from unittest.mock import MagicMock
from io import StringIO
import sys
import tkinter as tk  
from webFilter import WebFiltering # Replace your_module_name with the actual name of your module for a reminder


class TestWebFiltering(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.web_filtering = WebFiltering(self.root)

    def test_is_valid_url(self):
        self.assertTrue(self.web_filtering.is_valid_url("www.example.com"))
        self.assertTrue(self.web_filtering.is_valid_url("example.com"))
        self.assertFalse(
            self.web_filtering.is_valid_url("htttp://invalid_url"))

        # Test invalid URLs
        self.assertFalse(self.web_filtering.is_valid_url('invalid_url'))
        self.assertFalse(self.web_filtering.is_valid_url('google'))

    def test_is_valid_time(self):
        # Test valid time strings
        self.assertTrue(self.web_filtering.is_valid_time('00:00'))
        self.assertTrue(self.web_filtering.is_valid_time('23:59'))

        # Test invalid time strings
        self.assertFalse(self.web_filtering.is_valid_time('24:00'))
        self.assertFalse(self.web_filtering.is_valid_time('23:60'))
        self.assertFalse(self.web_filtering.is_valid_time('2400'))
        self.assertFalse(self.web_filtering.is_valid_time('00:001'))


if __name__ == '__main__':
    unittest.main()
