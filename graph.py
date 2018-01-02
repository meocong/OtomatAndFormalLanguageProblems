import numpy as np
from state import State
from regular_expression import star_state

class Graph:
    # Define       : epsilon is e
    TYPE_START = "start"
    TYPE_STOP  = "stop"
    TYPE_SIMPLE = "simple"

    TYPE_DFA = "dfa"
    TYPE_NFA = "nfa"
    TYPE_RE  = "re"

    def __init__(self):
        self.s = State(0,0)

        self.n_F = 0
        self.F = []

        self.n_states = 0
        self.states = []
        self.dict_states = {}
        self.re = None
        self.type = None
        self.char = []

    def combine_final_states_into_one(self):
        new_state = self.add_state(-1, self.TYPE_STOP)

        for final_idx in range(self.n_F - 1):
            self.F[final_idx].add_edge("e", new_state)
            # print(self.F[final_idx].name, self.F[final_idx].position)
            self.F[final_idx].change_state_to_not_stop()
            # print(self.F[final_idx].name, self.F[final_idx].position)
        self.F = [new_state]
        new_state.position = (new_state.position[0],0,-1)
        self.n_F = 1

    def add_new_start_states(self):
        previous_s = self.s
        new_state = self.add_state(-2, self.TYPE_START)

        new_state.add_edge("e", previous_s)
        previous_s.change_state_to_not_start()

    def add_state(self, name, type):
        temp = None
        name = int(name)

        if (name in self.dict_states):
            temp = self.dict_states[name]

            if (temp.is_stop() == False and type == self.TYPE_STOP):
                temp.position[1] = self.n_F
                self.n_F += 1
                self.F.append(temp)
            elif (temp.is_start() == False and type == self.TYPE_START):
                temp.position[2] = 0
                self.s = temp
            return temp

        if (type == self.TYPE_START):
            temp = State(name, (self.n_states, -1, 0))
            self.s = temp
        elif (type == self.TYPE_STOP):
            temp = State(name, (self.n_states, self.n_F, -1))
            self.n_F += 1
            self.F.append(temp)
        else:
            temp = State(name, (self.n_states, -1, -1))

        self.n_states += 1
        self.dict_states[name] = temp
        self.states.append(temp)

        return temp

    def remove_state(self, state, join_edge = False):
        if (state.is_start()):
            self.s = None
        if (state.is_stop()):
            self.F[state.position[1]] = self.F[self.n_F - 1]
            self.F.pop()
            self.n_F -= 1
        self.states[state.position[0]] = self.states[self.n_states - 1]
        self.states[state.position[0]].position = state.position

        self.n_states -= 1
        self.states.pop()

        self.dict_states.pop(state.name)

        state.removed(join_edge)

    def swap_state(self, state1:State, state2:State):
        self.states[state1.position[0]] = state2
        self.states[state2.position[0]] = state1

        temp = state1.position
        state1.position = (state2.position[0], temp[1], temp[2])
        state2.position = (temp[0], state2.position[1], state2.position[2])

    def read_nfa_from_text(self, path):
        # Line 2       : s  # s: Starting state
        # Line 3       : F  # F: List final states
        # Line 4 -> end: i j u # Has a path from state i -> state j by edge u
        # Define       : epsilon is e
        self.__init__()

        with open(path) as file:
            lines = file.readlines()

        self.s = self.add_state(name=lines[0].rstrip('\n'), type=self.TYPE_START)
        self.F = [self.add_state(name=x, type=self.TYPE_STOP) for x in lines[1].rstrip('\n').split()]
        self.char = lines[2].rstrip('\n').split()

        for index in range(3,len(lines)):
            i, u, j = lines[index].rstrip('\n').split()
            state_i = self.add_state(i, self.TYPE_SIMPLE)
            state_j = self.add_state(j, self.TYPE_SIMPLE)
            state_i.add_edge(u, state_j)

        self.type = self.TYPE_NFA

    def read_dfa_from_text(self, path):
        # Line 1       : n  # n: Number of states
        # Line 2       : s  # s: Starting state
        # Line 3       : F  # F: List final states
        # Line 4 -> 3+n: Matrix edges
        #   Line i     : jth value: u # Has a path from state i -> state j by edge u
        # Define       : epsilon is e
        self.__init__()

        with open(path) as file:
            lines = file.readlines()

        self.n = int(lines[0].rstrip('\n'))
        self.s = self.add_state(name=lines[1].rstrip('\n'), type=self.TYPE_START)
        self.F = [self.add_state(name=x, type=self.TYPE_STOP) for x in lines[2].rstrip('\n').split()]
        self.char = lines[3].rstrip('\n').split()

        for index in range(4,4+self.n):
            edge = lines[index].rstrip('\n').split()
            i = index - 4

            for u, j in enumerate(edge):
                state_i = self.add_state(i, self.TYPE_SIMPLE)
                state_j = self.add_state(j, self.TYPE_SIMPLE)
                state_i.add_edge(self.char[u], state_j)

        self.type = self.TYPE_DFA

    def dfs_from_state(self, state:State, checked):
        checked[state.position[0]] = True
        for edge in state.edges:
            if (checked[edge.state.position[0]] == False):
                self.dfs_from_state(edge.state, checked)

    def inv_dfs_from_state(self, state, checked):
        checked[state.position[0]] = True

        for inv_edge in state.inv_edges:
            if (checked[inv_edge.state.position[0]] == False):
                self.inv_dfs_from_state(inv_edge.state, checked)

    def remove_state_cant_come_states(self):
        kt = [False] * self.n_states
        self.dfs_from_state(self.s, kt)

        for idx in range(self.n_states - 1, -1, -1):
            if (kt[idx] == False):
                self.remove_state(self.states[idx])

    def remove_state_cant_come_ending_state(self):
        kt = [False] * self.n_states
        for final_state in self.F:
            self.inv_dfs_from_state(final_state, kt)

        for idx in range(self.n_states - 1, -1, -1):
            if kt[idx] == False:
                self.remove_state(self.states[idx])

    def plot(self):
        for state in self.states:
            print("xxx",state.name, state.self_edge, state.position)
            for x in state.edges:
                print("edge",x.state.name, x.label)
            for x in state.inv_edges:
                print("inve",x.state.name, x.label)

    def to_regular_expression(self):
        if (self.type == self.TYPE_RE):
            return
        else:
            self.add_new_start_states()
            self.combine_final_states_into_one()

            self.remove_state_cant_come_states()
            if (len(self.F) == 0):
                self.re = ""
                return

            self.remove_state_cant_come_ending_state()
            if (self.s == None):
                self.re = ""
                return

            # self.plot()
            self.swap_state(self.states[0], self.s)
            self.swap_state(self.states[1], self.F[0])

            for i in range(self.n_states - 1,1,-1):
                for state in self.states:
                    state.merge_same_destination_edges()
                # print(i, self.states[i].name, self.states[i].position)
                self.remove_state(self.states[i], join_edge = True)

                # for x in self.states:
                    # print("uuu", x.name, x.self_edge)
                    # for edge in x.edges:
                    #     print("  u", edge.label, edge.state.name)
            self.s.merge_same_destination_edges()
            self.re = self.s.edges[0].label

        self.type = self.TYPE_RE

    def to_nfa(self):
        if (self.type == self.TYPE_RE):
            pass

    def remove_all_epsilon_edge(self):
        pass

    def to_dfa(self):
        if (self.type == self.TYPE_RE):
            self.to_nfa()

        if (self.type != self.TYPE_DFA):
            self.remove_all_epsilon_edge()

            stack = self.states.copy()
            # self.char = np.unique([edge.label])
            while len(stack) > 0:
                state = stack.pop()
                state.sort_edges_by_next_label()

    def to_Gp(self):
        self.to_nfa()

        for state in self.states:
            if (state.is_start()):
                state.v = "S"
            else:
                state.v = chr(int(state.name) + 66)

        self.V = [state.v for state in self.states]
        self.T = self.char

        self.P = []
        for state in self.states:
            if (state.self_edge != "e"):
                for char in state.self_edge.split("+"):
                    self.P.append(state.v + "->" + char + state.v)
                    if (state.is_stop()):
                        self.P.append(state.v + "->" + char)
            for edge in state.edges:
                if (edge.state.is_stop()):
                    self.P.append(state.v + "->" + edge.label)
                self.P.append(state.v + "->" + edge.label + edge.state.v)

    def reversed(self):
        self.combine_final_states_into_one()
        temp = self.states.copy()
        self.__init__()

        for state in temp:
            if (state.is_start()):
                new_state = self.add_state(state.name, self.TYPE_STOP)
            elif (state.is_stop()):
                new_state = self.add_state(state.name, self.TYPE_START)
            else:
                new_state = self.add_state(state.name, self.TYPE_SIMPLE)

            for inv_edge in state.inv_edges:
                if (inv_edge.state.is_start()):
                    new_re_state = self.add_state(inv_edge.state.name, self.TYPE_STOP)
                elif (inv_edge.state.is_stop()):
                    new_re_state = self.add_state(inv_edge.state.name, self.TYPE_START)
                else:
                    new_re_state = self.add_state(inv_edge.state.name, self.TYPE_SIMPLE)

                new_state.add_edge(inv_edge.label, new_re_state)

    def to_Gt(self):
        self.to_nfa()
        self.reversed()

        for state in self.states:
            if (state.is_start()):
                state.v = "S"
            else:
                state.v = chr(int(state.name) + 66)

        self.V = [state.v for state in self.states]
        self.T = self.char

        self.P = []
        for state in self.states:
            if (state.self_edge != "e"):
                for char in state.self_edge.split("+"):
                    self.P.append(state.v + "->" + state.v + char)
                    if (state.is_stop()):
                        self.P.append(state.v + "->" + char)
            for edge in state.edges:
                if (edge.state.is_stop()):
                    self.P.append(state.v + "->" + edge.label)
                self.P.append(state.v + "->" + edge.state.v + edge.label)


