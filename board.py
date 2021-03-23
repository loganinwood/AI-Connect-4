import numpy as np
class Board:
    def __init__(self):
        self.counter = 0
        self.rows = [6]*7
        self.board = [0] * 42
        self.moves = []
        self.side = True

    def __str__(self):
        res = ""
        for i in range(42):
            if i % 7 == 0 and i > 0:
                res += "\n"
            res += str(self.board[i]) + "  "
        return res

    def make_move(self, move):
        if move in self.legal_moves():
            self.moves.append(move)
            val = 7 * (self.rows[move] - 1) + move
            self.rows[move] = self.rows[move] - 1
            piece = 1 if self.side else 2
            self.board[val] = piece
            self.side = not self.side
            self.counter += 1
        else:
            print("Not a legal move")

    def unmake_move(self):
        move = self.moves.pop()
        self.rows[move] = self.rows[move] + 1
        self.side = not self.side
        val = 7 * (self.rows[move] - 1) + move
        self.board[val] = 0
        self.counter -= 1
        return move

    def legal_moves(self):
        res = set()
        for i in range(len(self.rows)):
            if self.rows[i] != 0:
                res.add(i)
        return res

    def is_win(self):
        piece = 2 if self.side else 1
        for i in range(6):
            for j in range(4):
                if self.board[7 * i + j] == piece and self.board[7 * i + j + 1] == piece and self.board[7 * i + j + 2] == piece and self.board[7 * i + j + 3] == piece:
                    return True
        for i in range(7):
            for j in range(3):
                if self.board[i + j * 7] == piece and self.board[i + (j + 1) * 7] == piece and self.board[i + (j + 2) * 7] == piece and self.board[i + (j + 3) * 7] == piece:
                    return True
        for i in range(4):
            for j in range(3):
                if self.board[j * 7 + i] == piece and self.board[(j + 1) * 7 + i + 1] == piece and self.board[(j + 2) * 7 + i + 2] == piece and self.board[(j + 3) * 7 + i + 3] == piece:
                    return True
        for i in range(3, 7):
            for j in range(3):
                if self.board[j * 7 + i] == piece and self.board[(j + 1) * 7 + i - 1] == piece and self.board[(j + 2) * 7 + i - 2] == piece and self.board[(j + 3) * 7 + i - 3] == piece:
                    return True
        return False

    def is_draw(self):
        return self.counter == 42
