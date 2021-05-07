from board import Board
from agent import MinmaxAgent
import pygame
import numpy as np

(SCREEN_WIDTH, SCREEN_HEIGHT) = 700, 700

WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 128)
YELLOW = (255, 255, 0)

pygame.init()
board = Board()
agent = MinmaxAgent()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Connect-4")
pygame.display.set_icon(pygame.image.load("icon.png"))

# Control buttons / game info
font = pygame.font.Font(None, 32)

turn_text = font.render("Move:", True, WHITE)

auto_button_rect = pygame.Rect(280, 622, 140, 48)
auto_button_text = font.render("Auto move", True, BLACK)

running = True
game_won = 0
# 0 - No winner, 1 - Player won, 2 - Draw


while running:
    ev = pygame.event.get()

    # proceed events
    for event in ev:
        # handle QUIT
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if game_won:
                    game_won = False
                move = board.unmake_move_safe(agent)

        # handle MOUSEBUTTONUP
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

            # Place piece down
            if not game_won:
                # Find move by agent
                if auto_button_rect.collidepoint(pos):
                    print("searching...")
                    score, column = agent.solve(board, 8)
                    board.make_move_safe(column, agent)

                elif pos[1] <= 600:
                    column = pos[0] // 100

                    # Check if move is a winning move
                    if board.is_winning_move(column):
                        game_won = 1
                        side = "RED" if board.turn else "YELLOW"
                        print(f"{side} has won!")

                    # Make the move on the board
                    board.make_move_safe(column, agent)
                    # make_move(column, board)

                    # Check if game is drawn
                    if not game_won and board.is_draw():
                        game_won = 2

    # Clear screen
    screen.fill(BLUE)

    pos = pygame.mouse.get_pos()
    board.draw(screen)

    if game_won:
        # Display winner
        if game_won == 2:
            winner_color = WHITE
            win_text = "No winner! DRAW"
        elif board.turn:
            winner_color = YELLOW
            win_text = "YELLOW has won!"
        else:
            winner_color = RED
            win_text = "RED has won!"

        winner_blit = font.render(win_text, True, winner_color)
        screen.blit(winner_blit, (480, 634))
    else:
        # Highlight selected column
        if pos[1] <= 600:
            column = pos[0] // 100
            board.highlight(screen, column)

    # Control buttons / Game info
    screen.blit(turn_text, (20, 634))

    # Auto place move button
    pygame.draw.rect(screen, GREEN, auto_button_rect)
    screen.blit(auto_button_text, (292, 634))

    # Display current move
    if board.turn:
        turn_color = RED
        turn_color_text = "RED"
    else:
        turn_color = YELLOW
        turn_color_text = "YELLOW"

    turn_blit = font.render(turn_color_text, True, turn_color)
    screen.blit(turn_blit, (90, 634))

    # Update screen
    pygame.display.flip()

pygame.quit()
