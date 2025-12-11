# main.py
import pygame
from game import Game

PANEL_HEIGHT = 300
IMAGE_HEIGHT = 600

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, PANEL_HEIGHT + IMAGE_HEIGHT))
    pygame.display.set_caption("5 Days At HFU")

    game = Game(screen)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.handle_event(event)

        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
