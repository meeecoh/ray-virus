
import asyncio

from websockets.exceptions import ConnectionClosed
from websockets.asyncio.client import connect
import json
from typing import Callable
from stores import AppStore, ConnectionState

class StreamerBotClient:
    def __init__(self, config, store:AppStore ):
        self.config = config
        self.address = self.config.get("streamerbot_address")
        self.redeems = {}
        self.store = store
        return

    
    # def set_status(self, status:Status):
    #     self.status = status
    #     self.manager.update_window()
    #     self.icon.update()
    
    def register_redeem(self, redeem_name, callable : Callable[[dict], None]):
        """Register a function to be called when a redeem activates"""
        self.redeems[redeem_name.lower()] = callable
    
    def _handle_message(self, message):
        """Parses received StreamerBot message and executes callback"""
        try:
            data = json.loads(message)
        except Exception as e:
            print(f"failed to convert to dict : {e}")
        
        # check if message is an event
        if data.get('event', None):
            
            # execute callback based on title
            redeem_name = data['data']['reward']['title'].lower()
            self.redeems[redeem_name](data)
    
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
    
    async def run_client(self, state_callable):
        self.store.update(connection=ConnectionState.CONNECTING)
        async with connect(self.address) as websocket:
            self.store.update(connection=ConnectionState.CONNECTED)
            # send subscribe  message to server
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
            
            while state_callable():
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    self._handle_message(message)
                except asyncio.TimeoutError:
                    continue
                except ConnectionClosed:
                    self.store.update(connection=ConnectionState.DISCONNECTED)
                    print("Connection closed by the server.")
                    break
        self.store.update(connection=ConnectionState.DISCONNECTED)

