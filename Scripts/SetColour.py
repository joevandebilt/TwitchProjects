"""L530 & L630 Example"""

import asyncio
import os
import sys

from tapo import ApiClient
from tapo.requests import Color

from typing import List

async def main():
    tapo_username = os.getenv("TAPO_USERNAME")
    tapo_password = os.getenv("TAPO_PASSWORD")
    ip_address = os.getenv("OFFICE_LAMP_IP_ADDRESS")

    #Command Supplied
    if len(sys.argv) <= 1:
        print("You need to supply a colour")
        exit()

    #Get Colour from our arguments
    colour = sys.argv[1].strip()

    #Does the colour exist in our library
    availableColours = [attr for attr in dir(Color) 
              if not attr.startswith('__')]
    
    if not colour.upper() in (colour.upper() for colour in availableColours):
        seperator = ", "
        print("You must use one of the following colours: {}".format(seperator.join(availableColours)))
        exit()
    

    lower_colours = [item.lower() for item in availableColours]
    index = lower_colours.index(colour.lower())

    googleColourValue = getattr(Color, availableColours[index])

    client = ApiClient(tapo_username, tapo_password)
    device = await client.l530(ip_address)

    #Get the status of the Lights
    status = await device.get_device_info();
    
    #Device needs to be on
    if not status.device_on:
        await device.on()

    #Get colour from arguments
    await device.set().color(googleColourValue).send(device)

    print("Changing the light colour to {}".format(colour))

if __name__ == "__main__":
    asyncio.run(main())