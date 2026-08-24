from PIL import Image
from pystray import Icon, Menu, MenuItem
from time import sleep

import asyncio
from websockets.exceptions import ConnectionClosed
from websockets.asyncio.client import connect
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
    def __init__(self, address = "ws://127.0.0.1:8080"):
        self.address = address
        
    def on_open(self, ws):
        print("Connection opened!")
        payload = json.dumps(
            {
				"request" : "Subscribe",
				"id" : "ray-virus",
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
    
    async def run_client(self):
        async with connect(self.address) as websocket:
            # send message to server
            payload = json.dumps(
                {
                    "request" : "Subscribe",
                    "id" : "ray-virus-manager",
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
            await websocket.send(payload)
            
            response = await websocket.recv()
            
            
            print(f"From server: : {response}")
            
            try:
                async for message in websocket:
                    print(f"From server: : {message}")
            except ConnectionClosed:
                print("connection was closed")
            except Exception as e:
                print(f"an error occured : {e}")
            
    
            


if __name__ == "__main__":
    
    
    # run system icon in separate thread
    icon = RaySystemIcon()
    icon.run_detached()
    
    # setup streamerbot client
    client = WebSocketClient()
    asyncio.run(client.run_client())
    
    # while True:
    #     if icon.running:
    #         sleep(1/12)
    #         print(icon.virus_enabled)
    #     else:
    #         exit