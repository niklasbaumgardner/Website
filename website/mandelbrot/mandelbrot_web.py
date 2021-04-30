from flask import Blueprint, render_template, session, request, url_for, redirect
import uuid
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
from numpy import random as rand
# import python_files.mandelbrot as mandel
from PIL import Image
import numpy as np
import os


mandelbrot_web = Blueprint('mandelbrot_web', __name__)


@mandelbrot_web.route('/projects/mandelbrot/', methods=["GET"])
def mandelbrot():
    scheduler = BackgroundScheduler()
    scheduler.start()
    try:
        session['uid']
    except:
        session['uid'] = uuid.uuid4()

    if 'r' in request.values and 'i' in request.values:
        real = float(request.values['r'])
        imaginary = float(request.values['i'])
        
        image = create(real, imaginary)
        filename = 'website/static/images/' + str(session['uid']) + 'fractal.png'
        # image.save('static/images/fractal.png')
        image.save(filename)

        time = datetime.datetime.now() + datetime.timedelta(seconds = 10)
        if scheduler.get_job(filename):
            scheduler.reschedule_job(job_id=filename, trigger='date', run_date=time)
            print(f'job rescheduled for {time}')
        else:
            scheduler.add_job(delete_file, args=[filename], trigger='date', run_date=time, id=filename)
            print(f'job scheduled for {time}')

        return render_template("mandelbrot.html", image='/' + filename[8:] + '?' + str(rand.randint(1000)), real=real, imag=imaginary)

    else:
        return render_template("mandelbrot.html", image='/static/images/defaultFractal.png', real=0, imag=0)


@mandelbrot_web.route('/projects/mandelbrot/calculate/', methods=["POST"])
def calculate():
    if 'go' in request.form:
        real = float(request.form['real'])
        imaginary = float(request.form['imaginary'])

    elif 'rand' in request.form:
        real = rand.rand() * ((-1) ** rand.randint(2))
        imaginary = rand.rand() * ((-1) ** rand.randint(2))

    if real == 0 and imaginary == 0:
        return redirect(url_for('mandelbrot_web.mandelbrot'))

    return redirect(url_for('mandelbrot_web.mandelbrot', r=real, i=imaginary))


def delete_file(filename):
    try:
        os.remove(filename)
        print(f'{filename} deleted')
    except FileNotFoundError:
        print(f'{filename} not found')


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