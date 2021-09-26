# a dirty hack to make e-art

from PIL import Image

def sample(start,stop,n):
    samples = []
    step_size = (stop-start)//n # integer div step size
    for i in range(start+step_size, stop, step_size):
        samples.append(i)
    return samples

# open an image from the working dir and get dims
original_image = Image.open("Henri.jpg")
xsize, ysize = original_image.size

# define some padding arounnd the image where we won't cut 
top_bottom_padding = int(0.08 * ysize)
right_left_padding = int(0.15 * xsize)

# define how large we want the squares to be and the spacing between them
square_size = int(0.03*xsize) # 5% of the width is a good size? Do whatever.
spacing_y = int(0.05*max(xsize,ysize)) # 5% of the bigger edge is square size?
spacing_x = int(0.05*max(xsize,ysize)) # 5% of the bigger edge is square size?

# how many squares do we want in x direction (rows) and y (cols)
xn = 10
yn = 15

# get the px coords we want to cut squares out in x and y directions
# when iterated over in nested for loops this will make a grid
x_points = sample(start=right_left_padding, stop=int(xsize-right_left_padding-square_size), n=xn)
y_points = sample(start=top_bottom_padding, stop=int(ysize-top_bottom_padding-square_size), n=yn) 

# initialize a new RGB image of the proper size
new_image = Image.new("RGB",(square_size*xn, square_size*yn))

# these are the coordinates in the new image (above)
# we will paste the rectangles cut from old image onto these coords
newy = 0
newx = 0

# create a white square image to paste onto original image
white_square = Image.new('RGB', (square_size, square_size), (256, 256, 256))

# NOTE ON THESE TUPLES
# The region is defined by a 4-tuple, where coordinates are (left, upper, right, lower). 
# The Python Imaging Library uses a coordinate system with (0, 0) in the upper left corner. 
# Also note that coordinates refer to positions between the pixels, 

for y in y_points:
        for x in x_points:
            print(x,y)
            box=(x,y,x+square_size,y+square_size)
            region = im.crop(box)
            original_image.paste(white_square,box)
            new_box=(newx,newy,newx+square_size,newy+square_size)
            new_image.paste(region,new_box)
            newx = (newx + square_size) % new_image.size[0]
            newy = (newy+square_size) % new_image.size[1] # make sure it fits
                
# show both images, your OS should have a default image viewer
im.show()
new_image.show()



