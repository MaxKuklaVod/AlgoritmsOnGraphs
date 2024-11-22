import random


class Ant:
    def __init__(self, start_node):
        """
        Инициализирует муравья с начальной позицией.

        Параметры:
        start_node (int/str): Узел, с которого начинает движение муравей.

        Атрибуты:
        start_node (int/str): Начальный узел муравья.
        path (list): Маршрут, пройденный муравьем, начинается с начального узла.
        total_cost (float): Общая стоимость (длина) маршрута.
        """
        self.start_node = start_node  # Начальная позиция муравья
        self.path = [start_node]  # Маршрут муравья (список узлов)
        self.total_cost = 0  # Общая стоимость пройденного пути

    def move(self, graph, alpha, beta):
        """
        Выполняет перемещение муравья в следующий узел на основе вероятностного выбора.

        Параметры:
        graph (Graph): Граф, содержащий информацию о соседях и феромонах.
        alpha (float): Влияние феромонов на выбор (чем больше, тем сильнее роль феромонов).
        beta (float): Влияние расстояния на выбор (чем больше, тем важнее короткий путь).
        """
        # Текущий узел муравья (последний узел в его пути)
        current_node = self.path[-1]

        # Получаем список соседей текущего узла (в формате [(сосед, вес), ...])
        neighbors = graph.get_neighbors(current_node)

        # Фильтруем соседей, которые уже посещены

        unvisited_neighbors = [
            (neighbor, weight)
            for neighbor, weight in neighbors
            if neighbor not in self.path
        ]

        if not unvisited_neighbors:  # Если нет непосещённых соседей
            print(f"Муравей на вершине {current_node} застрял. Перезагружаем путь...")
            self.path = [self.start_node]  # Перезапускаем путь
            self.total_cost = 0
            return

        # Список вероятностей для каждого соседа
        probabilities = []
        for neighbor, weight in unvisited_neighbors:
            # Уровень феромонов на ребре (current_node, neighbor)
            pheromone = graph.pheromone.get((current_node, neighbor), 1.0)
            # Вычисляем вероятность выбора этого соседа:
            # - pheromone ** alpha: роль феромонов
            # - (1 / weight) ** beta: роль обратного расстояния (чем меньше расстояние, тем лучше)
            probability = (pheromone**alpha) * ((1 / weight) ** beta)
            probabilities.append(probability)

        # Нормализуем вероятности, чтобы их сумма равнялась 1
        total = sum(probabilities)
        probabilities = [p / total for p in probabilities]

        # Случайно выбираем следующий узел с учетом нормализованных вероятностей
        next_node = random.choices(
            [neighbor for neighbor, _ in unvisited_neighbors],  # Список соседей
            weights=probabilities,  # Соответствующие вероятности
        )[0]

        # Стоимость следующего узла
        next_cost = dict(unvisited_neighbors)[next_node]

        # Обновляем маршрут муравья (добавляем следующий узел)
        self.path.append(next_node)

        # Обновляем общую стоимость пути
        self.total_cost += next_cost
