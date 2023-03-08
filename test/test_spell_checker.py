import sys
import unittest
from unittest.mock import patch

sys.path.append("src")

from spell_checker import get_response_for, parse_response, is_spelling_correct


class SpellCheckerTest(unittest.TestCase):
    def test_get_response_for_returns_some_response(self, word="FAVOR"):
        response = get_response_for(word)

        self.assertGreater(len(response), 0)

    def test_parse_response_true(self):
        self.assertTrue(parse_response("true"))

    def test_parse_response_false(self):
        self.assertFalse(parse_response("false"))

    @patch('spell_checker.parse_response')
    @patch('spell_checker.get_response_for')
    def test_is_spelling_correct_calls_get_response_and_parse(self, get_response_for_mock, parse_response_mock):
        get_response_for_mock.return_value = "true"
        parse_response_mock.return_value = True
        is_spelling_correct("FAVOR")

        get_response_for_mock.assert_called_once_with("FAVOR")
        parse_response_mock.assert_called_once_with("true")

    @patch('spell_checker.get_response_for')
    def test_is_spelling_correct_passes_exception_from_get_response(self, get_response_for_mock):
        get_response_for_mock.side_effect = Exception("Exception in get response")

        with self.assertRaises(Exception) as exception:
            is_spelling_correct("FAVOR")

        self.assertEqual(str(exception.exception), "Exception in get response")
