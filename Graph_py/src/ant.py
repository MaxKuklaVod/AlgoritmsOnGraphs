import random

class Ant:
    def __init__(self, start_node):
        self.start_node = start_node
        self.path = [start_node]
        self.total_cost = 0

    def move(self, graph, alpha, beta):
        current_node = self.path[-1]
        neighbors = graph.get_neighbors(current_node)

        probabilities = []
        for neighbor, weight in neighbors:
            pheromone = graph.pheromone.get((current_node, neighbor), 1.0)
            probability = (pheromone ** alpha) * ((1 / weight) ** beta)
            probabilities.append(probability)

        total = sum(probabilities)
        probabilities = [p / total for p in probabilities]

        next_node = random.choices([neighbor for neighbor, _ in neighbors], weights=probabilities)[0]
        next_cost = dict(neighbors)[next_node]

        self.path.append(next_node)
        self.total_cost += next_cost