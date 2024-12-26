import time


class AlphaBetaAlgorithm:
    def __init__(self, game_graph, max_depth=2, time_limit=1):
        self.game_graph = game_graph
        self.max_depth = max_depth
        self.time_limit = time_limit
        self.start_time = None

    def alpha_beta(self, depth, alpha, beta, maximizing_player):
        """Алгоритм альфа-бета отсечения."""
        if depth == 0 or abs(self.game_graph.evaluate()) == 100:
            return self.game_graph.evaluate()

        if time.time() - self.start_time > self.time_limit:
            return 0  # Временной лимит, возвращаем нейтральную оценку

        if maximizing_player:
            max_eval = -float("inf")
            for x, y in self.generate_prioritized_moves():                
                self.game_graph.apply_move(x, y, 1)  # Ход компьютера
                eval = self.alpha_beta(depth - 1, alpha, beta, False)
                self.game_graph.undo_move(x, y)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for x, y in self.generate_prioritized_moves():
                self.game_graph.apply_move(x, y, -1)  # Ход игрока
                eval = self.alpha_beta(depth - 1, alpha, beta, True)
                self.game_graph.undo_move(x, y)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def generate_prioritized_moves(self):
        """Генерация ходов с приоритетом: блокировка ходов игрока и возможности для победы."""
        # Генерация всех возможных ходов
        moves = self.game_graph.generate_moves()

        # Сначала проверяем возможные победные ходы для компьютера
        win_moves = self.find_threat_moves(1)  # Победные ходы для компьютера
        if win_moves:
            return win_moves

        # Затем проверяем блокировку угроз игрока
        threat_moves = self.find_threat_moves(-1)  # Блокировка игрока
        if threat_moves:
            return threat_moves

        # Если нет угроз и победных ходов, возвращаем обычные ходы
        return moves

    def find_threat_moves(self, player):
        """Нахождение угроз или победных ходов для указанного игрока (player)."""
        moves = []
        for x, y in self.game_graph.generate_moves():
            self.game_graph.apply_move(x, y, player)
            if self.game_graph.check_winner(player):  # Если ход ведет к победе
                moves.append((x, y))
            self.game_graph.undo_move(x, y)
        return moves

    def find_best_move(self, player):
        """Поиск лучшего хода с учетом времени."""
        self.start_time = time.time()
        best_move = None
        best_value = -float("inf") if player == 1 else float("inf")

        # Сначала оцениваем приоритетные ходы (блокировка или победа)
        for x, y in self.generate_prioritized_moves():
            self.game_graph.apply_move(x, y, player)
            move_value = self.alpha_beta(
                self.max_depth - 1, -float("inf"), float("inf"), player == -1
            )
            self.game_graph.undo_move(x, y)

            if (player == 1 and move_value > best_value) or (
                player == -1 and move_value < best_value
            ):
                best_value = move_value
                best_move = (x, y)

            # Прерываем поиск, если время истекло
            if time.time() - self.start_time > self.time_limit:
                break

        return best_move