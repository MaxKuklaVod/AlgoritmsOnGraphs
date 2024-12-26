import heapq


class DijkstraAlgorithm:
    """
    Класс DijkstraAlgorithm реализует алгоритм Дейкстры для поиска кратчайшего пути
    в графе с ненулевыми положительными весами ребер.
    """

    def __init__(self, graph):
        """
        Инициализирует алгоритм Дейкстры с заданным графом.
        graph: объект класса Graph
        """
        self.graph = graph

    def find_shortest_path(self, start_node, end_node):
        """
        Метод find_shortest_path находит кратчайший путь от start_node до end_node.
        start_node: начальный узел
        end_node: конечный узел
        Возвращает:
        - path: список узлов, представляющий кратчайший путь
        - distance: суммарное расстояние этого пути
        """
        # Очередь с приоритетом для обработки узлов в порядке увеличения расстояния
        priority_queue = []
        heapq.heappush(priority_queue, (0, start_node))

        # Словарь для хранения минимальных расстояний до каждого узла
        distances = {start_node: 0}

        # Словарь для восстановления пути
        parents = {start_node: None}

        while priority_queue:
            # Извлечение узла с минимальным расстоянием
            current_distance, current_node = heapq.heappop(priority_queue)

            # Если достигли конечного узла, можно завершить
            if current_node == end_node:
                break

            # Обход соседей текущего узла
            for neighbor, weight in self.graph.get_neighbors(current_node):
                # Вычисление нового расстояния
                distance = current_distance + weight
                # Если найден более короткий путь, обновляем данные
                if neighbor not in distances or distance < distances[neighbor]:
                    distances[neighbor] = distance
                    parents[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

        # Восстановление пути от конечного узла к начальному
        path = []
        node = end_node
        while node is not None:
            path.append(node)
            node = parents.get(node)

        return path[::-1], distances.get(end_node, float("inf"))
