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
        with open('settings.json', 'r') as f:
            settings = json.load(f)
        with open('settings.json', 'w') as f:
            #print('old settings: ',settings)
            formAttrs = request.form
            for attr in request.form:
                settings[attr]['value'] = formAttrs[attr]
            
            print('new settings: ',settings)
            json.dump(settings, f, indent=4)
            #f.close()
        
        return redirect('/')
    else:
        with open('settings.json', 'r') as f:
            settings = json.load(f)
        f.close()
        return render_template('settings.html', settings=settings)
        return 'hi'

