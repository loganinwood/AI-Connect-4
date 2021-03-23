from board import Board
testboard = Board()
while True:
    print(testboard.legal_moves())
    move = input("Enter a move: ")
    while not move.isdecimal():
        move = input("Enter a move: ")
    move = int(move)
    testboard.make_move(move)
    print(testboard)
    if testboard.is_win():
        print("Game over, {} won!".format(not testboard.side))
        exit()
    if testboard.is_draw():
        print("Game over, it's a draw!")
        exit()
