# bank_sort_cli.py

from PIL import Image, ImageDraw, ImageFont
import urllib.request
from osrsbox import items_api
import numpy as np
import os

items_banked = []

items = items_api.load()
fnt = ImageFont.truetype('RuneScape-Plain-11.ttf', 15)
padding = 4
color = 'rgb(255,255,0)'
shadow = 'rgb(0,0,0)'


for x in range(30):
	item_to_search_for = str(input("Enter an item to search for: "))
	hm = int(input("How many? "))
	for i in items:
		if item_to_search_for.lower() == (i.name).lower():
			print(str(i.name)+"\t\tID: "+str(i.id)+"\tStack: "+str(i.stacked))
			# first id will always be the regular one
			# then note, then dupe
			# stacking issue seems to be fixed, but code is ugly
			new_id = i.id
			if i.stacked == None:
				items_banked.append((new_id,hm))
				break # to escape adding the other items
			if i.stacked == hm:
				items_banked.append((new_id,hm))
				break # to escape adding the other items
			if i.stacked == 5 and hm >= 5: 
				items_banked.append((new_id,hm))
				break # to escape adding the other items
			else:
				pass

base_image = Image.open("empty_bank2.jpg")

counter = 0

for item in items_banked:

	item_id = item[0]
	how_many = str(item[1])

	# get which number item we are adding, to determine where to place it
	row_number = int(np.floor(counter/8))
	col_number = int(counter%8)
	y_coord = ((row_number+1)*padding)+(row_number*32)
	x_coord = ((col_number+1)*padding)+(col_number*36)
	coords = (x_coord, y_coord)
	shadow_coords = (x_coord+1, y_coord+1)

	# grab the image off this website
	url = "https://www.osrsbox.com/osrsbox-db/items-icons/"+str(item_id)+".png"
	save_as = str(item_id)+".png"
	urllib.request.urlretrieve(url, save_as)

	# open the image object w/ PIL
	next_item_image = Image.open(save_as)

	# paste onto base image, 3rd parameter is for alpha mask
	base_image.paste(next_item_image, coords, next_item_image)

	# write text @ coords
	if int(how_many) != 1: # we dont write the number for only a singular
		d = ImageDraw.Draw(base_image)
		d.text(shadow_coords, how_many, font=fnt, fill=shadow)
		d.text(coords, how_many, font=fnt, fill=color)

	# delete item icon
	os.remove(save_as)

	# add to counter, move to next item
	counter+=1

# save the final bank
base_image.save("output.png")
