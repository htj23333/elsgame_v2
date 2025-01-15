import pygame
import os

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.sound_enabled = True
        self.load_sounds()
        
    def load_sounds(self):
        """加载所有音效"""
        sound_dir = os.path.join('assets', 'sounds')
        # 确保音效目录存在
        os.makedirs(sound_dir, exist_ok=True)
        
        sound_files = {
            'move': 'move.wav',
            'rotate': 'rotate.wav',
            'clear': 'clear.wav',
            'drop': 'drop.wav',
            'pause': 'pause.wav',
            'start': 'start.wav',
            'gameover': 'gameover.wav'
        }
        
        # 如果音效文件不存在，创建空文件
        for filename in sound_files.values():
            filepath = os.path.join(sound_dir, filename)
            if not os.path.exists(filepath):
                open(filepath, 'w').close()
            
        for sound_name, filename in sound_files.items():
            self.load_sound(sound_name, os.path.join(sound_dir, filename))
            
    def load_sound(self, sound_name, filepath):
        """加载单个音效"""
        try:
            self.sounds[sound_name] = pygame.mixer.Sound(filepath)
            self.sounds[sound_name].set_volume(0.3)
        except Exception as e:
            print(f"Warning: Could not load sound {filepath}: {e}")
            self.sounds[sound_name] = None
            
    def play_sound(self, sound_name):
        if self.sound_enabled and sound_name in self.sounds and self.sounds[sound_name]:
            try:
                self.sounds[sound_name].play()
            except:
                pass 