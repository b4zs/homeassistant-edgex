
from edgex_client import push_data
from hass_client import HomeAssistantClient
from hass_client.models import Event
import os
import asyncio
from dotenv import load_dotenv
import json
import logging

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,  
    format="%(asctime)s [%(name)s] %(message)s"
)
logger = logging.getLogger('app');



class App:
    hass_client: HomeAssistantClient

    def __init__(self):
        self.hass_client = None
        pass    

    async def disconnect(self):
        if self.hass_client and self.hass_client.connected:
            logger.info('hass disconnecting')
            await self.hass_client.disconnect()
            logger.info('hass disconnected')

    async def init_hass(self): 
        logger.info('hass connecting')

        url = os.getenv('HOME_ASSISTANT_URL')
        token = os.getenv('HOME_ASSISTANT_TOKEN')
        
        self.hass_client = HomeAssistantClient(url, token)

        await self.hass_client.connect()
        logger.info('hass connected')

         # start listening will wait forever until the connection is closed/lost
        listener_task = asyncio.create_task(self.hass_client.start_listening())
        await self.hass_client.subscribe_events(self.on_hass_event)

        return listener_task


    async def init_edgex(self):
        logger.info('fake initializing edgex...')


    async def on_hass_event(self, evt: Event) -> None: 
        print(evt)

    async def run(self):
        hass_listener_task = await self.init_hass()
        await self.init_edgex()

        devices = await self.hass_client.get_device_registry()
        f = open('./data/devices.json', 'w+')
        f.write(json.dumps(devices))
        f.close()


        i = 0
        while True:
            logger.debug('running loop')
            await asyncio.sleep(1)
            i = i + 1
            if i>100:
                break
        
    
async def main():
    app = App()
    try:
        await app.run()
    except asyncio.CancelledError:
        logger.info('Cancelled')
    except asyncio.KeyboardInterrupt:
        logger.info('Cancelled')
    finally:
        logger.info('FINALLY')
        await app.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
