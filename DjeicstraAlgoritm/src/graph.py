class Graph:
    """
    Класс Graph представляет граф, который используется для хранения ребер.
    Ребра хранятся в виде словаря, где ключами являются узлы, а значениями - списки соседних узлов и веса ребер.
    """

    def __init__(self):
        self.edges = {}

    def add_edge(self, from_node, to_node, weight):
        """
        Метод add_edge добавляет ребро между двумя узлами с указанным весом.
        from_node: начальный узел
        to_node: конечный узел
        weight: вес ребра
        """
        if from_node not in self.edges:
            self.edges[from_node] = []
        self.edges[from_node].append((to_node, weight))

    def get_neighbors(self, node):
        """
        Метод get_neighbors возвращает список соседних узлов и весов ребер для заданного узла.
        node: узел, для которого ищутся соседи
        """
        return self.edges.get(node, [])
