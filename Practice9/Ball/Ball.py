import pygame


class Ball:
    """Red ball that moves around the screen."""

    def __init__(self, screen_width, screen_height):
        self.radius = 25
        self.diameter = 50
        self.color = (220, 50, 50)  # Red color
        self.speed = 20  # Pixels per key press

        self.screen_width = screen_width
        self.screen_height = screen_height

        # Start in the center
        self.x = screen_width // 2
        self.y = screen_height // 2

    def move(self, direction):
        """Move ball in given direction, but stay within screen boundaries."""
        new_x = self.x
        new_y = self.y

        if direction == "UP":
            new_y -= self.speed
        elif direction == "DOWN":
            new_y += self.speed
        elif direction == "LEFT":
            new_x -= self.speed
        elif direction == "RIGHT":
            new_x += self.speed

        # Check boundaries — ignore move if ball would go off screen
        if self.radius <= new_x <= self.screen_width - self.radius:
            self.x = new_x
        if self.radius <= new_y <= self.screen_height - self.radius:
            self.y = new_y

    def draw(self, surface):
        """Draw the ball on the given surface."""
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
        # Draw a small highlight to make it look 3D
        highlight_color = (255, 120, 120)
        pygame.draw.circle(surface, highlight_color, (self.x - 7, self.y - 7), 8)