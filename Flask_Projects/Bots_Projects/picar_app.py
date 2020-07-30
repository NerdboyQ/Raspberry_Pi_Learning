from flask import Flask, render_template, url_for
from datetime import datetime as dt

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('picar_dash.html')

if __name__ == "__main__":
    app.run(debug=True)
