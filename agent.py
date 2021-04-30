from copy import deepcopy

BOARD_WIDTH = 7
BOARD_HEIGHT = 6


class MinmaxAgent():
    def __init__(self, depth=0):
        self.explored_nodes = 0
        self.best_column = 0

    def solve(self, board):
        self.explored_nodes = 0
        self.best_column = 0

        alpha = -BOARD_WIDTH * BOARD_HEIGHT / 2
        beta = BOARD_WIDTH * BOARD_HEIGHT / 2
        score = self.minmax(board, alpha, beta)

        print(f"Explored: {self.explored_nodes} nodes")

        sign = "+" if score >= 0 else ""
        print(f"Score: {sign}{score} Column: {self.best_column}")

        return score, self.best_column

    def minmax(self, board, alpha, beta):
        s = f"{alpha} {beta}"
        assert alpha < beta, s

        self.explored_nodes += 1

        """
        Start to test if we are in a terminal state
        """
        if board.is_draw():
            self.best_column = None
            return 0

        for column in range(BOARD_WIDTH):
            if board.is_winning_move(column):
                self.best_column = column
                return (BOARD_WIDTH * BOARD_HEIGHT + 1 - board.move_count) / 2

        """
        Time to score
        """
        max_score = float("-inf")
        max_column = 0

        for column in range(BOARD_WIDTH):
            if not board.is_valid_move(column):
                continue

            new_board = deepcopy(board)
            new_board.make_move(column)

            score = -self.minmax(new_board, -beta, -alpha)
            if score > max_score:
                max_score = score
                max_column = column

            alpha = max(alpha, max_score)
            if alpha >= beta:
                break

        self.best_column = max_column
        return max_score
