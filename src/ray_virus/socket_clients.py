
import asyncio
import json
from collections.abc import Callable

from websockets.asyncio.client import connect
from websockets.exceptions import ConnectionClosed, InvalidURI

from .stores import AppStore, ConnectionState


class StreamerBotClient:
    def __init__(self, config, store:AppStore ):
        self.config = config
        self.address = store.state.streamerbot_address
        self.redeems = {}
        self._store = store
        
        self._task: asyncio.Task | None = None
    
    def register_redeem(self, redeem_name, callable : Callable[[dict], None]):
        """Register a function to be called when a redeem activates"""
        self.redeems[redeem_name.lower()] = callable
    
    def _handle_message(self, message):
        """Parses received StreamerBot message and executes callback"""
        try:
            data = json.loads(message)
        except json.JSONDecodeError as e:
            print(f"failed to convert to dict : {e}")
        
        # check if message is an event
        if data.get('event', None):
            
            # execute callback based on title
            redeem_name = data['data']['reward']['title'].lower()
            self.redeems[redeem_name](data)
        
    async def _subscribe_to_events(self, websocket) -> bool:
        """
        Send Subscribe message to socket server  
        returns True if subscribe successful  
        returns False in unsuccessful  
        """
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
        print(response)
        data = json.loads(response)
        return (data["status"] == "ok")

        
    async def _listen(self, websocket):
        """Listen to events after subscription"""
        while self._store.state.running:
            try:
                message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                self._handle_message(message)
            except asyncio.TimeoutError:
                continue
            except ConnectionClosed:
                self._store.update(connection=ConnectionState.DISCONNECTED)
                print("Connection closed by the server.")
                break

    
    async def connect(self):
        self.address = self._store.state.streamerbot_address
        self._store.update(connection=ConnectionState.CONNECTING)
        # try connect and listen
        try:
            async with connect(self.address) as websocket:
                resp = await websocket.recv()
                print(f"response : {resp}")
                self._store.update(connection=ConnectionState.CONNECTED)
                if await self._subscribe_to_events(websocket=websocket):
                    await self._listen(websocket=websocket)
        except ConnectionRefusedError:
            print("Connection Refused : Make sure Streamerbot's Websocket server is running!")
        except InvalidURI:
            print(f"Websocket Connection failed : {self.address} is not a valid URI")
            
        self._store.update(connection=ConnectionState.DISCONNECTED)
        
    def start(self):
        if self._task is None or self._task.done():
            self._task = asyncio.create_task(self.connect())
            
    async def stop(self):
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        self._store.update(connection=ConnectionState.DISCONNECTED)
        
    async def stop_and_restart(self):
        await self.stop()
        self.start()

