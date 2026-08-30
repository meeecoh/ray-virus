import json
from pathlib import Path

from platformdirs import user_config_path

from .stores import AppState
import keyring

KEYRING_SERVICE = "RayVirus"

class Config:
    def __init__(self, BASE_DIR:Path):
        self.config_path = user_config_path("RayVirus","meeecoh")/"config.json"
        print(f"Config Path: {self.config_path}")
        self.data = {}
        self.BASE_DIR = BASE_DIR
        self.ASSET_DIR = BASE_DIR / "assets"
        
        if self.config_path.exists():
            self.load()
        else:
            self._save_default_config()
            
            
    def _save_default_config(self):
        self.set("streamerbot_address", "ws://127.0.0.1:8080")
        self.set("streamerbot_pw", "")
        self.set("redeems_enabled", False)
        self.set("redeem_name", "enable ray virus")
        self.set("auto_start_socket", True)
        self.set("target_monitor_idx", 0)
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.save()
        
    
    def set(self, key:str, val)-> None:
        if key == "streamerbot_pw":
            if val:
                keyring.set_password(KEYRING_SERVICE, "streamerbot_pw", val)
            else:
                try:
                    keyring.delete_password(KEYRING_SERVICE, "streamerbot_pw")
                except:
                    print("Keyring Warning: No Password to delete")
            return
        self.data[key] = val
        
    def get(self, key) -> str:
        if key == "streamerbot_pw":
            return keyring.get_password(KEYRING_SERVICE, "streamerbot_pw")
        return self.data.get(key, None)
    
    def load(self):
        with open(self.config_path, 'r') as f:
            self.data = json.loads(f.read())
    
    def save(self):
        string_data = json.dumps(self.data, indent=4)
        with open(self.config_path, 'w') as f:
            f.write(string_data)
            
    def on_state_update(self, appstate:AppState):
        self.set("redeems_enabled", appstate.redeems_enabled)
        self.set("redeem_name", appstate.redeem_name)
        self.set("streamerbot_address", appstate.streamerbot_address)
        self.set("streamerbot_pw", appstate.streamerbot_pw)
        self.set("auto_start_socket", appstate.auto_start_socket)
        self.set("target_monitor_idx", appstate.target_monitor_idx)
        self.save()
    
    