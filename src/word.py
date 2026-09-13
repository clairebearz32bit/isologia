from __future__ import annotations

import re
import json
import requests
import networkx as nx

from enum import Enum
from dataclasses import dataclass, field


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

    def get_tokens(self):
        # Just uses static text for now to avoid API calls while I write the logic.
        # r = self.get_response()
        r = """{{etymon|en|:inh|enm:ethymologie|tree=1}}\nFrom {{inh|en|enm|ethymologie}}, from {{der|en|fro|ethimologie}}, from {{der|en|la|etymologia}}, from {{der|en|grc|\u1f10\u03c4\u03c5\u03bc\u03bf\u03bb\u03bf\u03b3\u03af\u03b1}}, from {{m|grc|\u1f14\u03c4\u03c5\u03bc\u03bf\u03bd||true sense}} and {{m|grc|-\u03bb\u03bf\u03b3\u03af\u03b1||study or logic of}}, from {{m|grc|\u03bb\u03cc\u03b3\u03bf\u03c2||word; explanation}}. {{surf|en|etymo-|-logy}}."""
        r = re.split(r"[{}\n.]", r)
        for s in r:
            if s not in ("", " ", None):
                yield s

    def parse_etymology(self):
        depth = 0
        nodes = [Node(self.word, depth)]
        tokens = iter(self.get_tokens())

        for token in tokens:
            token = token.lower().split("|")
            print(token)
            parents = []
            node_t = None
            next_token = None

            if "inh" in token:
                node_t = NodeType.INHERITED

            elif "der" in token:
                node_t = NodeType.BORROWED

            # This means this is the 1st parent
            if "tree=1" in token:
                next(tokens)

            if node_t in (NodeType.INHERITED, NodeType.BORROWED):
                token[:] = token[1:]
                word = token[-1]
                language_code = token[1]


                # print(token)

            # if "from" in token:
            #     parent = Node(token, depth)
            #     token = r[i + 1]
            #     i += 1
            #     depth -= 1
            #     nodes.append(Node(token, depth, [parent]))
            #
            # elif "and" in token:
            #     depth -= 2
            #     parent1 = Node(r[i - 1], depth)
            #     parent2 = Node(r[i + 1], depth)
            #     parents.extend([parent1, parent2])
            #
            #     token = r[i - 2]
            #     nodes.append(Node(token, depth + 1, parents))
            #
            #     i += 1

        return nodes

    def create_graph(self, word):
        G = nx.MultiDiGraph()


@dataclass
class Node:
    word: str
    depth: int
    parents: list[Node] = field(default=None)

# Wiktionary differentiates 'inherited' words-which are essentially native words-and 'borrowed' words.
# inh denotes inherited, der denotes borrowed. idk what m| means yet.
class NodeType(Enum):
    INHERITED = 0
    BORROWED = 1
    SURFACE = 2