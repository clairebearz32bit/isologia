import re
import json
import requests
import networkx as nx


class Word:
    def __init__(self, word):
        self.word = word

    """
    WARNING: This function uses API calls to wiktionary, use it sparingly.
    Parse the JSON response and dump it into a file by default. Prepares the etymology to be put into a directed multigraph with networkx.
    """
    def get_etymology(self, dump_json=True):
        URL = "https://en.wiktionary.org/w/api.php?action=parse&page={}&prop=wikitext&format=json&origin=*"
        headers = {"User-Agent": "Isologia/0.0 (https://github.com/clairebearz32bit/isologia)"}

        response = requests.get(URL.format(self.word), headers=headers).json()
        response = response["parse"]["wikitext"]["*"]

        if "===Etymology===" not in response or "==English==" not in response:
            # Maybe add another source here as a fallback?
            # Can maybe add support for other languages later
            raise Exception("This word does not have an English etymology section on Wiktionary.")

        match = re.search(
            r"^==English==\s*\n.*?"
            r"^===Etymology===\s*\n"
            r"(?P<etymology>.*?)"
            r"(?=^={3,6}[^=\n].*?={3,6}\s*$|^==[^=\n].*?==\s*$|\Z)",
            response,
            flags=re.MULTILINE | re.DOTALL,
        )

        t = str.translate("{}", "\n", )
        etymology_text = match.group("etymology").strip().translate(t) if match else None

        if dump_json:
            filepath = "./{}_ETYMOLOGY.json".format(self.word)
            with open(filepath, "w+") as fp:
                json.dump(etymology_text, fp, indent=4)

        return etymology_text

    # Just uses static text for now to avoid API calls while I write the logic.
    def parse_etymology(self):
        # r = self.get_response()
        r = """
        {{etymon|en|:ubor|fr:croissant|tree=1}}
        {{root|en|ine-pro|*ḱer- (grow)}}
        {{ubor|en|fr|croissant||crescent}}, present participle of {{m|fr|croître||to grow}}. {{doublet|en|crescent}}.
        """
        nodes = []

        return nodes

    def create_graph(self, word):
        G = nx.MultiDiGraph()
