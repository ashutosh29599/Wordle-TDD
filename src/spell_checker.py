import requests


def get_response_for(word, get_request=requests.get):
    url = f"http://agilec.cs.uh.edu/spell?check={word}"

    return get_request(url).text


def parse_response(text):
    return text == "true"


def is_spelling_correct(word):
    return parse_response(get_response_for(word))
