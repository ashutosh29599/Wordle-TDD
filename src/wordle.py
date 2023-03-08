from game_status import GameStatus
from match import Match

WORD_SIZE = 5
ALLOWED_ATTEMPTS = 6


def tally(target_word, guessed_word):
    if (len(guessed_word) != WORD_SIZE) or (len(target_word) != WORD_SIZE):
        raise Exception(f"word lengths should be {WORD_SIZE}")

    if target_word == guessed_word:
        return [Match.EXACT] * WORD_SIZE

    return [tally_for_position(i, letter_at_position, target_word, guessed_word) for i, letter_at_position in
            enumerate(guessed_word)]


def tally_for_position(position, letter_at_position, target_word, guessed_word):
    if target_word[position] == letter_at_position:
        return Match.EXACT

    positional_matches = count_positional_matches(target_word, guessed_word, letter_at_position)
    non_positional_occurrences_in_target = target_word.count(letter_at_position) - positional_matches

    number_of_occurrences_in_guess_until_position = guessed_word.count(letter_at_position, 0, position + 1)

    if non_positional_occurrences_in_target >= number_of_occurrences_in_guess_until_position:
        return Match.PRESENT

    return Match.NOMATCH


def count_positional_matches(target_word, guessed_word, letter):
    return sum(1 for i, target_letter in enumerate(target_word) if
               target_letter == letter and target_letter == guessed_word[i])


def winning_greeting_message(attempt):
    return ["Amazing", "Splendid", "Awesome"][attempt] if attempt < 3 else "Yay"


def play(target_word, guessed_word, attempts, is_spelling_correct=lambda _: True):
    if attempts >= ALLOWED_ATTEMPTS:
        raise Exception(f"maximum allowed attempts is {ALLOWED_ATTEMPTS}")

    result = []
    valid_attempts = attempts
    game_status = GameStatus.WRONG_SPELLING
    greeting_message = ""

    if is_spelling_correct(guessed_word):
        result = tally(target_word, guessed_word)
        valid_attempts = attempts + 1

        if result == [Match.EXACT] * WORD_SIZE:
            game_status = GameStatus.WIN
            greeting_message = winning_greeting_message(attempts)
        else:
            game_status, greeting_message = (GameStatus.INPROGRESS, "") if attempts < ALLOWED_ATTEMPTS - 1 else (
                GameStatus.LOSE, f"It was {target_word}, better luck next time")

    return {
        "tally": result,
        "attempts": valid_attempts,
        "game_status": game_status,
        "greeting_message": greeting_message
    }
