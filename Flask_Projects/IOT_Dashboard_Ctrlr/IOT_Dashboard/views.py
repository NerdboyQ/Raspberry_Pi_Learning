from flask import render_template, jsonify, url_for, Response, stream_with_context
from IOT_Dashboard import app

@app.route("/")
def render_homepage():
	"""
	Starts homepage for the webapp.
	"""

	return render_template("MainDashboard.html")