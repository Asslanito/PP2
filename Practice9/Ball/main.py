import pygame
import sys
from ball import Ball

# Window settings
WIDTH = 600
HEIGHT = 500
FPS = 60
TITLE = "Moving Ball Game"


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    ball = Ball(WIDTH, HEIGHT)

    # Font for instructions
    font = pygame.font.SysFont("Arial", 18)

    running = True
    while running:
        clock.tick(FPS)

        # --- Event handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ball.move("UP")
                elif event.key == pygame.K_DOWN:
                    ball.move("DOWN")
                elif event.key == pygame.K_LEFT:
                    ball.move("LEFT")
                elif event.key == pygame.K_RIGHT:
                    ball.move("RIGHT")
                elif event.key == pygame.K_ESCAPE:
                    running = False

        # --- Drawing ---
        screen.fill((255, 255, 255))  # White background

        ball.draw(screen)

        # Show instructions
        instructions = [
            "Arrow Keys — Move Ball",
            "ESC — Quit",
            f"Position: ({ball.x}, {ball.y})"
        ]
        for i, text in enumerate(instructions):
            label = font.render(text, True, (100, 100, 100))
            screen.blit(label, (10, 10 + i * 22))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()