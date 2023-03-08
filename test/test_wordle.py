import sys
import unittest

from parameterized import parameterized

sys.path.append("src")

from game_status import GameStatus
from match import Match
from wordle import tally, play

EXACT = Match.EXACT
NOMATCH = Match.NOMATCH
PRESENT = Match.PRESENT


class WordleTests(unittest.TestCase):
    def test_canary(self):
        self.assertTrue(True)

    @parameterized.expand([
        ("FAVOR", "FAVOR", [EXACT, EXACT, EXACT, EXACT, EXACT]),
        ("TESTS", "FAVOR", [NOMATCH, NOMATCH, NOMATCH, NOMATCH, NOMATCH]),
        ("RAPID", "FAVOR", [PRESENT, EXACT, NOMATCH, NOMATCH, NOMATCH]),
        ("MAYOR", "FAVOR", [NOMATCH, EXACT, NOMATCH, EXACT, EXACT]),
        ("RIVER", "FAVOR", [NOMATCH, NOMATCH, EXACT, NOMATCH, EXACT]),
        ("AMAST", "FAVOR", [PRESENT, NOMATCH, NOMATCH, NOMATCH, NOMATCH]),
        ("SKILL", "SKILL", [EXACT, EXACT, EXACT, EXACT, EXACT]),
        ("SWIRL", "SKILL", [EXACT, NOMATCH, EXACT, NOMATCH, EXACT]),
        ("CIVIL", "SKILL", [NOMATCH, PRESENT, NOMATCH, NOMATCH, EXACT]),
        ("SHIMS", "SKILL", [EXACT, NOMATCH, EXACT, NOMATCH, NOMATCH]),
        ("SILLY", "SKILL", [EXACT, PRESENT, PRESENT, EXACT, NOMATCH]),
        ("SLICE", "SKILL", [EXACT, PRESENT, EXACT, NOMATCH, NOMATCH]),
    ])
    def test_tally(self, guessed_word, target_word, expected):
        self.assertEqual(tally(target_word, guessed_word), expected)

    @parameterized.expand([
        ("FOR", "FAVOR"),
        ("FERVER", "FAVOR"),
    ])
    def test_tally_invalid_length(self, guessed_word, target_word):
        with self.assertRaises(Exception) as exception:
            tally(target_word, guessed_word)
            self.assertEqual(str(exception.exception), "word lengths should be 5")

    @parameterized.expand([
        ("FAVOR", 0, "Amazing"),
        ("FAVOR", 1, "Splendid"),
        ("FAVOR", 2, "Awesome"),
        ("FAVOR", 3, "Yay"),
        ("FAVOR", 4, "Yay"),
        ("FAVOR", 5, "Yay"),
    ])
    def test_play(self, target_word, attempts, greeting_message):
        self.assertEqual(play(target_word, target_word, attempts),
                         {
                             "tally": [EXACT, EXACT, EXACT, EXACT, EXACT],
                             "attempts": attempts + 1,
                             "game_status": GameStatus.WIN,
                             "greeting_message": greeting_message
                         })

    def test_play_first_attempt_invalid_guess(self, target_word="FAVOR", guessed_word="FOR", attempts=0):
        with self.assertRaises(Exception) as exception:
            play(target_word, guessed_word, attempts)
            self.assertEqual(str(exception.exception), "word lengths should be 5")

    @parameterized.expand([
        ("FAVOR", "RAPID", 0, GameStatus.INPROGRESS, ""),
        ("FAVOR", "RAPID", 1, GameStatus.INPROGRESS, ""),
        ("FAVOR", "RAPID", 2, GameStatus.INPROGRESS, ""),
        ("FAVOR", "RAPID", 3, GameStatus.INPROGRESS, ""),
        ("FAVOR", "RAPID", 4, GameStatus.INPROGRESS, ""),
        ("FAVOR", "RAPID", 5, GameStatus.LOSE, "It was FAVOR, better luck next time"),
    ])
    def test_play_non_winning_guess(self, target_word, guessed_word, attempts, game_status, greeting_message):
        self.assertEqual(play(target_word, guessed_word, attempts),
                         {
                             "tally": [PRESENT, EXACT, NOMATCH, NOMATCH, NOMATCH],
                             "attempts": attempts + 1,
                             "game_status": game_status,
                             "greeting_message": greeting_message
                         })

    @parameterized.expand([
        ("FAVOR", "FAVOR", 6),
        ("FAVOR", "RAPID", 7),
    ])
    def test_play_guess_after_six_attempts(self, target_word, guessed_word, attempts):
        with self.assertRaises(Exception) as exception:
            play(target_word, guessed_word, attempts)
            self.assertEqual(str(exception.exception), "maximum allowed attempts is 6")

    def test_play_with_correct_spelling(self, guessed_word="FAVOR"):
        def is_spelling_correct_mock(word):
            is_spelling_correct_mock.called_with = word
            return True

        play("FAVOR", guessed_word, 0, is_spelling_correct_mock)

        self.assertEqual(guessed_word, is_spelling_correct_mock.called_with)

    def test_play_with_another_correct_spelling(self, guessed_word="RAPID"):
        def is_spelling_correct_mock(word):
            is_spelling_correct_mock.called_with = word
            return True

        play("FAVOR", guessed_word, 0, is_spelling_correct_mock)

        self.assertEqual(guessed_word, is_spelling_correct_mock.called_with)

    def test_play_with_wrong_spelling(self, guessed_word="FAVOR"):
        def is_spelling_correct_mock(word):
            is_spelling_correct_mock.called_with = word
            return False

        self.assertEqual(play("FAVOR", guessed_word, 0, is_spelling_correct_mock), {
            "tally": [],
            "attempts": 0,
            "game_status": GameStatus.WRONG_SPELLING,
            "greeting_message": ""
        })
        self.assertEqual(guessed_word, is_spelling_correct_mock.called_with)

    def test_play_with_another_wrong_spelling(self, guessed_word="RAPID"):
        def is_spelling_correct_mock(word):
            is_spelling_correct_mock.called_with = word
            return False

        self.assertEqual(play("FAVOR", guessed_word, 0, is_spelling_correct_mock), {
            "tally": [],
            "attempts": 0,
            "game_status": GameStatus.WRONG_SPELLING,
            "greeting_message": ""
        })
        self.assertEqual(guessed_word, is_spelling_correct_mock.called_with)

    def test_play_with_exception_in_spell_check(self, guessed_word="FAVOR"):
        def is_spelling_correct_mock(word):
            is_spelling_correct_mock.called_with = word
            raise Exception("Exception in spell check")

        with self.assertRaises(Exception) as exception:
            play("FAVOR", guessed_word, 0, is_spelling_correct_mock)

        self.assertEqual(str(exception.exception), "Exception in spell check")

        self.assertEqual(guessed_word, is_spelling_correct_mock.called_with)


if __name__ == '__main__':
    unittest.main()
