class State:
    def __init__(self, name, position, type):
        self.edges = []
        self.n_edges = 0

        self.inv_edges = []
        self.n_inv_edges = 0
        self.name = name

        self.position = position
        self.type = type

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

        self.edges[pos1][0].n_inv_edges[self.edges[pos1][2]] = pos1
        self.edges[pos2][0].n_inv_edges[self.edges[pos2][2]] = pos2

    def remove_inv_edges(self, pos):
        self.inv_edges[pos] = self.inv_edges[self.n_inv_edges - 1]
        self.n_inv_edges -= 1

    def remove_edge(self, pos):
        self.edges[pos][0].remove_inv_edges(self.edges[pos][2])

        if (pos != self.n_edges - 1):
            self.edges[pos] = self.edges[self.n_edges - 1]
            self.edges[pos][0].n_inv_edges[self.edges[pos][2]] = pos
        self.n_edges -= 1

    def removed(self):
        for edge in self.edges:
            edge[0].remove_inv_edges(edge[2])

        for inv_edge in self.inv_edges:
            inv_edge[0].remove_edge(inv_edge[2])