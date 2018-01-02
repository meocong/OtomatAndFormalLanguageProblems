from graph import Graph

class Automat:
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

    def nfaToDfa(self, path):
        self.graph.read_nfa_from_text(path)
        self.graph.to_dfa()

    def nfaToGp(self, path):
        self.graph.read_nfa_from_text(path)
        self.graph.to_Gp()
        print("V = ", self.graph.V)
        print("T = ", self.graph.char)
        print("P = ", self.graph.P)

    def dfaToGp(self, path):
        self.graph.read_dfa_from_text(path)
        self.graph.to_Gp()
        print("V = ", self.graph.V)
        print("T = ", self.graph.char)
        print("P = ", self.graph.P)

    def nfaToGt(self, path):
        self.graph.read_nfa_from_text(path)
        self.graph.to_Gt()
        print("S = S")
        print("V = ", self.graph.V)
        print("T = ", self.graph.char)
        print("P = ", self.graph.P)

    def dfaToGt(self, path):
        self.graph.read_dfa_from_text(path)
        self.graph.to_Gt()
        print("S = S")
        print("V = ", self.graph.V)
        print("T = ", self.graph.char)
        print("P = ", self.graph.P)

    def GpToNfa(self):
        pass

    def GpToDfa(self):
        pass

    def reToNfa(self):
        pass

    def reToDfa(self):
        pass

    def reToGp(self):
        pass

    def reToGt(self):
        pass

    def GpToRe(self):
        pass

    def GtToRe(self):
        pass

test = Automat()
# test.dfaToRe("dfa.txt")
# test.dfaToRe("dfa.txt")
# test.nfaToGp("nfa.txt")
# test.nfaToGt("nfa.txt")
# test.dfaToGp("dfa.txt")
# test.dfaToGt("dfa.txt")