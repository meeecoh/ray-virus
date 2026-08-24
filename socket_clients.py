
import asyncio
from websockets.exceptions import ConnectionClosed
from websockets.asyncio.client import connect
import json

class StreamerBotClient:
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
                