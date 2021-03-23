from board import Board
testboard = Board()
for i in range(43):
    print(testboard.legal_moves())
    move = input("Enter a move: ")
    while not move.isdecimal():
        move = input("Enter a move: ")
    move = int(move)
    testboard.make_move(move)
    print(testboard)
    if testboard.is_win() or testboard.is_draw():
        print("game over")
        exit()