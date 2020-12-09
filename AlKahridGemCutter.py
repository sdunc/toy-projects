# srd
# gem-cutter.py
# inspired by Ben Land's code

import pyautogui
import numpy as np
from pytesseract import image_to_string
from PIL import Image
import time
import random

pants_color = [47, 191, 154]
shirt_color = [57, 127, 59]

def dist_val(a,b):
    '''returns the sum of squared RGB color distance for each coordinate of a,b normalized such that dist(black,white)=1.0'''
    return np.sum(np.square(a-b),axis=-1) / (3*255**2.0)

def dist_cmp(a,b,tol):
    '''returns a boolean mask for values that satisfy tolerange requirements between a,b
       tolerance requires the quadrature sum of channel distances to be less than tol'''
    return dist_val(a,b) < tol*tol

def find_bitmap(bmp,region,tol=0.01):
    '''similar to find_bitmap_prob but uses the heuristic that each pixel must match better than some tolerance.
       Only returns the coordinates of potential matches.'''
    xs,ys=0,0
    hr,wr=region.shape[:2]
    hs,ws=bmp.shape[:2]
    candidates = np.asarray(np.nonzero(dist_cmp(bmp[0,0],region[:-hs,:-ws],tol)))
    for i in np.arange(0,hs):
        for j in np.arange(0,ws):
            view = region[candidates[0]+i,candidates[1]+j,:]
            passed = dist_cmp(bmp[i,j],view,tol)
            candidates = candidates.T[passed].T
    return candidates[[1,0],:].T

def find_colors(color,region,tol=0.1):
    '''finds all instance of color in region'''
    mask = dist_cmp(region,color,tol)
    found = np.argwhere(mask)[:,[1,0]]
    return found

def move_mouse(x,y,speed=1.0):
    '''moves the mouse to a point'''
    cx,cy = pyautogui.position()
    dt = np.sqrt((cx-x)**2.0+(cy-y)**2.0)/(speed*1000)
    pyautogui.moveTo(x,y,dt,pyautogui.easeOutQuad)

def click_mouse(x,y,left=True,speed=1.0):
    '''moves to and clicks a point'''
    move_mouse(x,y,speed=speed)
    pyautogui.click(button='left' if left else 'right')

def get_random():
    return np.random.random()

anchor = np.asarray(Image.open('anchor.png'))[:,:,:-1] # to get rid of bad shape
desktop = np.array(pyautogui.screenshot())
fb = find_bitmap(anchor, desktop, tol=.01)
print('Vscape logo found at xy: ',fb[0])

anchor_x = fb[0][0]
anchor_y = fb[0][1]

def open_shop():
    try: 
        pants = find_colors(pants_color,desktop,tol=0.01)
    except: 
        pants = find_colors(shirt_color,desktop,tol=0.01)
    print('found '+str(len(pants))+' pixels of Gem trader pants color')
    print('shuffling pants pixels...')
    np.random.shuffle(pants)

    click_mouse(*(pants[0]),left=False, speed=np.random.random())
    rs = get_random()
    print('attempting trade...')
    click_mouse(x=pants[0][0]+np.random.randint(-30,30),y=pants[0][1]+np.random.randint(43,48),left=True, speed=rs)
    nap()

def messy_buy():
    print('messy buy')
    cx,cy = pyautogui.position()
    click_mouse(x=cx+np.random.randint(-50,50), y=cy+np.random.randint(40,80), left=False, speed=get_random())
    click_mouse(*pyautogui.position())

def buy_gems():
    saphire_x = anchor_x+np.random.randint(80,100)
    saphire_y = anchor_y+np.random.randint(100,120)
    emerald_x = anchor_x+np.random.randint(120,140)
    emerald_y = anchor_y+np.random.randint(100,120)  

    e_or_s = random.choice([0,1])
    if e_or_s == 0:
        print('buying saphire first')
        click_mouse(x=saphire_x, y=saphire_y, left=False, speed=get_random())
        messy_buy()
        time.sleep(np.random.random())
        click_mouse(x=emerald_x, y=emerald_y, left=False, speed=get_random())
        messy_buy()
    else:
        print('buying emerald first')
        click_mouse(x=emerald_x, y=emerald_y, left=False, speed=get_random())
        messy_buy()
        time.sleep(np.random.random())
        click_mouse(x=saphire_x, y=saphire_y, left=False, speed=get_random())
        messy_buy()
    nap()

