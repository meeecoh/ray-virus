from platformdirs import user_config_path
import json

class Config:
    def __init__(self):
        self.config_path = user_config_path("RayVirus","meeecoh")/"config.json"
        self.data = {}
        
        if self.config_path.exists():
            self.load()
        else:
            # set initial data
            self.set("streamerbot_address", "ws://127.0.0.1:8080")
            self.set("virus_enabled", False)
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            self.save()
    
    def set(self, key:str, val)-> None:
        self.data[key] = val
        
    def get(self, key) -> str:
        return self.data.get(key, None)
    
    def load(self):
        with open(self.config_path, 'r') as f:
            self.data = json.loads(f.read())
    
    def save(self):
        string_data = json.dumps(self.data, indent=4)
        with open(self.config_path, 'w') as f:
            f.write(string_data)
    
    