from board import Board
import pygame

(SCREEN_WIDTH, SCREEN_HEIGHT) = 700, 700

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 128)
YELLOW = (255, 255, 0)

pygame.init()
testboard = Board()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Connect-4")
pygame.display.set_icon(pygame.image.load("icon.png"))

font = pygame.font.Font(None, 32)
move_text = font.render("Move:", True, WHITE)

running = True

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
                move = testboard.unmake_move()

        # handle MOUSEBUTTONUP
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            move = pos[0] // 100
            if move in testboard.legal_moves():
                testboard.make_move(move)

    # Clear screen
    screen.fill(BLUE)

    # Highlight selected column
    pos = pygame.mouse.get_pos()
    column = pos[0] // 100
    testboard.draw(screen)
    testboard.highlight(column, screen)

    # Control buttons / Game Info
    screen.blit(move_text, (20, 634))

    if testboard.side:
        move_color = RED
        move_color_text = "RED"
    else:
        move_color = YELLOW
        move_color_text = "YELLOW"

    move_player = font.render(move_color_text, True, move_color)
    screen.blit(move_player, (90, 634))

    # Update screen
    pygame.display.flip()

    if testboard.is_win():
        winning_side = "Red" if not testboard.side else "Yellow"
        print("Game over, {} won!".format(winning_side))
        # print(testboard)
        running = False
    if testboard.is_draw():
        print("Game over, it's a draw!")
        # print(testboard)
        running = False

pygame.quit()
