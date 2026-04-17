import pygame
import os


class MusicPlayer:


    def __init__(self, music_folder="music"):
        self.music_folder = music_folder
        self.playlist = []  # List of file paths
        self.current_index = 0  # Index of currently selected track
        self.is_playing = False
        self.volume = 0.7  # Default volume (0.0 to 1.0)

        pygame.mixer.init()
        pygame.mixer.music.set_volume(self.volume)

        self._load_playlist()

    def _load_playlist(self):
        if not os.path.exists(self.music_folder):
            os.makedirs(self.music_folder)

        for filename in sorted(os.listdir(self.music_folder)):
            if filename.lower().endswith((".mp3", ".wav", ".ogg")):
                full_path = os.path.join(self.music_folder, filename)
                self.playlist.append(full_path)

    def get_track_name(self):
        if not self.playlist:
            return "No tracks found"
        path = self.playlist[self.current_index]
        return os.path.splitext(os.path.basename(path))[0]

    def get_status(self):
        """Return current playback status string."""
        if not self.playlist:
            return "No tracks in playlist"
        if self.is_playing:
            return "▶  Playing"
        return "⏹  Stopped"

    def play(self):
        """Play the current track."""
        if not self.playlist:
            return
        track = self.playlist[self.current_index]
        pygame.mixer.music.load(track)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()
        self.is_playing = True

    def stop(self):
        """Stop playback."""
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        """Switch to the next track."""
        if not self.playlist:
            return
        self.current_index = (self.current_index + 1) % len(self.playlist)
        if self.is_playing:
            self.play()

    def previous_track(self):
        """Switch to the previous track."""
        if not self.playlist:
            return
        self.current_index = (self.current_index - 1) % len(self.playlist)
        if self.is_playing:
            self.play()

    def volume_up(self):
        self.volume = min(1.0, self.volume + 0.1)
        pygame.mixer.music.set_volume(self.volume)

    def volume_down(self):
        self.volume = max(0.0, self.volume - 0.1)
        pygame.mixer.music.set_volume(self.volume)

    def get_playlist_info(self):
        return [os.path.splitext(os.path.basename(p))[0] for p in self.playlist]

    def check_track_ended(self):
        if self.is_playing and not pygame.mixer.music.get_busy():
            self.next_track()
