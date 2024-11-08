class Graph:
    def __init__(self):
        self.graph = {}
        self.pheromone = {}

    def add_edge(self, u, v, weight):
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []

        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))

        if (u, v) not in self.pheromone:
            self.pheromone[(u, v)] = 1.0
        if (v, u) not in self.pheromone:
            self.pheromone[(v, u)] = 1.0

    def get_neighbors(self, node):
        return self.graph[node]