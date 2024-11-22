from src.graph import Graph
from src.antAlg import AntColonyOptimizer


file = open('graph.txt')
# Создаем граф
graph = Graph()

# Добавляем рёбра
for line in file.readlines():
    graph.add_edge(str(line.split()[0]), str(line.split()[1]), int(line.split()[2]))

# Параметры алгоритма
num_ants = 5
alpha = 1.0
beta = 2.0
evaporation_rate = 0.5
iterations = 20

# Создаем оптимизатор и запускаем анимацию
aco = AntColonyOptimizer(graph, num_ants, alpha, beta, evaporation_rate, iterations)
aco.run_animation("a", "c")

