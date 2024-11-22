from src.ant import Ant  # Импорт класса муравья
from matplotlib.animation import FuncAnimation  # Для анимации
import matplotlib.pyplot as plt  # Для визуализации
import networkx as nx  # Для работы с графами


class AntColonyOptimizer:
    def __init__(
        self, graph, num_ants, alpha=1.0, beta=2.0, evaporation_rate=0.5, iterations=100
    ):
        """
        Инициализирует алгоритм муравьиной колонии.

        Параметры:
        graph (Graph): Граф, по которому будут перемещаться муравьи.
        num_ants (int): Количество муравьев.
        alpha (float): Влияние уровня феромонов на выбор пути.
        beta (float): Влияние расстояния на выбор пути.
        evaporation_rate (float): Скорость испарения феромонов (0 < evaporation_rate < 1).
        iterations (int): Количество итераций алгоритма.

        Атрибуты:
        best_path (list): Лучший найденный путь.
        best_cost (float): Стоимость (длина) лучшего пути.
        """
        self.graph = graph
        self.num_ants = num_ants
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.iterations = iterations
        self.best_path = None
        self.best_cost = float("inf")  # Начальная стоимость задается как бесконечность

    def optimize_iteration(self, start, end):
        """
        Выполняет одну итерацию алгоритма: перемещение муравьев, обновление феромонов.

        Параметры:
        start (int/str): Стартовый узел.
        end (int/str): Конечный узел.
        """
        # Создаем муравьев, каждый начинает путь с узла start
        ants = [Ant(start) for _ in range(self.num_ants)]

        for ant in ants:
            # Пока муравей не достиг конечного узла, он перемещается
            while ant.path[-1] != end:
                ant.move(self.graph, self.alpha, self.beta)

            # Проверяем, является ли маршрут этого муравья лучшим
            if ant.total_cost < self.best_cost:
                self.best_cost = ant.total_cost
                self.best_path = ant.path

            # Обновляем феромоны по маршруту муравья
            self.update_pheromone(ant)

        # Испаряем феромоны, чтобы избежать их чрезмерного накопления
        self.evaporate_pheromone()
        print(
            f"Текущая лучшая длина {self.best_cost}"
        )  # Выводим текущую лучшую стоимость

    def update_pheromone(self, ant):
        """
        Добавляет феромоны на маршруте, пройденном муравьем.

        Параметры:
        ant (Ant): Объект муравья, для которого обновляются феромоны.
        """
        for i in range(len(ant.path) - 1):
            u = ant.path[i]
            v = ant.path[i + 1]

            # Убедимся, что ребро присутствует в словаре феромонов
            if (u, v) not in self.graph.pheromone:
                self.graph.pheromone[(u, v)] = 1.0
            # Для семмитричного графа
            # if (v, u) not in self.graph.pheromone:
            #     self.graph.pheromone[(v, u)] = 1.0

            # Увеличиваем уровень феромонов, пропорционально обратной стоимости маршрута
            self.graph.pheromone[(u, v)] += 1.0 / ant.total_cost
            # self.graph.pheromone[(v, u)] += 1.0 / ant.total_cost  # Для симметричных графов

    def evaporate_pheromone(self):
        """
        Испаряет часть феромонов на всех ребрах графа, уменьшая их уровни.
        """
        for edge in self.graph.pheromone:
            # Уменьшаем уровень феромонов на ребре с учетом коэффициента испарения
            self.graph.pheromone[edge] *= 1 - self.evaporation_rate

    def visualize(self, ax, sm=None):
        """
        Визуализирует текущий граф с уровнями феромонов.

        Параметры:
        ax (matplotlib.axes.Axes): Объект осей для отрисовки.
        sm (ScalarMappable): Объект для цветовой шкалы (может быть None).

        Возвращает:
        sm (ScalarMappable): Обновленный объект цветовой шкалы.
        """
        ax.clear()  # Очищаем предыдущую отрисовку
        G = nx.Graph()

        # Добавляем узлы
        for node in self.graph.graph:
            G.add_node(node)

        # Добавляем рёбра с весами и уровнями феромонов
        for (u, v), pheromone in self.graph.pheromone.items():
            weight = dict(self.graph.get_neighbors(u))[v]  # Получаем вес ребра
            G.add_edge(u, v, weight=weight, pheromone=pheromone)

        # Генерируем позиции узлов для визуализации
        pos = nx.spring_layout(G)

        # Рисуем узлы
        nx.draw_networkx_nodes(G, pos, ax=ax, node_size=500, node_color="lightblue")
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_color="black")

        # Рисуем рёбра, толщину и цвет которых определяет уровень феромонов
        edges = G.edges(data=True)
        edge_colors = [data["pheromone"] for _, _, data in edges]
        edge_widths = [
            0.1 + 4 * (data["pheromone"] / max(edge_colors)) for _, _, data in edges
        ]

        nx.draw_networkx_edges(
            G,
            pos,
            ax=ax,
            width=edge_widths,
            edge_color=edge_colors,
            edge_cmap=plt.cm.Blues,
        )

        # Отображаем лучший путь красным
        if self.best_path:
            path_edges = [
                (self.best_path[i], self.best_path[i + 1])
                for i in range(len(self.best_path) - 1)
            ]
            nx.draw_networkx_edges(
                G, pos, ax=ax, edgelist=path_edges, edge_color="red", width=2.5
            )

        ax.set_title(f"Best Cost: {self.best_cost}")

        # Обновляем или создаем цветовую шкалу
        if sm is not None:
            sm.set_array(edge_colors)
        else:
            sm = plt.cm.ScalarMappable(cmap=plt.cm.Blues)
            sm.set_array(edge_colors)
            self.colorbar = plt.colorbar(sm, ax=ax, label="Pheromone Level")

        return sm

    def run_animation(self, start, end):
        """
        Запускает анимацию работы алгоритма.

        Параметры:
        start (int/str): Стартовый узел.
        end (int/str): Конечный узел.
        """
        fig, ax = plt.subplots(figsize=(8, 6))  # Создаем фигуру для визуализации
        sm = None  # Инициализируем цветовую шкалу

        def update(frame):
            # Обновляем состояние графа на каждой итерации
            self.optimize_iteration(start, end)
            nonlocal sm
            sm = self.visualize(ax, sm)

        # Создаем анимацию
        anim = FuncAnimation(fig, update, frames=self.iterations, repeat=False)
        plt.show()  # Показываем анимацию
