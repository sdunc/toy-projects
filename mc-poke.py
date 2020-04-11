#Stephen Duncanson
#Monte Carlo Pokemon Crystal

from pyautogui import press, typewrite, hotkey, screenshot
import time
import random

possible_keys = ['a','s','return','space','up','right','down','left']

move_counter = 0

write_file = open('mc-poke.txt','a')

while True:
	move_counter +=1
	choice = random.choice(possible_keys)
	press(choice)
	write_file.write(str(choice)+"\t"+str(time.time())+"\n")
	if move_counter % 1000 == 0:
		myScreenshot = screenshot()
		myScreenshot.save(str(move_counter)+'.png')
	#time.sleep(.5)


