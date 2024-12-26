from src.graph import GameGraph
from src.algoritm import AlphaBetaAlgorithm

def main():
    # Инициализация игры
    game = GameGraph(board_size=20, win_count=5)  # Игровая доска 20x20 и 5 в ряд для победы
    ai = AlphaBetaAlgorithm(game, max_depth=2, time_limit=20)  # Алгоритм альфа-бета с глубиной 2 и временем 1 секунда на ход

    # Настройка текущего игрока
    game.current_player = 1  # 1 - крестики (X), -1 - нолики (O)

    print("Игра началась! Вы играете за X. Компьютер за O.")
    game.print_board()

    while True:
        # Ход игрока (человек)
        if game.current_player == 1:
            print("\nВаш ход (X). Введите координаты (x y): ")
            try:
                x, y = map(int, input().split())  # Получаем координаты хода от игрока
                if not (0 <= x < game.board_size and 0 <= y < game.board_size):
                    print("Некорректные координаты. Попробуйте снова.")
                    continue
                if game.board[x][y] != 0:  # Проверка, если клетка уже занята
                    print("Эта клетка уже занята. Попробуйте снова.")
                    continue
            except (ValueError, IndexError):
                print("Некорректный ввод. Попробуйте снова.")
                continue

            game.apply_move(x, y, game.current_player)  # Применяем ход игрока
            if game.check_winner(game.current_player):
                print("\nПоздравляем, вы победили!")
                game.print_board()
                break

        # Ход компьютера (AI)
        else:
            print("\nХод компьютера (O).")
            x, y = ai.find_best_move(game.current_player)
            if x is None or y is None:
                print("Ничья! Нет доступных ходов.")
                break
            game.apply_move(x, y, game.current_player)
            print(f"Компьютер сделал ход: {x} {y}")
            if game.check_winner(game.current_player):
                print("\nКомпьютер победил!")
                game.print_board()
                break

        # Печать доски после каждого хода
        game.print_board()

        # Смена текущего игрока
        game.current_player = -game.current_player

if __name__ == "__main__":
    main()
