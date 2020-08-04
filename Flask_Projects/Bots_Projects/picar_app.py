from flask import Flask, render_template, url_for
from datetime import datetime as dt

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('picar_dash.html')

if __name__ == "__main__":
    # adding host '0.0.0.0' & a port, this can serve as a local network server when running.
    app.run(host="0.0.0.0",port=81,debug=True)
