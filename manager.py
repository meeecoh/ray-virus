from PIL import Image
from pystray import Icon, Menu, MenuItem
from time import sleep
import websocket
import json
import threading

class RaySystemIcon:
    """
    Window Manager for Ray Virus
    Opens ray viruses
    """
    def __init__(self):
        self.virus_enabled = True
        self.running = False
        
        menu = Menu(
                MenuItem("Enable", self._toggle_virus, checked=lambda x : self.virus_enabled),
                MenuItem("Streamerbot Status : Disconnected", action=None),
                MenuItem("Connect", action=None),
                MenuItem("Config", action=None),
                MenuItem("Exit", self.on_exit)
            )
        
        self.icon = Icon(
            name="RayVirusManager",
            icon=Image.open("you_hacked.png").resize((64, 64)),
            title="Ray Virus Manager",
            menu=menu
        )

    def on_exit(self):
        """Stops tray application loop"""
        self.icon.stop()
        self.running = False
        
    def run_detached(self):
        """Run loop handling events detached"""
        self.running = True
        self.icon.run_detached()
        
    def run(self):
        """Run icon events"""
        self.running = True
        self.icon.run()

    def _toggle_virus(self):
        self.virus_enabled =  not self.virus_enabled

class WebSocketClient:
    def __init__(self, address = "ws://127.0.0.1:8080", password="", enable_debug=False):
        self.address = address
        self.pw = password
        websocket.enableTrace(enable_debug)
        
        self.ws_app = websocket.WebSocketApp(
            self.address,
            on_open=self.on_open,
            on_close=self.on_close,
            on_message=self.on_message,
            on_error=self.on_error
            
        )
    
    def on_open(self, ws):
        print("Connection opened!")
        payload = json.dumps(
            {
				"request" : "Subscribe",
				"id" : "mochi-buddy",
				"events": {
					"Twitch": [
						"RewardRedemption"
					],
					"General": [
						"Custom"
					],
				}
			}
        )
        ws.send(payload)
        
    def on_close(self, ws, close_status_code, close_msg):
        print(f"### Connection closed with status : {close_status_code}")
        print(f"close msg : {close_msg}")
        
    def on_message(self, ws, message):
        try:
            data = json.loads(message)
            print(f"Received: {json.dumps(data, indent=2)}")
        except:
            print(f"Received: {message}")
            
    
    def on_error(self, ws, error):
        print(f"Error: {error}")
        
    def run(self):
        self.ws_app.run_forever()


if __name__ == "__main__":
    
    
    # run system icon in separate thread
    icon = RaySystemIcon()
    icon.run_detached()
    
    client = WebSocketClient()
    client.run()
    
    # while True:
    #     if icon.running:
    #         sleep(1/12)
    #         print(icon.virus_enabled)
    #     else:
    #         exit