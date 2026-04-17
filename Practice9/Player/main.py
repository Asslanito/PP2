import pygame
import sys
import os
from player import MusicPlayer

# Window settings
WIDTH = 600
HEIGHT = 500
FPS = 30
TITLE = "Music Player"

# Colors
BG_COLOR = (20, 20, 35)
PANEL_COLOR = (35, 35, 55)
ACCENT_COLOR = (80, 160, 255)
TEXT_COLOR = (220, 220, 220)
DIM_COLOR = (120, 120, 140)
PLAYING_COLOR = (80, 220, 120)
STOPPED_COLOR = (220, 80, 80)
HIGHLIGHT = (60, 60, 90)


def draw_text(surface, text, font, color, x, y, center=False):
    """Helper to draw text, optionally centered on x."""
    label = font.render(text, True, color)
    if center:
        rect = label.get_rect(center=(x, y))
        surface.blit(label, rect)
    else:
        surface.blit(label, (x, y))


def draw_rounded_rect(surface, color, rect, radius=12):
    """Draw a rectangle with rounded corners."""
    pygame.draw.rect(surface, color, rect, border_radius=radius)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    # Fonts
    font_big = pygame.font.SysFont("Arial", 28, bold=True)
    font_medium = pygame.font.SysFont("Arial", 20)
    font_small = pygame.font.SysFont("Arial", 16)
    font_title = pygame.font.SysFont("Arial", 36, bold=True)

    # Music player — looks for files in the 'music/' subfolder
    music_dir = os.path.join(os.path.dirname(__file__), "music")
    player = MusicPlayer(music_folder=music_dir)

    running = True
    while running:
        clock.tick(FPS)

        # Auto-advance to next track when current one ends
        player.check_track_ended()

        # --- Event handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # P = Play
                    player.play()
                elif event.key == pygame.K_s:  # S = Stop
                    player.stop()
                elif event.key == pygame.K_n:  # N = Next
                    player.next_track()
                elif event.key == pygame.K_b:  # B = Back (previous)
                    player.previous_track()
                elif event.key == pygame.K_UP:  # Up = Volume +
                    player.volume_up()
                elif event.key == pygame.K_DOWN:  # Down = Volume -
                    player.volume_down()
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    running = False

        # --- Drawing ---
        screen.fill(BG_COLOR)

        # Title
        draw_text(screen, "🎵  Music Player", font_title, ACCENT_COLOR, WIDTH // 2, 35, center=True)

        # Now Playing panel
        draw_rounded_rect(screen, PANEL_COLOR, pygame.Rect(40, 75, WIDTH - 80, 100))
        draw_text(screen, "NOW PLAYING", font_small, DIM_COLOR, WIDTH // 2, 95, center=True)
        track_name = player.get_track_name()
        # Truncate long names
        if len(track_name) > 36:
            track_name = track_name[:33] + "..."
        draw_text(screen, track_name, font_big, TEXT_COLOR, WIDTH // 2, 130, center=True)

        # Status + volume
        status = player.get_status()
        status_color = PLAYING_COLOR if player.is_playing else STOPPED_COLOR
        draw_text(screen, status, font_medium, status_color, WIDTH // 2, 165, center=True)
        vol_text = f"Volume: {int(player.volume * 100)}%"
        draw_text(screen, vol_text, font_small, DIM_COLOR, WIDTH - 50, 165, center=True)

        # Playlist panel
        draw_rounded_rect(screen, PANEL_COLOR, pygame.Rect(40, 195, WIDTH - 80, 185))
        draw_text(screen, "PLAYLIST", font_small, DIM_COLOR, 60, 205)

        playlist = player.get_playlist_info()
        if not playlist:
            draw_text(screen, "No .mp3 / .wav files found in music/ folder",
                      font_small, DIM_COLOR, WIDTH // 2, 270, center=True)
        else:
            for i, name in enumerate(playlist[:6]):  # Show up to 6 tracks
                y = 225 + i * 26
                if i == player.current_index:
                    draw_rounded_rect(screen, HIGHLIGHT, pygame.Rect(50, y - 3, WIDTH - 100, 24), radius=6)
                    prefix = "▶  "
                    color = ACCENT_COLOR
                else:
                    prefix = f"{i + 1}.  "
                    color = TEXT_COLOR
                name_display = name if len(name) <= 38 else name[:35] + "..."
                draw_text(screen, prefix + name_display, font_small, color, 60, y)

        # Controls help panel
        draw_rounded_rect(screen, PANEL_COLOR, pygame.Rect(40, 395, WIDTH - 80, 90))
        controls = [
            ("[P] Play", PLAYING_COLOR),
            ("[S] Stop", STOPPED_COLOR),
            ("[N] Next", ACCENT_COLOR),
            ("[B] Back", ACCENT_COLOR),
            ("[↑↓] Volume", DIM_COLOR),
            ("[Q] Quit", DIM_COLOR),
        ]
        col_w = (WIDTH - 80) // 3
        for i, (text, color) in enumerate(controls):
            col = i % 3
            row = i // 3
            x = 55 + col * col_w
            y = 410 + row * 28
            draw_text(screen, text, font_small, color, x, y)

        pygame.display.flip()

    player.stop()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
