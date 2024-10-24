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

    client = ApiClient(tapo_username, tapo_password)
    device = await client.l530(ip_address)

    #Get the status of the Lights
    status = await device.get_device_info()
    
    hex_value = '#16c716'
    rgb_value = hex2rgb(hex_value)
    hsv_value = rgb2hsv(*rgb_value)

    #Device needs to be on
    if not status.device_on:
        await device.on()

    #Get colour from arguments
    await device.set().hue_saturation(hsv_value[0], hsv_value[1]).brightness(hsv_value[2]).send(device)
    return

def hex2rgb(hex_value):
    h = hex_value.strip("#") 
    rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    return rgb

def rgb2hsv(r, g, b):
    # Normalize R, G, B values
    r, g, b = r / 255.0, g / 255.0, b / 255.0

    # h, s, v = hue, saturation, value
    max_rgb = max(r, g, b)    
    min_rgb = min(r, g, b)   
    difference = max_rgb-min_rgb 

    # if max_rgb and max_rgb are equal then h = 0
    if max_rgb == min_rgb:
            h = 0
        
    # if max_rgb==r then h is computed as follows
    elif max_rgb == r:
            h = (60 * ((g - b) / difference) + 360) % 360

    # if max_rgb==g then compute h as follows
    elif max_rgb == g:
            h = (60 * ((b - r) / difference) + 120) % 360

    # if max_rgb=b then compute h
    elif max_rgb == b:
            h = (60 * ((r - g) / difference) + 240) % 360

    # if max_rgb==zero then s=0
    if max_rgb == 0:
            s = 0
    else:
            s = (difference / max_rgb) * 100

    # compute v
    v = max_rgb * 100
    # return rounded values of H, S and V
    return tuple(map(round, (h, s, v)))

if __name__ == "__main__":
    asyncio.run(main())