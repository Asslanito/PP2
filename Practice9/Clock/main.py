import pygame
import sys
from clock import MickeysClock

# Window settings
WIDTH = 600
HEIGHT = 550
FPS = 10  # 10 FPS is enough for a clock (updates every ~0.1s)
TITLE = "Mickey's Clock"


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock_tick = pygame.time.Clock()

    # Create Mickey's clock
    mickey_clock = MickeysClock(WIDTH, HEIGHT - 50)
    mickey_clock.load_fonts()  # Must be called after pygame.init()

    running = True
    while running:
        clock_tick.tick(FPS)

        # --- Event handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # --- Drawing ---
        screen.fill((230, 240, 255))  # Light blue background
        mickey_clock.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()