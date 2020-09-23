from flask import Flask, escape, request, render_template, url_for, redirect, session, flash
from flask_mail import Mail, Message
from numpy import random as rand
import mandelbrot as mandel
import steganography as steg
import os
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import uuid


app = Flask(__name__)

app.secret_key = os.urandom(24)

scheduler = BackgroundScheduler()
scheduler.start()

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/projects/mandelbrot/', methods=["GET"])
def mandelbrot():
    try:
        session['uid']
    except:
        session['uid'] = uuid.uuid4()

    if 'r' in request.values and 'i' in request.values:
        real = float(request.values['r'])
        imaginary = float(request.values['i'])
        
        image = mandel.create(real, imaginary)
        filename = 'static/images/' + str(session['uid']) + 'fractal.png'
        # image.save('static/images/fractal.png')
        image.save(filename)

        time = datetime.datetime.now() + datetime.timedelta(seconds = 10)
        if scheduler.get_job(filename):
            scheduler.reschedule_job(job_id=filename, trigger='date', run_date=time)
            print(f'job rescheduled for {time}')
        else:
            scheduler.add_job(delete_file, args=[filename], trigger='date', run_date=time, id=filename)
            print(f'job scheduled for {time}')

        return render_template("mandelbrot.html", image='/' + filename + '?' + str(rand.randint(1000)), real=real, imag=imaginary)

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

    if real == 0 and imaginary == 0:
        return redirect(url_for('mandelbrot'))

    return redirect(url_for('mandelbrot', r=real, i=imaginary))
    
    
@app.route("/projects/steganography/", methods=["GET"])
def steganography():
    
    return render_template("steganography.html")


@app.route("/projects/steganography/encode/", methods=["GET"])
def encode():
    try:
        session['uid']
    except:
        session['uid'] = uuid.uuid4()

    img = ''
    show = False
    if 'show' in request.values and request.values['show'] == 'True':
        show = True
        img = '/' + session['steganography_image'] + '?' + str(rand.randint(1000))
    
    return render_template("encode.html", image=img, show=show)


@app.route("/projects/steganography/encode/compute/", methods=["POST"])
def encode_compute():
    message = request.form['message']
    image = request.files['img']
    if not message or not image:
        return redirect(url_for('encode'))
    
    filename = 'static/images/' + str(session['uid']) + image.filename.split('.')[0] + '.png'
    image.save(filename)
    session['steganography_image'] = filename
    
    binary_string = steg.encode_string(message)
    image = steg.encode_image(filename, binary_string)

    time = datetime.datetime.now() + datetime.timedelta(minutes = 4)
    if scheduler.get_job(filename):
        scheduler.reschedule_job(job_id=filename, trigger='date', run_date=time)
        print(f'job rescheduled for {time}')
    else:
        scheduler.add_job(delete_file, args=[filename], trigger='date', run_date=time, id=filename)
        print(f'job scheduled for {time}')
    
    return redirect(url_for('encode', show='True'))

def delete_file(filename):
    os.remove(filename)
    print(f'{filename} deleted')


@app.route("/projects/steganography/decode/", methods=["GET"])
def decode():
    hidden = 'hidden'
    message = ''
    
    if 'message' in request.values:
        message = request.values['message']
        hidden = ''
        
    return render_template("decode.html", hidden=hidden, message=message)


@app.route("/projects/steganography/decode/compute/", methods=["POST"])
def decode_compute():
    image = request.files['img']
    if not image:
        return redirect(url_for('decode'))
    
    binary_string = steg.decode_image(image)
    message = steg.decode_string(binary_string)

    return redirect(url_for('decode', message=message))


@app.route("/projects/", methods=["GET"])
def projects():
    return render_template("projects.html")

@app.route("/contact/", methods=["GET"])
def contact():
    return render_template("contact.html")

@app.route("/send/", methods=["POST"])
def send():

    try:
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        
        emailMessage = Message(subject=subject, sender='noreply', recipients=[email, "baumga91@msu.edu"], body=message)

        mail.send(emailMessage)

        flash('Email successfully sent!', 'w3-pale-green')
    except:
        flash('Email failed to send', 'w3-pale-red')

    return redirect(url_for('contact'))




# set FLASK_APP=hello.py
# $env:FLASK_APP = "hello.py"
# WSL
# export FLASK_APP=home.py
# flask run


# $site->dbConfigure('mysql:host=mysql-user.cse.msu.edu;dbname=baumga91',
#         'baumga91',       // Database user
#         'password',     // Database password
#         '');            // Table prefix


if __name__ == '__main__':
    # app.run(debug=True)
    app.run()

