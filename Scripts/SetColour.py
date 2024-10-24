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
		print("You need to give me a colour!")
		exit()

	#Get Colour from our arguments
	colour_value = sys.argv[1].strip().strip('#').upper()
	if len(colour_value) == 6 and validHex(colour_value):
		#Now convert out colour
		rgb_value = hex2rgb(colour_value)
		hsv_value = rgb2hsv(*rgb_value)
	else:
		#Try and validate text colour
		colour_map = { 
			'COOLWHITE': (0, 100, 50),
			'DAYLIGHT': (0, 100, 75),
			'IVORY': (0, 100, 100),
			'WARMWHITE': (0, 100, 25),
			'INCANDESCENT': (0, 100, 100),
			'CANDLELIGHT': (0, 100, 25),
			'SNOW': (0, 100, 100),
			'GHOSTWHITE': (0, 100, 100),
			'ALICEBLUE': (208, 5, 75),
			'LIGHTGOLDENROD': (54, 28, 75),
			'LEMONCHIFFON': (54, 19, 75),
			'ANTIQUEWHITE': (0, 100, 70),
			'GOLD': (50, 100, 75),
			'PERU': (29, 69, 75),
			'CHOCOLATE': (30, 100, 75),
			'SANDYBROWN': (27, 60, 75),
			'CORAL': (16, 68, 75),
			'PUMPKIN': (24, 90, 75),
			'TOMATO': (9, 72, 75),
			'VERMILION': (4, 77, 75),
			'ORANGERED': (16, 100, 75),
			'PINK': (349, 24, 75),
			'CRIMSON': (348, 90, 75),
			'DARKRED': (0, 100, 75),
			'HOTPINK': (330, 58, 75),
			'SMITTEN': (329, 67, 75),
			'MEDIUMPURPLE': (259, 48, 75),
			'BLUEVIOLET': (271, 80, 75),
			'INDIGO': (274, 100, 75),
			'LIGHTSKYBLUE': (202, 46, 75),
			'CORNFLOWERBLUE': (218, 57, 75),
			'ULTRAMARINE': (254, 100, 75),
			'DEEPSKYBLUE': (195, 100, 75),
			'AZURE': (210, 100, 75),
			'NAVYBLUE': (240, 100, 75),
			'LIGHTTURQUOISE': (180, 26, 75),
			'AQUAMARINE': (159, 50, 75),
			'TURQUOISE': (174, 71, 75),
			'LIGHTGREEN': (120, 39, 75),
			'LIME': (75, 100, 75),
			'FORESTGREEN': (120, 75, 75),
			'BLACK': (1, 1, 1),
			'WHITE': (360, 1, 100),	
			'RED': (1, 100, 100),	
			'LIME': (120, 100, 100),
			'BLUE': (240, 100, 100),
			'YELLOW': (60, 100, 100),	
			'CYAN': (180, 100, 100),
			'MAGENTA': (300, 100, 100),
			'SILVER': (1, 1, 75),		
			'GRAY': (1, 1, 50),		
			'MAROON': (1, 100, 50),	
			'OLIVE': (60, 100, 50),	
			'GREEN': (120, 100, 50),	
			'PURPLE': (300, 100, 50),	
			'TEAL': (180, 100, 50),	
			'NAVY': (240, 100, 50)
		}

		if not colour_value.upper() in (key.upper() for key in colour_map):
			print("Sorry but I couldn't figure out what that colour is, try using a hex value instead?")
			exit()
		
		hsv_value = colour_map[colour_value.upper()]

	client = ApiClient(tapo_username, tapo_password)
	device = await client.l530(ip_address)

	#Get colour from arguments
	await device.set().hue_saturation(hsv_value[0], hsv_value[1]).brightness(hsv_value[2]).send(device)
	print(f"Changing the light colour to {colour_value}")

def validHex(str):
	validation = set(str)
	acceptable_chars = set('0123456789ABCDEFabcdef')
	if validation.issubset(acceptable_chars):
		return True
	else:
		return False

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
		(60 * ((g - b) / difference) + 360) % 360

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