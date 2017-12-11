class Edge:
    def __init__(self, state, label, position):
        self.state = state
        self.label = label
        self.position = position
        self.colla_edge = None

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

        # self.edges = [[next_state, label, position of inv edge in next state]..]
        self.inv_edges = []
        self.n_inv_edges = 0

        # self.inv_edges = [[previous_state, label, position of edge in previous state]...]
        self.name = name

        self.position = position

    def change_state_to_simple(self):
        self.position[1] = -1
        self.position[2] = -1

    def add_edge(self, label, next_state):
        self.n_edges += 1
        edge = Edge(next_state, label, self.n_edges)
        inv_edge = Edge(self, label, next_state.n_inv_edges)
        edge.colla_edge = inv_edge
        inv_edge.colla_edge = edge

        self.edges.append(edge)
        next_state.add_inv_edge(inv_edge)

    def add_inv_edge(self, inv_edge):
        self.n_inv_edges += 1
        self.inv_edges.append(inv_edge)

    def swap_edge(self, pos1, pos2):
        temp = self.edges[pos2]
        self.edges[pos2] = self.edges[pos1]
        self.edges[pos1] = temp

        self.edges[pos1].position = pos1
        self.edges[pos2].position = pos2

    def swap_inv_edge(self, pos1, pos2):
        temp = self.inv_edges[pos2]
        self.inv_edges[pos2] = self.inv_edges[pos1]
        self.inv_edges[pos1] = temp

        self.inv_edges[pos1].position = pos1
        self.inv_edges[pos2].position = pos2

    def remove_inv_edge(self, pos):
        self.swap_inv_edge(pos, self.n_inv_edges - 1)
        self.n_inv_edges -= 1
        self.inv_edges[pos][0].edges.pop()

    def remove_edge(self, pos):
        edge = self.edges[pos]
        self.swap_edge(pos, self.n_edges - 1)
        edge.state.remove_inv_edge(edge.colla_edge.position)

        self.n_edges -= 1
        self.edges.pop()

    def removed(self):
        for edge in range(self.n_edges):
            self.remove_edge(0)

        for inv_edge in self.inv_edges.copy():
            inv_edge.state.remove_edge(inv_edge.colla_edge.position)

    def sort_edges_by_next_state(self):
        self.edges = sorted(self.edges, key=lambda x: x.state)
        for idx, edge in self.edges:
            edge.position = idx

    def combine_edge(self, pos1, pos2):
        if (self.edges[pos1].label != self.edges[pos2].label):
            self.edges[pos1].label += "+" + self.edges[pos2].label

    def merge_same_destination_edges(self):
        self.sort_edges_by_next_state()

        will_remove_edge = []
        if (self.n_edges == 0):
            return

        pre_same_edge = 0
        for idx in range(1,self.n_edges):
            if (self.edges[idx].state != self.edges[idx - 1].state):
                pre_same_edge = idx
                continue

            self.combine_edge(pre_same_edge,idx)
            will_remove_edge.append(idx)

        for remove_idx in will_remove_edge[::-1]:
            self.remove_edge(remove_idx)