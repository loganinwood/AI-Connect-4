import pygame

# COLORS
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

BOARD_WIDTH = 7
BOARD_HEIGHT = 6


class Board:
    def __init__(self):
        self.move_count = 0
        self.turn = True

        self.moves = []
        # self.board = [[0] * BOARD_WIDTH in range(BOARD_HEIGHT)]
        self.board = []
        for x in range(BOARD_WIDTH):
            self.board.append([0] * BOARD_HEIGHT)
        self.heights = [0] * BOARD_WIDTH

    def get_current_player(self):
        """
        Return the piece value of the current player
        """

        return 1 if self.turn else 2

    def get_pos(self, x, y):
        """
        Returns the value at the board position
        (0 - None, 1 - Red, 2 - Yellow)

        Returns None if not a valid board position
        """

        if 0 <= x < BOARD_WIDTH and 0 <= y < BOARD_HEIGHT:
            return self.board[x][y]

        return None

    def is_valid_move(self, column):
        """
        A move is valid if the piece can be placed in the column
        (column is not full)
        """

        return self.heights[column] < BOARD_HEIGHT

    def is_winning_move(self, column):
        """
        Returns the value of the current player
        """

        if not self.is_valid_move(column):
            return None

        piece = self.get_current_player()

        # Check for vertical win
        col_height = self.heights[column]
        if col_height >= 3:
            if self.get_pos(column, col_height - 1) == piece and \
               self.get_pos(column, col_height - 2) == piece and \
               self.get_pos(column, col_height - 3) == piece:
                return True

        # Check for horizontal win
        lower_bound = max(0, column - 3)
        upper_bound = min(BOARD_WIDTH, column + 4)
        iteration = list(range(lower_bound, upper_bound))
        iteration.remove(column)

        in_row = 0
        for x in iteration:
            if self.get_pos(x, col_height) == piece:
                in_row += 1
                if in_row == 3:
                    return True
            else:
                in_row = 0

        # Check for diagonal wins
        in_row_up = 0
        in_row_down = 0
        for x in iteration:
            if self.get_pos(x, col_height + (x - column)) == piece:
                in_row_up += 1
                if in_row_up == 3:
                    return True
            else:
                in_row_up = 0

            if self.get_pos(x, col_height - (x - column)) == piece:
                in_row_down += 1
                if in_row_down == 3:
                    return True
            else:
                in_row_down = 0

        return False

    def is_draw(self):
        """
        Draws occur when the board is full and no winner
        """

        return self.move_count == BOARD_WIDTH * BOARD_HEIGHT

    def make_move(self, column):
        """
        With a given column place piece in lowest available slot.
        """

        if not self.is_valid_move(column):
            return False

        player_piece = self.get_current_player()

        (x, y) = column, self.heights[column]
        self.board[x][y] = player_piece
        self.heights[column] += 1

        self.moves.append(column)
        self.move_count += 1
        self.turn = not self.turn

        return True

    def undo_move(self):
        """
        If there are moves present to undo then revert one move.
        """

        if self.move_count == 0:
            return False

        column = self.moves.pop()

        self.heights[column] -= 1
        self.board[column][self.heights[column]] = 0

        self.move_count -= 1
        self.turn = not self.turn

        return True

    def draw(self, display):
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                piece = self.board[x][y]

                if piece == 0:
                    color = WHITE
                elif piece == 1:
                    color = RED
                elif piece == 2:
                    color = YELLOW

                center = (x * 100 + 50, (BOARD_HEIGHT - y - 1) * 100 + 50)
                pygame.draw.circle(display, color, center, 40)

    def highlight(self, screen, column):
        for i in range(self.heights[column], BOARD_HEIGHT):
            center = (column * 100 + 50, (BOARD_HEIGHT - i - 1) * 100 + 50)
            pygame.draw.circle(screen, GRAY, center, 40)
