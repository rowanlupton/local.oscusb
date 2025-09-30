from flask import Flask
from flask import redirect
from flask import render_template
from flask import request

import json

from usb_osc import usbOSC

usbOSC() # start usb keypress handler

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        return redirect('/')
        #return request.form['name']
    else:
        return render_template('settings.html')

