from graph import Graph

class DfaNfaToRe:
    def __init__(self):
        self.graph = Graph()

    def dfaToRe(self, path):
        self.graph.read_dfa_from_text(path)
        self.graph.to_regular_expression()
        print("Regular expression: ", self.graph.re)

    def nfaToRe(self, path):
        self.graph.read_nfa_from_text(path)
        self.graph.to_regular_expression()
        print("Regular expression: ", self.graph.re)

    def dfaToNfa(self, path):
        pass


test = DfaNfaToRe()
test.dfaToRe("dfa.txt")
test.nfaToRe("nfa.txt")