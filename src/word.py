import re
import json
import requests
import networkx as nx

from dataclasses import dataclass

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
        if not match:
            return None

        etymology = match.group("etymology").strip()

        if dump_json:
            filepath = "./{}_ETYMOLOGY.json".format(self.word)
            with open(filepath, "w+") as fp:
                json.dump(etymology, fp, indent=4)

        return etymology

    # Just uses static text for now to avoid API calls while I write the logic.
    def parse_etymology(self):
        # r = self.get_response()
        r = """{{etymon|en|:inh|enm:ethymologie|tree=1}}\nFrom {{inh|en|enm|ethymologie}}, from {{der|en|fro|ethimologie}}, from {{der|en|la|etymologia}}, from {{der|en|grc|\u1f10\u03c4\u03c5\u03bc\u03bf\u03bb\u03bf\u03b3\u03af\u03b1}}, from {{m|grc|\u1f14\u03c4\u03c5\u03bc\u03bf\u03bd||true sense}} and {{m|grc|-\u03bb\u03bf\u03b3\u03af\u03b1||study or logic of}}, from {{m|grc|\u03bb\u03cc\u03b3\u03bf\u03c2||word; explanation}}. {{surf|en|etymo-|-logy}}."""
        r = re.split(r"[{}\n]", r)
        r[:] = [s for s in r if s not in ("")]

        print(r)

        nodes = []

        return nodes

    def create_graph(self, word):
        G = nx.MultiDiGraph()


@dataclass
class Node:
    word: str
    depth: int
