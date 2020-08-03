from flask import Flask, escape, request, render_template, url_for, redirect
# from bs4 import BeautifulSoup as bs
from numpy import random as rand
import mandelbrot as mandel
import steganography as steg

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/projects/mandelbrot/', methods=["GET"])
def mandelbrot():

    if 'r' in request.values and 'i' in request.values:
        real = float(request.values['r'])
        imaginary = float(request.values['i'])

        # if 'm' in request.values:
        #     return render_template("mandelbrot.html", image='/static/images/fractal.png', real=real, imag=imaginary)
        
        if 'd' in request.values:
            return render_template("mandelbrot.html", image='/static/images/defaultFractal.png', real=real, imag=imaginary)
        
        image = mandel.create(real, imaginary)
        image.save('static/images/fractal.png')

        return render_template("mandelbrot.html", image='/static/images/fractal.png?' + str(rand.randint(1000)), real=real, imag=imaginary)

    else:
        return render_template("mandelbrot.html", image='/static/images/defaultFractal.png', real=0, imag=0)
    

@app.route('/projects/mandelbrot/calculate/', methods=["POST"])
def calculate():
    if 'go' in request.form:
        real = float(request.form['real'])
        imaginary = float(request.form['imaginary'])

    elif 'rand' in request.form:
        real = rand.rand() * ((-1) ** rand.randint(2))
        imaginary = rand.rand() * ((-1) ** rand.randint(2))

    # r = None
    # i = None
    # size = None
    # if 'r' in request.form:
    #     r = float(request.form['r'])

    # if 'i' in request.form:
    #     i = float(request.form['i'])

    # print(r, real)
    # print(i, imaginary)

    if real == 0 and imaginary == 0:
        return redirect(url_for('mandelbrot', r=real, i=imaginary, d='d'))

    # if real == r and imaginary == i:
    #     return redirect(url_for('mandelbrot', r=real, i=imaginary, m='m'))

    return redirect(url_for('mandelbrot', r=real, i=imaginary))

    
@app.route("/projects/steganography/", methods=["GET"])
def steganography():
    
    return render_template("steganography.html")


@app.route("/projects/steganography/encode/", methods=["POST", "GET"])
def encode():
    img = '/static/images/steganography.png?' + str(rand.randint(1000))
    # message = ''
    hidden = 'hidden'
    if request.method == 'GET':
        if 'show' in request.values:
            hidden = ''
    # if request.method == "GET":
    #     if 'img' in request.form:
    #         img = '../static/steganography.png' + str(rand.randint(1000))
    # img = request.form.get('img')
    # print(img)
    return render_template("encode.html", image=img, hidden=hidden)


@app.route("/projects/steganography/encode/compute/", methods=["POST", "GET"])
def encode_compute():
    message = request.form['message']
    image = request.files['img']
    if not message or not image:
        return redirect(url_for('encode'))
    image.save('static/images/steganography.png')

    binary_string = steg.encode_string(message)
    steg.encode_image('static/images/steganography.png', binary_string)
    
    return redirect(url_for('encode', show='1'))


@app.route("/projects/steganography/decode/", methods=["GET"])
def decode():
    hidden = 'hidden'
    message = ''
    # if request.method == 'POST':
        # print('post')
    if 'message' in request.values:
        # print(request.values['message'])
        message = request.values['message']
        hidden = ''
        
    return render_template("decode.html", hidden=hidden, message=message)


@app.route("/projects/steganography/decode/compute/", methods=["POST", "GET"])
def decode_compute():
    image = request.files['img']
    if not image:
        return redirect(url_for('decode'))
    # image.save('static/steganography.png')

    binary_string = steg.decode_image(image)
    message = steg.decode_string(binary_string)

    # return redirect(url_for('decode', _method="POST", message=message))
    return redirect(url_for('decode', message=message))


@app.route("/projects/", methods=["POST", "GET"])
def projects():
    return render_template("projects.html")

@app.route("/contact/", methods=["POST", "GET"])
def contact():
    return render_template("contact.html")



# set FLASK_APP=hello.py
# $env:FLASK_APP = "hello.py"
# WSL
# export FLASK_APP=home.py
# flask run



if __name__ == '__main__':
    app.run(debug=True)

