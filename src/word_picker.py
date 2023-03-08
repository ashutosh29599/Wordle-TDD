import random
import time

import requests


def get_response():
    url = "https://agilec.cs.uh.edu/words"

    return requests.get(url).text


def parse_response(text):
    if text.startswith("[") and text.rstrip().endswith("]"):
        return list(filter(None, text[1:-1].rstrip().replace(' ', '').split(',')))

    raise Exception("Response is not a list")


def get_a_random_word_given_a_seed(seed, words):
    if (not hasattr(get_a_random_word_given_a_seed, "seed")) or (get_a_random_word_given_a_seed.seed != seed):
        get_a_random_word_given_a_seed.seed = seed
        random.seed(seed)

    return random.choice(words)


def get_a_random_word():
    seed = time.time_ns()
    word = get_a_random_word_given_a_seed(seed, parse_response(get_response()))

    if len(word) != 5:
        raise Exception("Word should be length of 5")

    return word.upper()
