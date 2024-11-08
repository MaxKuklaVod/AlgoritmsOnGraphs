from src.ant import Ant
from matplotlib.animation import FuncAnimation

import matplotlib.pyplot as plt
import networkx as nx

class AntColonyOptimizer:
    def __init__(self, graph, num_ants, alpha=1.0, beta=2.0, evaporation_rate=0.5, iterations=100):
        self.graph = graph
        self.num_ants = num_ants
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.iterations = iterations
        self.best_path = None
        self.best_cost = float('inf')

    def optimize_iteration(self, start, end):
        ants = [Ant(start) for _ in range(self.num_ants)]

        for ant in ants:
            while ant.path[-1] != end:
                ant.move(self.graph, self.alpha, self.beta)

            if ant.total_cost < self.best_cost:
                self.best_cost = ant.total_cost
                self.best_path = ant.path

            self.update_pheromone(ant)

        self.evaporate_pheromone()

    def update_pheromone(self, ant):
        for i in range(len(ant.path) - 1):
            u = ant.path[i]
            v = ant.path[i + 1]

            if (u, v) not in self.graph.pheromone:
                self.graph.pheromone[(u, v)] = 1.0
            if (v, u) not in self.graph.pheromone:
                self.graph.pheromone[(v, u)] = 1.0

            self.graph.pheromone[(u, v)] += 1.0 / ant.total_cost
            self.graph.pheromone[(v, u)] += 1.0 / ant.total_cost

    def evaporate_pheromone(self):
        for edge in self.graph.pheromone:
            self.graph.pheromone[edge] *= (1 - self.evaporation_rate)

    def visualize(self, ax, sm=None):
        ax.clear()
        G = nx.Graph()
        for node in self.graph.graph:
            G.add_node(node)

        # Добавляем рёбра с весами и феромонами
        for (u, v), pheromone in self.graph.pheromone.items():
            weight = dict(self.graph.get_neighbors(u))[v]
            G.add_edge(u, v, weight=weight, pheromone=pheromone)

        # Позиционируем узлы для отображения
        pos = nx.spring_layout(G)

        # Рисуем узлы и подписи к ним
        nx.draw_networkx_nodes(G, pos, ax=ax, node_size=500, node_color="lightblue")
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_color="black")

        # Рисуем рёбра с феромонами (цвет и толщина зависят от количества феромонов)
        edges = G.edges(data=True)
        edge_colors = [data['pheromone'] for _, _, data in edges]
        edge_widths = [0.1 + 4 * (data['pheromone'] / max(edge_colors)) for _, _, data in edges]

        nx.draw_networkx_edges(G, pos, ax=ax, width=edge_widths, edge_color=edge_colors, edge_cmap=plt.cm.Blues)

        # Отображаем лучший путь, если он найден
        if self.best_path:
            path_edges = [(self.best_path[i], self.best_path[i + 1]) for i in range(len(self.best_path) - 1)]
            nx.draw_networkx_edges(G, pos, ax=ax, edgelist=path_edges, edge_color="red", width=2.5)

        ax.set_title(f"Best Cost: {self.best_cost}")

        # Обновляем или создаём цветовую шкалу
        if sm is not None:
            sm.set_array(edge_colors)
        else:
            sm = plt.cm.ScalarMappable(cmap=plt.cm.Blues)
            sm.set_array(edge_colors)
            self.colorbar = plt.colorbar(sm, ax=ax, label="Pheromone Level")
        
        return sm

    def run_animation(self, start, end):
        fig, ax = plt.subplots(figsize=(8, 6))
        sm = None  # Инициализируем объект ScalarMappable

        def update(frame):
            self.optimize_iteration(start, end)
            nonlocal sm
            sm = self.visualize(ax, sm)

        anim = FuncAnimation(fig, update, frames=self.iterations, repeat=False)
        plt.show()
