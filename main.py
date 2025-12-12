# main.py
import pygame
from game import Game

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 900  # 220 panel + 600 image

def show_start_screen(screen):
    clock = pygame.time.Clock()
    font_title = pygame.font.SysFont(None, 40)
    font_text = pygame.font.SysFont(None, 26)

    start_bg = None
    try:
        img = pygame.image.load("assets/images/start_screen.png").convert()
        start_bg = pygame.transform.scale(img, (WINDOW_WIDTH, WINDOW_HEIGHT))
    except Exception as e:
        print("Could not load start_screen.png:", e)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return True

        if start_bg is not None:
            screen.blit(start_bg, (0, 0))
        else:
            screen.fill((10, 10, 40))

        # top panel
        pygame.draw.rect(screen, (15, 15, 40), pygame.Rect(0, 0, WINDOW_WIDTH, 260))

        # title
        y = 20
        title_surf = font_title.render("5 Days At HFU", True, (255, 255, 255))
        screen.blit(title_surf, (20, y))
        y += 40

        # left column: goal + stats
        left_x = 20
        left_y = y
        left_lines = [
            "Goal:",
            "Survive 5 days and pass",
            "the exam on Friday.",
            "",
            "Stats:",
            "SOC  = Social (unlocks options)",
            "KNOW = Knowledge (exam success)",
            "NRG  = Energy (limits actions)",
        ]
        for line in left_lines:
            surf = font_text.render(line, True, (230, 230, 230))
            screen.blit(surf, (left_x, left_y))
            left_y += 22

        # right column: controls
        right_x = WINDOW_WIDTH // 2 + 20
        right_y = y
        right_lines = [
            "Controls:",
            "Up / Down  = select",
            "Enter      = confirm",
            "",
            "During exam:",
            "Enter      = restart",
            "Press ENTER or SPACE",
            "to start the game.",
        ]
        for line in right_lines:
            surf = font_text.render(line, True, (230, 230, 230))
            screen.blit(surf, (right_x, right_y))
            right_y += 22

        pygame.display.flip()
        clock.tick(60)

    return False

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("5 Days At HFU")

    proceed = show_start_screen(screen)
    if not proceed:
        pygame.quit()
        return

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
