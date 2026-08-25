
from manager import VirusManager, event_loop
from socket_clients import StreamerBotClient
from sys_icon import RaySystemIcon
import asyncio
import window
from config import Config


async def main():
        # setup manager, streamerbot, and systemIcons
        c = Config()
        manager = VirusManager(config=c)
        sb_client = StreamerBotClient(config=c)
        icon = RaySystemIcon(config=c, manager=manager, websocket_client=sb_client)
        
        ### register windows
        manager.register_window("ray_virus", window.RayWindow)
        
        ### register redeem events
        sb_client.register_redeem("enable ray virus", lambda x: manager.show_random_window())
        
        #run system icon and websocket client
        icon.run_detached()
        
        # run event loop async
        await asyncio.gather(
            event_loop(manager, icon),
            sb_client.run_client()
        )
        
        
if __name__ == "__main__":
    asyncio.run(main())
    