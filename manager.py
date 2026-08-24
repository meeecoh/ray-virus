
from time import sleep

import asyncio
from socket_clients import StreamerBotClient
from sys_icon import RaySystemIcon

class Manager:
    def __init__(self):
        pass


if __name__ == "__main__":
    
    # register window types in a list
    
    
    
    # run system icon in separate thread
    icon = RaySystemIcon()
    icon.run_detached()
    
    # setup streamerbot client
    sb_client = StreamerBotClient()
    
    
    asyncio.run(sb_client.run_client())
   