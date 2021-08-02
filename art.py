from PIL import Image

def linear_sample(start=0,stop=10,n=10):
        # return n samples between start and stop
        # return in an array
        samples = []
        step_size = (stop-start)//n # integer div step size
        for i in range(start+step_size, stop, step_size):
                samples.append(i)
        return samples

im = Image.open("Henri.jpg")
xsize, ysize = im.size
print(xsize, ysize, im.mode)
# define a border around the image
top_bottom_padding = int(0.08 * ysize) # 10% for top and bottom
right_left_padding = int(0.15 * xsize) # 20% for right and left
print(top_bottom_padding, right_left_padding)

square_size = int(0.03*xsize) # 5% of the bigger edge is square size
spacing_y = int(0.05*max(xsize,ysize)) # 5% of the bigger edge is square size
spacing_x = int(0.05*max(xsize,ysize)) # 5% of the bigger edge is square size

# The region is defined by a 4-tuple, where coordinates are (left, upper, right, lower). 
# The Python Imaging Library uses a coordinate system with (0, 0) in the upper left corner. 
# Also note that coordinates refer to positions between the pixels, 
# so the region in the above example is exactly 300x300 pixels.

# iterate over the image row by row adding to our position until we are at the 
# the other edge

# start in the top left corner 
current_x = right_left_padding
current_y = top_bottom_padding

xn = 10
yn = 15

x_points = linear_sample(start=right_left_padding, stop=int(xsize-right_left_padding-square_size), n=xn)
y_points = linear_sample(start=top_bottom_padding, stop=int(ysize-top_bottom_padding-square_size), n=yn) # eventually do n for x and y with img res

new_image = Image.new("RGB",(square_size*xn, square_size*yn))

# we paste back in to a small image
newy = 0
newx = 0
# these are added two with every crop

white_square = Image.new('RGB', (square_size, square_size), (256, 256, 256))

for y in y_points:
        for x in x_points:
                print(x,y)
                box=(x,y,x+square_size,y+square_size)
                region = im.crop(box)
                #region = region.transpose(Image.ROTATE_90)

                im.paste(white_square,box)

                new_box=(newx,newy,newx+square_size,newy+square_size)
                new_image.paste(region,new_box)
                newx = (newx + square_size) % new_image.size[0]
        newy = (newy+square_size) % new_image.size[1] # make sure it fits
        
                #         break
        #         newx+=square_size
        #         print(newx,newy)
        # newy+=square_size
        # print(newx,newy)

im.show()
new_image.show()

