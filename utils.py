import numpy as np

class Graph:
    def read_nfa_from_text(self, path):
        # Line 1       : n  # n: Number of states
        # Line 2       : s  # s: Starting state
        # Line 3       : F  # F: List final states
        # Line 4 -> end: i j u # Has a path from state i -> state j by edge u

        with open(path) as file:
            lines = file.readlines()

        n = int(lines[0].rstrip('\n'))
        s = int(lines[1].rstrip('\n'))
        F = [int(x) for x in lines[2].rstrip('\n').split()]
        E = [[]] * n

        for index in range(3,len(lines)):
            i, j, u = lines[index].rstrip('\n').split()
            E[int(i)].append((int(j),u))

        return n,s,F,E

    def read_dfa_from_text(self, path):
        # Line 1       : n  # n: Number of states
        # Line 2       : s  # s: Starting state
        # Line 3       : F  # F: List final states
        # Line 4 -> 3+n: Matrix edges
        #   Line i     : jth value: u # Has a path from state i -> state j by edge u

        with open(path) as file:
            lines = file.readlines()

        n = int(lines[0].rstrip('\n'))
        s = int(lines[1].rstrip('\n'))
        F = [int(x) for x in lines[2].rstrip('\n').split()]
        E = [[]] * n

        for index in range(3,len(lines)):
            edge = lines[index].rstrip('\n').split()
            i = index - 3
            for j, u in enumerate(edge):
                E[i].append((j,u))

        return n,s,F,E

