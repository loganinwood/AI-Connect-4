from copy import deepcopy
import rawopening
import numpy as np
from table_entry import Entry

BOARD_WIDTH = 7
BOARD_HEIGHT = 6
TSIZE = 1e8

class MinmaxAgent():
    def __init__(self, depth=0):
        self.explored_nodes = 0
        self.best_column = 0
        self.trans_table = {}
        self.ZBOARD = [[np.uint64(0) for i in range(42)] for j in range(2)]
        self.ZOBRIST = np.random.randint(0, np.iinfo(np.uint64).max, dtype=np.uint64)
        for i in range(len(self.ZBOARD)):
            for j in range(len(self.ZBOARD[i])):
                self.ZBOARD[i][j] = np.random.randint(0, np.iinfo(np.uint64).max, dtype=np.uint64)

    def solve(self, board, depth):
        self.explored_nodes = 0
        self.best_column = 0
        if board.move_count <= 4:
            open = "".join(map(str, board.moves))
            return 0, rawopening.moves[open]
        alpha = -BOARD_WIDTH * BOARD_HEIGHT / 2
        beta = BOARD_WIDTH * BOARD_HEIGHT / 2
        score = self.minmax(board, alpha, beta, depth)

        print(f"Explored: {self.explored_nodes} nodes")

        sign = "+" if score >= 0 else ""
        print(f"Score: {sign}{score} Column: {self.best_column}")

        return score, self.best_column

    def minmax(self, board, alpha, beta, depth):
        s = f"{alpha} {beta}"
        assert alpha < beta, s

        self.explored_nodes += 1
        if depth == 0:
            return board.bval

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

        for column in self.move_ordering(board):
            if not board.is_valid_move(column):
                continue

            new_board = deepcopy(board)
            new_board.make_move_safe(column, self)

            score = -self.minmax(new_board, -beta, -alpha, depth - 1)
            if score > max_score:
                max_score = score
                max_column = column

            alpha = max(alpha, max_score)
            if alpha >= beta:
                break

            new_board.unmake_move_safe(self)

        self.best_column = max_column
        entry = Entry(self.ZOBRIST, depth, 0, max_score, max_column)
        self.update_table(entry)
        return max_score


    def update_table(self, entry):
        """
        Update transposition table with a replacement by depth method
        """
        global TSIZE
        key = self.ZOBRIST % TSIZE
        prev = self.trans_table.get(key)
        if prev is not None:
            if prev.depth <= entry.depth:
                self.trans_table[key] = entry
        else:
            self.trans_table[key] = entry

    def get_tableval(self):
        """
        Retrieve entry from transposition table for current zobrist hash
        """
        global TSIZE
        key = self.ZOBRIST % TSIZE
        prev = self.trans_table.get(key)
        return prev

    def move_ordering(self, board, bmove=None):
        """
        Orders moves by: move from iterative deepening
                         move from transposition table
                         closeness to center
        """
        global TSIZE
        tmove = None
        key = self.ZOBRIST % TSIZE
        prev = self.trans_table.get(key)
        if prev is not None:
            if prev.zobrist == self.ZOBRIST:
                # print("valid transposition table value")
                tmove = prev.move
        legal_movegen = lambda i: i if board.heights != 6 else -1
        legal_moves = [legal_movegen(i) for i in range(BOARD_WIDTH)]
        while -1 in legal_moves:
            legal_moves.remove(-1)
        ordered = sorted(legal_moves, key=lambda x: -100 if x == bmove else -50 if x == tmove else abs(3 - x))
        return ordered
