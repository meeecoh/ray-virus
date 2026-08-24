
import asyncio
import websocket
from websockets.exceptions import ConnectionClosed
from websockets.asyncio.client import connect
import json
from typing import Callable

class StreamerBotClient:
    def __init__(self, address = "ws://127.0.0.1:8080"):
        self.address = address
        self.connected = False
        self.redeems = {}
        return
    
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
    
    async def run_client(self):
        async with connect(self.address) as websocket:
            self.connected = True
            
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
            
            try:
                async for message in websocket:
                    self._handle_message(message)
                    
            except ConnectionClosed:
                print("connection was closed")
            except Exception as e:
                print(f"an error occured : {e}")

