from board import Board
import random
import pygame
import time


SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600
pygame.init()
testboard = Board()
draws = 0
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill((0, 0, 128))
running = True
while running:
    # print(testboard.legal_moves())
    # move = random.choice(list(testboard.legal_moves()))
    ev = pygame.event.get()

    # proceed events
    for event in ev:

        # handle MOUSEBUTTONUP
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            move = pos[0] // 100
            if move in testboard.legal_moves():
                testboard.make_move(move)
    pos = pygame.mouse.get_pos()
    column = pos[0] // 100
    screen.fill((0, 0, 128))
    testboard.draw(screen)
    testboard.highlight(column, screen)
    pygame.display.flip()
    if testboard.is_win():
        print("Game over, {} won!".format("Red" if not testboard.side else "Yellow"))
        # print(testboard)
        running = False
    if testboard.is_draw():
        print("Game over, it's a draw!")
        # print(testboard)
        running = False
pygame.quit()
