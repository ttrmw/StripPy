import requests
import xml.etree.ElementTree as ET

MERRIAM_KEY = "d0d90723-3851-4c65-8c04-dea85de4051f"


def dict_lookup(word):
    """returns dictionary definitions from merriam webster for given word"""
    def get_def(query):

        url_build = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/"
        url_build += query
        url_build += "?key="
        url_build += MERRIAM_KEY

        return requests.get(url_build).text.encode("utf-8")

    try:
        response = ET.fromstring(get_def(word))
    except requests.ConnectionError:
        return "Unable to connect!"

    def try_strip(input_word, strip_chars):
        #attempt strip, if it fails (on an empty string), return the input.
        try:
            return input_word.strip(strip_chars)
        except AttributeError:
            return input_word

    definitions = [try_strip(definition.text, ": ") for definition in response.iter("dt")]

    return filter(None, definitions)

if __name__ == "__main__":
    import sys
    for i in sys.argv[1:]:
        for x in dict_lookup(i)[:]:
            print x
