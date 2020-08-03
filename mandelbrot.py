from PIL import Image
import numpy as np



# TODO: Try change color values or a completely different function to map the colors
def create_color(v):
    values = [0, 64, 128, 196]
    b = values[v % 4] 
    g = values[(v//4) % 4] 
    r = values[(v//16) % 4]
    return (r, g, b)


def calc_pixel(w, h, ZOOM, PIXEL_SCALE, XSTART, YSTART, MAX_ITER, initial_z):
    c1 = XSTART + w/PIXEL_SCALE
    c2 = YSTART + h/PIXEL_SCALE

    c = complex(c1, c2)
    z = initial_z
    for i in range(MAX_ITER):
        z = z*z + c
        if abs(z) >= 2:
            return i
    return 0


def create(real=0, imag=0, zoom=1.2, p_scale=200):
    
    ZOOM = zoom # default = 1

    # minimun of 200
    PIXEL_SCALE = 400 * ZOOM
    WIDTH = 3 / ZOOM
    HEIGHT = 3 / ZOOM

    # XSTART = -2 # default = -2
    # YSTART = -1.5 # default = -1.5
    XSTART = -2 / 1.2
    YSTART = -1.5 / 1.2

    # Number of iterations for calculating whether point is convergent
    MAX_ITER = 100

    image_width = int(PIXEL_SCALE*WIDTH)
    image_height = int(PIXEL_SCALE*HEIGHT)

    # initial_z = complex(-.6506302876687291, .3550966973478127) # zoom=60, x=-.76, y=.24
    # initial_z = complex(-.2826053590620101, .6285527181661623) # need to zoom
    # initial_z = complex(0.03400854576513822, -0.6275409288083754) # need to zoom
    initial_z = complex(real, imag)

    image = Image.new('RGB', (image_width, image_height), color = (0, 0, 0))
    pix = image.load()
    print(real, imag)
    for w in range(image_width):
        for h in range(image_height):
            val = calc_pixel(w, h, ZOOM, PIXEL_SCALE, XSTART, YSTART, MAX_ITER, initial_z)
            color = create_color(val)
            pix[w, h] = color

        # prints the row to see progress
        if w % 100 == 0:
            print(w, 'out of', image_width)
    
    # Saves image
    # image.save('static/default.png')
    print('done')
    return image