def cut_gems():
    # slot coords
    r1c1_xy = (anchor_x+np.random.randint(560,580), anchor_y+np.random.randint(240,260))
    r1c2_xy = (anchor_x+np.random.randint(606,620), anchor_y+np.random.randint(241,261))  
    r1c3_xy = (anchor_x+np.random.randint(646,663), anchor_y+np.random.randint(241,261))

    # new cutting chisel -> right -> left -> chisel 
    # overshoot on the chisel and left
    print('fancy gem cut order')
    click_mouse(*r1c1_xy, speed=get_random())
    click_mouse(*r1c2_xy, speed=get_random())
    nap()
    click_mouse(*r1c3_xy, speed=get_random())
    click_mouse(*r1c1_xy, speed=get_random())
    nap()

    # old cutting
    #s1ors2 = random.choice([0,1])
    #if s1ors2 == 0:
    #    print('cutting slot2 first')
    #    print('selecting chisel')
    #    click_mouse(x=chisel_x, y=chisel_y, speed=get_random())
    #    time.sleep(get_random())
    #    print('cutting slot2...')
    #    click_mouse(x=s2_x, y=s2_y, speed=get_random())
    #    time.sleep(np.random.random())
    #    print('selecting chisel')
    #    click_mouse(x=chisel_x, y=chisel_y, speed=get_random())
    #    time.sleep(get_random())
    #    print('cutting slot3...')
    #    click_mouse(x=s3_x, y=s3_y, speed=get_random())
    #else:
    #    print('cutting slot3 first')
    #    print('selecting chisel')
    #    click_mouse(x=chisel_x, y=chisel_y, speed=get_random())
    #    time.sleep(get_random())
    #    print('cutting slot3...')
    #    click_mouse(x=s3_x, y=s3_y, speed=get_random())
    #    time.sleep(np.random.random())
    #    print('selecting chisel')
    #    click_mouse(x=chisel_x, y=chisel_y, speed=get_random())
    #    time.sleep(get_random())
    #    print('cutting slot2...')
    #    click_mouse(x=s2_x, y=s2_y, speed=get_random())
    nap()


def messy_sell():
    print('messy sell')
    cx,cy = pyautogui.position()
    click_mouse(x=cx+np.random.randint(-50,50), y=cy+np.random.randint(40,80), left=False, speed=get_random())
    click_mouse(*pyautogui.position())

def nap():
    nap_length = np.random.random()
    print('napping for '+str(nap_length)+'s')
    time.sleep(nap_length+0.5)

def sell_and_buy_gems():
    # todo: fix ranges and get ranges for all slots (in a function?)
    r1c2_xy = (anchor_x+np.random.randint(606,620), anchor_y+np.random.randint(241,261))  
    r1c3_xy = (anchor_x+np.random.randint(646,663), anchor_y+np.random.randint(241,261))
    sell_first = np.random.choice(['left','right'])
    left_sell_mousespeed = np.random.random()
    right_sell_mousespeed = np.random.random()
    if sell_first == 'left':
        print('selling left (slot 2) first at speed '+str(left_sell_mousespeed))
        click_mouse(*r1c2_xy, speed=left_sell_mousespeed, left=False)
        messy_sell()
        nap()
        print('now selling right (slot 3)'+str(right_sell_mousespeed))
        click_mouse(*r1c3_xy, speed=right_sell_mousespeed, left=False)
        time.sleep(np.random.random())
        messy_sell()
    else:
        print('selling right (slot 3)'+str(right_sell_mousespeed))
        click_mouse(*r1c3_xy, speed=right_sell_mousespeed, left=False)
        time.sleep(np.random.random())
        messy_sell()
        nap()
        print('selling left (slot 2) first at speed '+str(left_sell_mousespeed))
        click_mouse(*r1c2_xy, speed=left_sell_mousespeed, left=False)
        time.sleep(np.random.random())
        messy_sell()
    buy_gems()

def close_shop():
    closespeed = np.random.random()
    #nap()
    print('right to buy!')
    close_gem_shop_xy = (anchor_x+np.random.randint(420,470), anchor_y+np.random.randint(62,66))
    print('close shop xy: '+str(close_gem_shop_xy))
    click_mouse(*close_gem_shop_xy, left=True, speed=closespeed)
    nap()

open_shop() # initial shop open and buy happens outside main loop
buy_gems()  # this is so we repeat the game loop at the right point
close_shop()
while True:
    # we start to loop with uncut gems in slots 2/3
    cut_gems()
    open_shop()
    sell_and_buy_gems()
    close_shop()
    time.sleep(1) # wait for restock, time this! 

