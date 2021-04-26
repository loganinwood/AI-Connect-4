from copy import deepcopy

BOARD_WIDTH = 7
BOARD_HEIGHT = 6

class MinmaxAgent():
    def __init__(self, depth=0):
        self.count = 0

    def solve(self, board):
        self.count = 0
        return self.minmax(board)

    def minmax(self, board):
        self.count += 1
        print(self.count)

        if board.is_draw():
            return (0, None)

        for column in range(BOARD_WIDTH):
            if board.is_winning_move(column):
                return ((BOARD_WIDTH * BOARD_HEIGHT + 1 - board.move_count) / 2, column)

        max_score = -BOARD_WIDTH * BOARD_HEIGHT
        max_column = 0

        for column in range(BOARD_WIDTH):
            if board.is_valid_move(column):
                new_board = deepcopy(board)
                new_board.make_move(column)

                (new_score, new_column) = self.minmax(new_board)
                if -new_score > max_score:
                    max_score = -new_score
                    max_column = column

        return (max_score, max_column)