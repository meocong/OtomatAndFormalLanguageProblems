class State:
    TYPE_START = "start"
    TYPE_STOP = "stop"
    TYPE_SIMPLE = "simple"

    def __init__(self, name, position):
        # position = (x,y,z)
        # x: position of state in states list
        # y: position of state in ending states list
        # z: = -1 if state is not starting state otherwise it's
        self.edges = []
        self.n_edges = 0

        # self.edges = [(next_state, label, position of inv edge in next state)]
        self.inv_edges = []
        self.n_inv_edges = 0

        # self.inv_edges = [(previous_state, label, position of edge in previous state)]
        self.name = name

        self.position = position

    def change_state_to_simple(self):
        self.position[1] = -1
        self.position[2] = -1

    def add_edge(self, label, next_state):
        self.n_edges += 1
        if (self.n_edges > len(self.edges)):
            self.edges.append((next_state, label, next_state.n_inv_edges))
        else:
            self.edges[self.n_edges-1] = (next_state, label, next_state.n_inv_edges)

        next_state.add_inv_edge(label, self)

    def add_inv_edge(self, char, pre_state):
        self.n_inv_edges += 1
        if self.n_inv_edges > len(self.edges):
            self.inv_edges.append((pre_state, char, pre_state.n_edges - 1))
        else:
            self.inv_edges[self.n_inv_edges - 1] = (pre_state, char, pre_state.n_edges - 1)

    def swap_edge(self, pos1, pos2):
        temp = self.edges[pos2]
        self.edges[pos2] = self.edges[pos1]
        self.edges[pos1] = temp

        self.edges[pos1][0].inv_edges[self.edges[pos1][2]][2] = pos2
        self.edges[pos2][0].inv_edges[self.edges[pos2][2]][2] = pos1

    def swap_inv_edge(self, pos1, pos2):
        temp = self.inv_edges[pos2]
        self.inv_edges[pos2] = self.inv_edges[pos1]
        self.inv_edges[pos1] = temp

        self.inv_edges[pos1][0].edges[self.inv_edges[pos1][2]][2] = pos2
        self.inv_edges[pos2][0].edges[self.inv_edges[pos2][2]][2] = pos1

    def remove_inv_edge(self, pos):
        self.swap_inv_edge(pos, self.n_inv_edges - 1)
        self.inv_edges[pos][0].swap_edges(self.inv_edges[pos][2], self.inv_edges[pos][0].n_edges - 1)

        self.n_inv_edges -= 1
        self.inv_edges[pos][0].n_edges -= 1

    def remove_edge(self, pos):
        self.swap_edge(pos, self.n_edges - 1)
        self.edges[pos][0].swap_inv_edges(self.edges[pos][2], self.edges[pos][0].n_inv_edges - 1)

        self.n_edges -= 1
        self.edges[pos][0].n_inv_edges -= 1

    def removed(self):
        for edge in range(self.n_edges):
            self.remove_edge(0)

        for inv_edge in range(self.n_inv_edges):
            self.remove_inv_edge(0)