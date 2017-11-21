import numpy as np

class Graph:
    # Define       : epsilon is e

    def __init__(self):
        self.n = 0
        self.s = 0
        self.F = []
        self.E = []
        self.inv_E = []
        self.status_states = []

    def combine_final_states_into_one(self):
        if (len(self.F) <= 1):
            return

        f = self.n
        self.n += 1
        self.E.append([])
        self.inv_E.append([])

        for final_state in self.F:
            self.E[final_state].append((f,'e'))
            self.inv_E[f].append((final_state,'e'))

        self.F = [f]

    def _update_status_of_states(self):
        self.status_states = ['n'] * self.n
        self.status_states[self.s] = 's'
        for f in self.F:
            self.status_states[f] = 'f'

    def read_nfa_from_text(self, path):
        # Line 1       : n  # n: Number of states
        # Line 2       : s  # s: Starting state
        # Line 3       : F  # F: List final states
        # Line 4 -> end: i j u # Has a path from state i -> state j by edge u
        # Define       : epsilon is e

        with open(path) as file:
            lines = file.readlines()

        self.n = int(lines[0].rstrip('\n'))
        self.s = int(lines[1].rstrip('\n'))
        self.F = [int(x) for x in lines[2].rstrip('\n').split()]
        self.E = [[]] * self.n
        self.inv_E = [[]] * self.n

        for index in range(3,len(lines)):
            i, j, u = lines[index].rstrip('\n').split()
            self.E[int(i)].append((int(j),u))
            self.inv_E[int(j)].append((int(i),u))

        self._update_status_of_states()
        self.remove_unmeaningful_states()

    def read_dfa_from_text(self, path):
        # Line 1       : n  # n: Number of states
        # Line 2       : s  # s: Starting state
        # Line 3       : F  # F: List final states
        # Line 4 -> 3+n: Matrix edges
        #   Line i     : jth value: u # Has a path from state i -> state j by edge u
        # Define       : epsilon is e

        with open(path) as file:
            lines = file.readlines()

        self.n = int(lines[0].rstrip('\n'))
        self.s = int(lines[1].rstrip('\n'))
        self.F = [int(x) for x in lines[2].rstrip('\n').split()]
        self.E = [[]] * self.n
        self.inv_E = [[]] * self.n

        for index in range(3,len(lines)):
            edge = lines[index].rstrip('\n').split()
            i = index - 3
            for j, u in enumerate(edge):
                self.E[i].append((j,u))
                self.inv_E[j].append((i,u))

        self._update_status_of_states()
        self.remove_unmeaningful_states()

    def dfs_from_state(self, state, checked):
        checked[state] = True
        for next_state, w in self.E[state]:
            if (checked[next_state] == False):
                self.dfs_from_state(next_state, checked)

    def inv_dfs_from_state(self, state, checked):
        checked[state] = True
        for next_state, w in self.inv_E[state]:
            if (checked[next_state] == False):
                self.dfs_from_state(next_state, checked)

    def remove_unmeaningful_states(self):
        kt1 = [False] * self.n
        self.dfs_from_state(self.s, kt1)

        kt2 = [False] * self.n
        for final_state in self.F:
            self.inv_dfs_from_state(final_state, kt2)

        kt = [kt1[i] and kt2[i] for i in range(0, self.n)]

        new_E = [self.E[i] for i in range(0,self.n) if kt[i] or i == self.s]
        self.E = new_E

        new_E = [self.inv_E[i] for i in range(0,self.n) if kt[i] or i == self.s]
        self.inv_E = new_E

        self.F = [i for i in range(0,self.n) if kt[i] or i == self.s]
        self.n = len(self.E)
        self._update_status_of_states()




