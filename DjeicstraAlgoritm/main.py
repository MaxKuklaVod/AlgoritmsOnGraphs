from src.djeicstra import DijkstraAlgorithm
from src.graph import Graph

graph = Graph()
graph.add_edge("A", "B", 1)
graph.add_edge("A", "C", 4)
graph.add_edge("B", "C", 2)
graph.add_edge("B", "D", 6)
graph.add_edge("C", "D", 3)

# Инициализация алгоритма Дейкстры
dijkstra = DijkstraAlgorithm(graph)
start, end = "A", "D"
# Поиск кратчайшего пути
path, distance = dijkstra.find_shortest_path(start, end)

# Вывод результата
print(f"Кратчайший путь от {start} до {end}: {path}")
print(f"Общее расстояние: {distance}")
