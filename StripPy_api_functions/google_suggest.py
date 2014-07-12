import requests
import json


def google_suggest(word):
    """returns suggested queries from Google API. Works quite well as a spellchecker"""

    def make_request(query):
        url_build = "http://suggestqueries.google.com/complete/search?client=chrome&q="
        url_build += query

        return requests.get(url_build).text.encode("utf-8")

    json_response = json.loads(make_request(word))

    return [suggestion.encode("utf-8") for suggestion in json_response[1]]

if __name__ == "__main__":
    import sys
    for arg in sys.argv[1:]:
        suggestions = google_suggest(arg)
        for word in suggestions:
            print word