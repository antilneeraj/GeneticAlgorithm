import pygame
import os
from src.utils.constants import *

class AssetLoader:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.fonts = {}
        
    def load_all_assets(self):
        self.load_images()
        self.load_sounds()
        self.load_fonts()
        
    def load_images(self):
        try:
            # Load bird sprites for all types and flap states
            for bird_type in BIRD_TYPES.values():
                self.images[f"{bird_type}_sprites"] = [
                    pygame.image.load(os.path.join(IMAGES_DIR, f"{bird_type}-downflap.png")).convert_alpha(),
                    pygame.image.load(os.path.join(IMAGES_DIR, f"{bird_type}-midflap.png")).convert_alpha(),
                    pygame.image.load(os.path.join(IMAGES_DIR, f"{bird_type}-upflap.png")).convert_alpha()
                ]
            
            # Load pipe sprites
            for pipe_name, pipe_file in PIPE_TYPES.items():
                pipe_img = pygame.image.load(os.path.join(IMAGES_DIR, pipe_file)).convert_alpha()
                self.images[f"pipe_{pipe_name.lower()}"] = pipe_img
                
            # Load backgrounds
            for bg_name, bg_file in BACKGROUND_TYPES.items():
                self.images[f"background_{bg_name.lower()}"] = pygame.image.load(
                    os.path.join(IMAGES_DIR, bg_file)).convert()
                    
            # Load ground/base
            self.images["base"] = pygame.image.load(
                os.path.join(IMAGES_DIR, "base.png")).convert()
                
            # Load UI elements
            self.images["gameover"] = pygame.image.load(
                os.path.join(IMAGES_DIR, "gameover.png")).convert_alpha()
            self.images["message"] = pygame.image.load(
                os.path.join(IMAGES_DIR, "message.png")).convert_alpha()
                
            # Load number sprites (0-9)
            self.images["numbers"] = {}
            for i in range(10):
                self.images["numbers"][i] = pygame.image.load(
                    os.path.join(IMAGES_DIR, f"{i}.png")).convert_alpha()
                    
            print("✅ All images loaded successfully")
            
        except pygame.error as e:
            print(f"❌ Error loading images: {e}")
            
    def load_sounds(self):
        try:
            pygame.mixer.init()
            sound_files = {
                "wing": "wing.wav",
                "hit": "hit.wav", 
                "die": "die.wav",
                "point": "point.wav",
                "swoosh": "swoosh.wav"
            }
            
            for sound_name, sound_file in sound_files.items():
                self.sounds[sound_name] = pygame.mixer.Sound(
                    os.path.join(SOUNDS_DIR, sound_file))
                self.sounds[sound_name].set_volume(SOUND_VOLUME)
                
            print("✅ All sounds loaded successfully")
            
        except pygame.error as e:
            print(f"❌ Error loading sounds: {e}")
            
    def load_fonts(self):
        try:
            self.fonts["small"] = pygame.font.Font(None, 24)
            self.fonts["medium"] = pygame.font.Font(None, 36)
            self.fonts["large"] = pygame.font.Font(None, 48)
            print("✅ Fonts loaded successfully")
            
        except pygame.error as e:
            print(f"❌ Error loading fonts: {e}")
            
    def get_bird_sprites(self, bird_type="BLUE"):
        return self.images.get(f"{BIRD_TYPES[bird_type]}_sprites", [])
        
    def get_pipe_sprite(self, pipe_type="GREEN"):
        return self.images.get(f"pipe_{pipe_type.lower()}")
        
    def get_background(self, bg_type="DAY"):
        return self.images.get(f"background_{bg_type.lower()}")
        
    def get_sound(self, sound_name):
        return self.sounds.get(sound_name)
        
    def get_font(self, size):
        return self.fonts.get(size)