"""L530 & L630 Example"""

import asyncio
import os

from tapo import ApiClient
from tapo.requests import Color


async def main():
    tapo_username = os.getenv("TAPO_USERNAME")
    tapo_password = os.getenv("TAPO_PASSWORD")
    ip_address = os.getenv("OFFICE_LAMP_IP_ADDRESS")

    client = ApiClient(tapo_username, tapo_password)
    device = await client.l530(ip_address)

    #Get the status of the Lights
    status = await device.get_device_info();

    #If off 
    if (status.device_on):
        print("Turning light off...")
        await device.off()
    
    #else 
    else:
        print("Turning light on...")
        await device.on()

if __name__ == "__main__":
    asyncio.run(main())