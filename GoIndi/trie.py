"""
A fast data structure for searching strings with autocomplete support.
"""
class CityNode:
    def __init__(self,city,state,priority):
        self.city = city
        self.state = state
        self.priority=priority



class Trie(object):
    def __init__(self):
        self.children = {}
        self.flag = False # Flag to represent that a word ends at this node

    def add(self, char):
        self.children[char] = Trie()

    def insert(self, word):
        node = self
        for char in word:
            if char not in node.children:
                node.add(char)
            node = node.children[char]
        node.flag = True
        #node.fieldValue=CityNode(word,state,priority)

    def contains(self, word):
        node = self
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.fieldValue

    def all_suffixes(self, prefix):
        results = set()
        if self.flag:
            results.add(prefix)
        if not self.children: return results
        return reduce(lambda a, b: a | b, [node.all_suffixes(prefix + char) for (char, node) in self.children.items()]) | results

    def autocomplete(self, prefix):
        node = self
        for char in prefix:
            if char not in node.children:
                return set()
            node = node.children[char]
        return list(node.all_suffixes(prefix))


TRIE = Trie()

def read():
    f = open("/home/ankur/citylist.txt", "r")
    line = f.read().splitlines()
    f.close()
    return line

def initialize():
    lines = read()
    for line in lines:
        TRIE.insert(line.title())
