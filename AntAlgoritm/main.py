import matplotlib.pyplot as plt

from src.graph import Graph
from src.antAlg import AntColonyOptimizer


file = open("mygraph.txt")
# Создаем граф
graph = Graph()

# Добавляем рёбра
for line in file.readlines():
    graph.add_edge(str(line.split()[0]), str(line.split()[1]), int(line.split()[2]))

# Параметры алгоритма
num_ants = 1000
alpha = 2.0
beta = 1.0
evaporation_rate = 1.3
iterations = 10

# Создаем оптимизатор и запускаем анимацию
aco = AntColonyOptimizer(graph, num_ants, alpha, beta, evaporation_rate, iterations)
for i in range(iterations):
    aco.optimize_iteration('a', 'd')
x_stack = aco.stack_path.keys()
y_stack = aco.stack_path.values()
x_cost = aco.iter_path.keys()
y_cost = aco.iter_path.values()
x_feromons = aco.pheromons_path.keys()
y_feromons = aco.pheromons_path.values()

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))
ax1.set_title("Зависимость застреваний муравья от итераций")
ax1.set_xlabel("Итерация")
ax1.set_ylabel("Кол-во застреваний")
ax1.plot(x_stack, y_stack)
ax1.grid(True)
ax2.set_title("Зависимость длины пути от итераций")
ax2.set_xlabel("Итерации")
ax2.set_ylabel("Длина пути")
ax2.plot(x_cost, y_cost)
ax2.grid(True)
ax3.set_title("Зависимость феромонов от итераций")
ax3.set_xlabel("Итерации")
ax3.set_ylabel("Феромоны")
ax3.plot(x_feromons, y_feromons)
ax3.grid(True)
plt.tight_layout()
plt.show()
