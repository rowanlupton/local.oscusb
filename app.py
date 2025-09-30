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
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    f.close()
    
    if request.method == 'POST':
        print(request.form)
        return redirect('/')
        #return request.form
    else:
        return render_template('settings.html', settings=settings)

