import pygame
from const import *

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.setup_asset_structure()
        self.load_sounds()
        self.music_playing = False

    def setup_asset_structure(self):
        """Create the asset directory structure if it doesn't exist."""
        if not os.path.exists(ASSETS_DIR):
            os.makedirs(ASSETS_DIR)
        if not os.path.exists(SOUNDS_DIR):
            os.makedirs(SOUNDS_DIR)

    def load_sounds(self):
        """Load sound effects from files."""
        try:
            self.sounds['shoot'] = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'shoot.wav'))
            self.sounds['explosion'] = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'explosion.wav'))
            
            self.sounds['shoot'].set_volume(0.3)
            self.sounds['explosion'].set_volume(0.4)
        except FileNotFoundError:
            print("Warning: Sound files not found. Please ensure sound files are in the assets/sounds directory.")
            print("Required files:")
            print("- assets/sounds/shoot.wav")
            print("- assets/sounds/explosion.wav")
            print("- assets/sounds/background_music.wav")

    def play_sound(self, sound_name):
        """Play a sound effect."""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

    def start_background_music(self):
        """Start playing background music."""
        if not self.music_playing:
            try:
                pygame.mixer.music.load(os.path.join(SOUNDS_DIR, 'background_music.wav'))
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)
                self.music_playing = True
            except FileNotFoundError:
                print("Warning: Background music file not found.")

    def stop_background_music(self):
        """Stop playing background music."""
        if self.music_playing:
            pygame.mixer.music.stop()
            self.music_playing = False