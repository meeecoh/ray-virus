import pygame
from pathlib import Path
from typing import Dict
from ray_virus.stores import AppState

class SoundPlayer:
    def __init__(self, asset_dir:Path):
        self._enabled = True 
        
        try:
            pygame.mixer.init()
        except pygame.error as e:
            print(f"Audio disabled: could not init mixer ({e})")
            self._enabled = False
            return
        
        self._sounds : Dict[str, pygame.mixer.Sound] = {}
        self._asset_dir : Path = asset_dir
        
        # load up files already
        ext = (".mp3", ".wav", ".ogg")
        for path in self._asset_dir.iterdir():
            path : Path 
            if (path.is_file()) and (path.suffix in ext):
                self.load(path.name)
                print(f"loaded sound : {path.name}")
        
    def update_volume(self, volume:float):
        for sound in self._sounds.values():
            sound : pygame.mixer.Sound
            sound.set_volume(volume)
        
    def load(self, filename):
        if not self._enabled:
            return
        self._sounds[filename] = pygame.mixer.Sound(self._asset_dir / filename)
        
    def play(self, name) -> pygame.Channel | None:
        if not self._enabled:
            return None
        if name in self._sounds:
            return self._sounds[name].play()
        
    def on_state_update(self, appstate:AppState):
        volume = appstate.audio_lvl / 100
        self.update_volume(volume)