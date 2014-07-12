import requests
import xml.etree.ElementTree as ET

MERRIAM_KEY = "d0d90723-3851-4c65-8c04-dea85de4051f"


def dict_lookup(mail):

    def get_def(word):

        url_build = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/"
        url_build += word
        url_build += "?key="
        url_build += MERRIAM_KEY

        return requests.get(url_build).text.encode("utf-8")

    response = ET.fromstring(get_def(mail))

    definitions = filter(None, [definition.text for definition in response.iter("dt")])
    definitions = [definition.strip(": ") for definition in definitions]

    print response
    return definitions

if __name__ == "__main__":
    import sys
    for i in sys.argv[1:]:
        for x in dict_lookup(i):
            print x
