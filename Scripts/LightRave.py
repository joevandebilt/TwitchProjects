"""L530 & L630 Example"""

import asyncio
import os
import sys
import random
import time

from tapo import ApiClient
from tapo.requests import Color
from random import randint

from typing import List


async def main():
    tapo_username = os.getenv("TAPO_USERNAME")
    tapo_password = os.getenv("TAPO_PASSWORD")
    ip_address = os.getenv("OFFICE_LAMP_IP_ADDRESS")

    client = ApiClient(tapo_username, tapo_password)
    device = await client.l530(ip_address)

    #Get the status of the Lights
    status = await device.get_device_info()
    
    #Device needs to be on
    if not status.device_on:
        await device.on()

    #Get Available colours
    availableColours = [attr for attr in dir(Color) 
              if not attr.startswith('__')]
    
    delay = 500
    now = time.time()
    while True:
        if time.time() > now+delay:
            #Escape now
            break

        googleColourValue = getattr(Color, availableColours[randint(0, len(availableColours)-1)])
        
        #Get colour from arguments
        await device.set().color(googleColourValue).send(device)
        time.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())