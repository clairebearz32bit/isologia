import requests


class Word:
    def __init__(self, word):
        URL = "https://en.wiktionary.org/w/api.php?action=parse&page={}&prop=wikitext&format=json&origin=*"
        headers = {"User-Agent": "Isologia/0.0 (https://github.com/clairebearz32bit/isologia)"}

        response = requests.get(URL.format(word), headers=headers).json()

        if "===Etymology===" not in response:
            # Maybe add another source here as a fallback?
            raise Exception("This word does not have an etymology section on Wiktionary.")

        self.etymology = response
        print(self.etymology)

    def parse_response(self):
