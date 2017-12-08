import numpy as np
from state import State

class Graph:
    # Define       : epsilon is e
    TYPE_START = "start"
    TYPE_STOP  = "stop"
    TYPE_SIMPLE = "simple"

    def __init__(self):
        self.s = State(0,0)

        self.n_F = 0
        self.F = []

        self.n_states = 0
        self.states = []
        self.dict_states = {}

    def combine_final_states_into_one(self):
        new_state = self.add_state(-1, self.TYPE_STOP)

        for final_idx in range(self.n_F):
            self.F[final_idx].add_edge(new_state, "e")
            self.F[final_idx].change_state_to_simple()

        self.F[0] = new_state
        self.n_F = 1

    def add_state(self, name, type):
        if (name in self.dict_states):
            temp = self.dict_states[name]

            if (temp.position[1] == -1 and type != self.TYPE_STOP):
                temp.position[1] = self.n_F
                self.n_F += 1
                if (self.n_F > len(self.F)):
                    self.F.append(temp)
                else:
                    self.F[self.n_F - 1] = temp
            elif (temp.position[2] == -1 and type != self.TYPE_START):
                temp.position[2] = 0
                self.s = temp
            return temp

        if (type == self.TYPE_START):
            temp = State(name, (self.n_states, -1, ))
            self.dict_states[name]  = temp
            self.s = temp
        elif (type == self.TYPE_STOP):
            temp = State(name, (self.n_states, self.n_F))
            self.dict_states[name] = temp

            self.n_F += 1
            if (self.n_F > len(self.F)):
                self.F.append(temp)
            else:
                self.F[self.n_F  - 1] = temp

        self.n_states += 1
        if (self.n_states > len(self.states)):
            self.states.append(temp)
        else:
            self.states[self.n_states - 1] = temp

        return temp

    def remove_state(self, state):
        self.states[state.position[0]] = self.states[self.n_states - 1]
        self.n_states -= 1

        if (state.type == self.TYPE_START):
            self.s = None
        elif (state.type == self.TYPE_STOP):
            self.F[state.position[1]] = self.F[self.n_F - 1]
            self.n_F -= 1

        self.dict_states.pop(state.name)

        state.removed()

    def read_nfa_from_text(self, path):
        # Line 2       : s  # s: Starting state
        # Line 3       : F  # F: List final states
        # Line 4 -> end: i j u # Has a path from state i -> state j by edge u
        # Define       : epsilon is e

        with open(path) as file:
            lines = file.readlines()

        self.s = self.add_state(name=int(lines[0].rstrip('\n')), type=self.TYPE_START)
        self.F = [self.add_state(name=int(x), type=self.TYPE_STOP) for x in lines[1].rstrip('\n').split()]

        for index in range(3,len(lines)):
            i, u, j = lines[index].rstrip('\n').split()
            state_i = self.add_state(i, self.TYPE_SIMPLE)
            state_j = self.add_state(j, self.TYPE_SIMPLE)
            state_i.add_edge(u, state_j)

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
        self.s = self.add_state(name=int(lines[1].rstrip('\n')), type=self.TYPE_START)
        self.F = [self.add_state(name=int(x), type=self.TYPE_STOP) for x in lines[2].rstrip('\n').split()]

        for index in range(3,len(lines)):
            edge = lines[index].rstrip('\n').split()
            i = index - 3
            for j, u in enumerate(edge):
                state_i = self.add_state(i, self.TYPE_SIMPLE)
                state_j = self.add_state(j, self.TYPE_SIMPLE)
                state_i.add_edge(u, state_j)

    def dfs_from_state(self, state:State, checked):
        checked[state.position[0]] = True

        for next_state, label, _ in state.edges:
            if (checked[next_state.position[0]] == False):
                self.dfs_from_state(next_state, checked)

    def inv_dfs_from_state(self, state, checked):
        checked[state.position[0]] = True

        for pre_state, w, _ in state.inv_edges:
            if (checked[pre_state.position[0]] == False):
                self.dfs_from_state(pre_state, checked)

    def remove_state_cant_come_states(self):
        kt = [False] * self.n_states
        self.dfs_from_state(self.s, kt)

        for idx in range(0, self.n_states):
            if (kt[idx] == False):
                self.remove_state(self.states[idx])

    def remove_state_cant_come_ending_state(self):
        kt = [False] * self.n_states
        for final_idx in range(self.n_F):
            self.inv_dfs_from_state(self.F[final_idx], kt)

        for idx in range(0, self.n_states):
            if kt[idx] == False:
                self.remove_state(self.states[idx])

    def to_regular_expression(self):
        pass

    def to_nfa(self):
        pass

    def to_dfa(self):
        pass



