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
        # load our settings. this maintains file contents as it opens
        with open('settings.json', 'r') as f:
            settings = json.load(f)

        # open our settings file to write. this clears out the file as it opens
        with open('settings.json', 'w') as f:
            formAttrs = request.form
            # write our POSTed attributes into the existing json structure
            for attr in request.form:
                settings[attr]['value'] = formAttrs[attr]

            # write new settings into the original file
            json.dump(settings, f, indent=4)

        # redirect to regular settings page
        return redirect('/')
    else:
        # load our settings, read-only
        with open('settings.json', 'r') as f:
            settings = json.load(f)
            
        return render_template('settings.html', settings=settings)

