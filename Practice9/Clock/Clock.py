import pygame
import math
import datetime


class MickeysClock:
    """
    Mickey Mouse clock using his hands as clock hands.
    Right hand = minutes, Left hand = seconds.
    """

    def __init__(self, screen_width, screen_height):
        self.center_x = screen_width // 2
        self.center_y = screen_height // 2

        # Clock circle settings
        self.clock_radius = 180
        self.bg_color = (255, 245, 220)  # Cream background
        self.circle_color = (255, 200, 100)  # Orange clock face
        self.border_color = (180, 120, 40)  # Brown border

        # Hand settings
        self.minute_color = (30, 100, 200)  # Blue for minutes
        self.second_color = (200, 40, 40)  # Red for seconds
        self.hand_length = 130
        self.hand_width_min = 10
        self.hand_width_sec = 7

        # Font for numbers and time display
        self.font_numbers = None
        self.font_time = None

    def load_fonts(self):
        """Load fonts after pygame.init() is called."""
        self.font_numbers = pygame.font.SysFont("Arial", 22, bold=True)
        self.font_time = pygame.font.SysFont("Courier New", 42, bold=True)

    def _angle_for_seconds(self, seconds):
        """Convert seconds (0-59) to angle in radians. 12 o'clock = -90 deg."""
        return math.radians(seconds * 6 - 90)

    def _angle_for_minutes(self, minutes, seconds):
        """Convert minutes + seconds to smooth angle in radians."""
        total = minutes + seconds / 60
        return math.radians(total * 6 - 90)

    def _hand_endpoint(self, angle, length):
        """Calculate the tip coordinates of a hand given angle and length."""
        x = self.center_x + int(length * math.cos(angle))
        y = self.center_y + int(length * math.sin(angle))
        return (x, y)

    def draw(self, surface):
        """Draw the full clock on the given surface."""
        now = datetime.datetime.now()
        minutes = now.minute
        seconds = now.second

        # Draw clock background circle
        pygame.draw.circle(surface, self.circle_color,
                           (self.center_x, self.center_y), self.clock_radius)
        pygame.draw.circle(surface, self.border_color,
                           (self.center_x, self.center_y), self.clock_radius, 6)

        # Draw hour markers (dots at each 5-minute position)
        for i in range(12):
            angle = math.radians(i * 30 - 90)
            dot_x = self.center_x + int((self.clock_radius - 20) * math.cos(angle))
            dot_y = self.center_y + int((self.clock_radius - 20) * math.sin(angle))
            pygame.draw.circle(surface, self.border_color, (dot_x, dot_y), 6)

        # Draw minute numbers (0, 5, 10, ..., 55)
        if self.font_numbers:
            for i in range(12):
                num = i * 5
                angle = math.radians(i * 30 - 90)
                num_x = self.center_x + int((self.clock_radius - 45) * math.cos(angle))
                num_y = self.center_y + int((self.clock_radius - 45) * math.sin(angle))
                label = self.font_numbers.render(str(num), True, (80, 40, 10))
                rect = label.get_rect(center=(num_x, num_y))
                surface.blit(label, rect)

        # Calculate angles
        min_angle = self._angle_for_minutes(minutes, seconds)
        sec_angle = self._angle_for_seconds(seconds)

        # Draw MINUTE hand (right hand — blue, thicker)
        min_end = self._hand_endpoint(min_angle, self.hand_length)
        pygame.draw.line(surface, self.minute_color,
                         (self.center_x, self.center_y), min_end, self.hand_width_min)
        # Draw round tip for minute hand
        pygame.draw.circle(surface, self.minute_color, min_end, 12)

        # Draw SECOND hand (left hand — red, thinner)
        sec_end = self._hand_endpoint(sec_angle, self.hand_length - 10)
        pygame.draw.line(surface, self.second_color,
                         (self.center_x, self.center_y), sec_end, self.hand_width_sec)
        # Draw round tip for second hand
        pygame.draw.circle(surface, self.second_color, sec_end, 9)

        # Center dot
        pygame.draw.circle(surface, (60, 30, 5),
                           (self.center_x, self.center_y), 10)

        # Display current time as text below the clock
        if self.font_time:
            time_str = f"{minutes:02d}:{seconds:02d}"
            time_label = self.font_time.render(time_str, True, (50, 50, 50))
            rect = time_label.get_rect(center=(self.center_x, self.center_y + self.clock_radius + 40))
            surface.blit(time_label, rect)

        # Legend
        if self.font_numbers:
            legend1 = self.font_numbers.render("Blue = Minutes (right hand)", True, self.minute_color)
            legend2 = self.font_numbers.render("Red  = Seconds (left hand)", True, self.second_color)
            surface.blit(legend1, (10, 10))
            surface.blit(legend2, (10, 35))