#!/usr/bin/env python3
"""
Test module lib6.py
"""
import unittest
import client

__author__ = 'Matthew Thompson'
__version__ = 'Fall 2021'
__pylint__ = 'v1.8.3.'


class TestUtils(unittest.TestCase):
    """Test Utils class"""

    def test_invalid_entry_random(self):
        """
        random word
        """
        val = 'random'
        self.assertEqual(False, client.check_channel_input(val))

    def test_invalid_entry_capital(self):
        """
        not capitalized
        """
        val = 'py'
        self.assertEqual(False, client.check_channel_input(val))

    def test_invalid_entry_extra(self):
        """
        extra letters
        """
        val = 'PYDB'
        self.assertEqual(False, client.check_channel_input(val))

    def test_valid_entry_py(self):
        """
        Valid
        """
        val = 'PY'
        self.assertEqual(True, client.check_channel_input(val))

    def test_valid_entry_qa(self):
        """
        Valid
        """
        val = 'QA'
        self.assertEqual(True, client.check_channel_input(val))

    def test_valid_entry_db(self):
        """
        Valid
        """
        val = 'DB'
        self.assertEqual(True, client.check_channel_input(val))

    @staticmethod
    def test_close():
        """closes the client"""
        client.close()

if __name__ == '__main__':
    unittest.main()
