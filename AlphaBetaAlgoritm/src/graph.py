import numpy as np


class GameGraph:
    def __init__(self, board_size=20, win_count=5):
        """Инициализация игры с заданным размером доски и количеством символов для победы."""
        self.board_size = board_size
        self.win_count = win_count
        self.board = np.zeros(
            (self.board_size, self.board_size), dtype=int
        )  # 0 - пустая клетка, 1 - крестик (X), -1 - нолик (O)

    def reset_board(self):
        """Сбрасывает доску в начальное состояние."""
        self.board.fill(0)

    def check_winner(self, player):
        """Проверяет, есть ли победитель для данного игрока."""
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] == player:
                    if any(
                        self.check_line(x, y, dx, dy, player)
                        for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]
                    ):
                        return True
        return False

    def check_line(self, x, y, dx, dy, player):
        """Проверяет, есть ли линия длины win_count с указанной начальной точки (x, y) в заданном направлении (dx, dy)."""
        count = 0
        for i in range(self.win_count):
            nx, ny = x + i * dx, y + i * dy
            if (
                0 <= nx < self.board_size
                and 0 <= ny < self.board_size
                and self.board[nx][ny] == player
            ):
                count += 1
            else:
                break
        return count == self.win_count

    def generate_moves(self):
        """Возвращает список всех доступных ходов (пустых клеток)."""
        moves = []
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] == 0:
                    # Добавляем только клетки, которые находятся рядом с занятыми
                    if any(
                        0 <= x + dx < self.board_size
                        and 0 <= y + dy < self.board_size
                        and self.board[x + dx][y + dy] != 0
                        for dx, dy in [
                            (-1, 0),
                            (1, 0),
                            (0, -1),
                            (0, 1),
                            (-1, -1),
                            (-1, 1),
                            (1, -1),
                            (1, 1),
                        ]
                    ):
                        moves.append((x, y))
        return (
            moves
            if moves
            else [
                (x, y)
                for x in range(self.board_size)
                for y in range(self.board_size)
                if self.board[x][y] == 0
            ]
        )

    def apply_move(self, x, y, player):
        """Применяет ход для игрока (1 для крестика, -1 для нолика)."""
        if self.board[x][y] == 0:  # Проверка, что клетка пуста
            self.board[x][y] = player
            return True
        return False

    def undo_move(self, x, y):
        """Отменяет ход, ставя клетку в начальное состояние (0)."""
        self.board[x][y] = 0

    def evaluate(self):
        """Оценка состояния доски:
        - 100 если выиграл крестик
        - -100 если выиграл нолик
        - 0 если нет победителя.
        """
        if self.check_winner(1):  # Крестики
            return 100
        elif self.check_winner(-1):  # Нолики
            return -100
        return self.evaluate_board()

    def evaluate_board(self):
        """Оценка доски для определения выгодных позиций."""
        score = 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] != 0:
                    player = self.board[x][y]
                    for dx, dy in directions:
                        score += self.evaluate_line(x, y, dx, dy, player)
        return score

    def evaluate_line(self, x, y, dx, dy, player):
        """Оценивает одну линию с началом в точке (x, y) и направлением (dx, dy)."""
        count = 0
        open_ends = 0
        for i in range(self.win_count):
            nx, ny = x + i * dx, y + i * dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                if self.board[nx][ny] == player:
                    count += 1
                elif self.board[nx][ny] == 0:
                    open_ends += 1
                else:
                    break

        if count == self.win_count:
            return 10000  # Победа
        elif count == 4 and open_ends > 0:
            return 100  # Почти победа
        elif count == 3 and open_ends > 1:
            return 50  # Хорошая линия
        elif count == 2 and open_ends > 1:
            return 10  # Перспективная линия
        return 0

    def print_board(self):
        """Выводит текущее состояние доски на экран с номерами строк и столбцов."""
        # Печать верхней границы с номерами столбцов
        print("   ", end="")  # Отступ для номеров строк
        for col in range(self.board_size):
            print(f" {col:2}", end=" ")  # Печать номера столбца с отступом
        print()  # Печать новой строки

        # Печать разделителей
        print(
            "   " + "----" * self.board_size
        )  # Разделитель между номерами и самой доской

        # Печать доски с номерами строк
        for row in range(self.board_size):
            print(f"{row:2} |", end="")  # Печать номера строки и разделитель
            for col in range(self.board_size):
                cell = self.board[row][col]
                # Печать символов доски, X для крестиков, O для ноликов, . для пустых клеток
                print(f" {'X' if cell == 1 else 'O' if cell == -1 else '.'} ", end="|")
            print()  # Печать новой строки после каждого ряда

            # Печать разделителя между рядами
            print("   " + "----" * self.board_size)  # Разделитель между рядами
