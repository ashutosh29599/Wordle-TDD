import unittest
from unittest.mock import patch, ANY

from word_picker import get_response, parse_response, get_a_random_word_given_a_seed, get_a_random_word


class WordPickerTest(unittest.TestCase):
    def test_get_response_returns_some_response(self):
        response = get_response()

        self.assertGreater(len(response), 0)

    def test_parse_response_for_word_list(self):
        word_list = parse_response("[FAVOR, GUESS]")

        self.assertEqual(word_list, ["FAVOR", "GUESS"])

    def test_parse_response_for_empty_list(self):
        word_list = parse_response("[]")

        self.assertEqual(word_list, [])

    def test_parse_response_raise_exception_if_not_list(self):
        with self.assertRaises(Exception) as exception:
            parse_response("FAVOR")

        self.assertEqual(str(exception.exception), "Response is not a list")

    def test_get_a_random_word_given_a_seed_and_list_of_words(self, seed=404):
        list_of_words = ["FAVOR", "GUESS", "RAPID"]

        random_word = get_a_random_word_given_a_seed(seed, list_of_words)

        self.assertIn(random_word, list_of_words)

    def test_get_a_random_word_given_a_seed_returns_two_different_random_words(self, seed=10384933884848448):
        list_of_words = ["FAVOR", "GUESS", "RAPID"]

        random_word_1 = get_a_random_word_given_a_seed(seed, list_of_words)
        random_word_2 = get_a_random_word_given_a_seed(seed, list_of_words)

        self.assertIn(random_word_1, list_of_words)
        self.assertIn(random_word_2, list_of_words)
        self.assertNotEqual(random_word_1, random_word_2)

    @patch('word_picker.get_a_random_word_given_a_seed')
    @patch('word_picker.parse_response')
    @patch('word_picker.get_response')
    def test_get_a_random_word_calls_get_response_parse_get_a_random_word_given_a_seed(self, get_response_mock, parse_response_mock, get_a_random_word_given_a_seed_mock):
        get_response_mock.return_value = "[FAVOR, GUESS, RAPID]"
        parse_response_mock.return_value = ["FAVOR", "GUESS", "RAPID"]
        get_a_random_word_given_a_seed_mock.return_value = "FAVOR"

        get_a_random_word()

        get_response_mock.assert_called_once()
        parse_response_mock.assert_called_once_with("[FAVOR, GUESS, RAPID]")
        get_a_random_word_given_a_seed_mock.assert_called_once_with(ANY, ["FAVOR", "GUESS", "RAPID"])

    @patch('word_picker.get_a_random_word_given_a_seed')
    @patch('word_picker.parse_response')
    def test_get_a_random_word_calls_get_random_word_given_a_seed_with_a_seed(self, parse_response_mock,
                                                                              get_a_random_word_given_a_seed_mock):
        parse_response_mock.return_value = ["FAVOR"]
        get_a_random_word_given_a_seed_mock.return_value = "FAVOR"

        get_a_random_word()

        get_a_random_word_given_a_seed_mock.assert_called_once_with(ANY, ANY)

    @patch('word_picker.get_a_random_word_given_a_seed')
    @patch('word_picker.parse_response')
    def test_get_a_random_word_calls_get_random_word_given_a_seed_with_a_different_seed_second_time(self,
                                                                                                    parse_response_mock,
                                                                                                    get_a_random_word_given_a_seed_mock):
        parse_response_mock.return_value = ["FAVOR"]
        get_a_random_word_given_a_seed_mock.return_value = "FAVOR"

        get_a_random_word()
        first_seed = get_a_random_word_given_a_seed_mock.call_args_list[0][0][0]

        get_a_random_word()
        second_seed = get_a_random_word_given_a_seed_mock.call_args_list[1][0][0]

        self.assertNotEqual(first_seed, second_seed)

    @patch('word_picker.parse_response')
    def test_check_the_random_word_is_of_length_5(self, parse_response_mock):
        parse_response_mock.return_value = ["FAVO"]

        with self.assertRaises(Exception) as exception:
            get_a_random_word()

        self.assertEqual(str(exception.exception), "Word should be length of 5")

    @patch('word_picker.parse_response')
    def test_check_the_random_word_is_in_all_caps(self, parse_response_mock):
        parse_response_mock.return_value = ["favor"]

        word = get_a_random_word()
        self.assertEqual(word, "FAVOR")
