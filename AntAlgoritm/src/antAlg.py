import numpy as np
import statistics as st

from src.ant import Ant


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
        self.stack_path = {}
        self.iter_path = {}
        self.pheromons_path = {}
        self.probabilities = {}
        self.probability = []
        self.count = None
        self.iter = 0
        self.pheromone_cost = 0
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
        self.count = 0
        self.iter += 1

        for ant in ants:
            # Пока муравей не достиг конечного узла, он перемещается
            while ant.path[-1] != end:
                flag = ant.move(self.graph, self.alpha, self.beta)

                if flag == True:
                    self.count += 1

                if self.count > len(ants) * 10000:
                    print(
                        f"Нет Гамельтонова цикла, потому что из {start} в {end} нет пути"
                    )
                    exit(0)

            # Проверяем, является ли маршрут этого муравья лучшим
            if ant.total_cost <= self.best_cost:
                self.best_cost = ant.total_cost
                self.best_path = ant.path
                self.best_path_probability()

            # Обновляем феромоны по маршруту муравья
            self.pheromone_cost = self.update_pheromone(ant, self.pheromone_cost)

        self.pheromons_path[self.iter] = self.pheromone_cost

        # Испаряем феромоны, чтобы избежать их чрезмерного накопления
        self.evaporate_pheromone()
        if st.median(self.probability) < 1 - st.median(self.probability):
            self.probabilities[self.iter] = 1 - st.median(self.probability)
        else:
            self.probabilities[self.iter] = st.median(self.probability)

        self.stack_path[self.iter] = self.count
        self.iter_path[self.iter] = self.best_cost

    def update_pheromone(self, ant, pheromone_cost):
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
            pheromone_cost += self.graph.pheromone[(u, v)]
        return pheromone_cost

    def evaporate_pheromone(self):
        """
        Испаряет часть феромонов на всех ребрах графа, уменьшая их уровни.
        """
        for edge in self.graph.pheromone:
            # Уменьшаем уровень феромонов на ребре с учетом коэффициента испарения
            self.graph.pheromone[edge] *= 1 - self.evaporation_rate

    def best_path_probability(self):
        best_path = 0
        self.probability = []
        for i in range(len(self.best_path) - 1):
            probabilities = []
            u = self.best_path[i]
            v = self.best_path[i + 1]
            neighbors = self.graph.get_neighbors(u)
            for neighbor, weight in neighbors:
                if neighbor != v:
                    # Уровень феромонов на ребре (current_node, neighbor)
                    pheromone = self.graph.pheromone.get((u, neighbor), 1.0)
                    # Вычисляем вероятность выбора этого соседа:
                    # - pheromone ** alpha: роль феромонов
                    # - (1 / weight) ** beta: роль обратного расстояния (чем меньше расстояние, тем лучше)
                    probability = (pheromone**self.alpha) * ((1 / weight) ** self.beta)
                    probabilities.append(probability)
                else:
                    pheromone = self.graph.pheromone.get((u, neighbor), 1.0)
                    # Вычисляем вероятность выбора этого соседа:
                    # - pheromone ** alpha: роль феромонов
                    # - (1 / weight) ** beta: роль обратного расстояния (чем меньше расстояние, тем лучше)
                    probability = (pheromone**self.alpha) * ((1 / weight) ** self.beta)
                    best_path = probability

            total = sum(probabilities) + best_path
            self.probability.append(best_path / total)
