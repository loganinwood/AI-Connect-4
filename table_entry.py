class Entry:
    def __init__(self, zobrist, depth, flag, eval, move):
        self.zobrist = zobrist
        self.depth = depth
        self.flag = flag
        self.eval = eval
        self.move = move