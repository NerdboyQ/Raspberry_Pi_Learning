from flask import render_template, jsonify, url_for, Response, stream_with_context
from IOT_Dashboard import app
from IOT_Dashboard.scripts.bt_ctrlr import * 

@app.route("/")
def render_homepage():
	"""
	Starts homepage for the webapp.
	"""

	return render_template("MainDashboard.html")

@app.route("/bt_scan")
def scan_for_bt_devices():
    print("[views.py] calling bt scan")
    run_bt_scanner()
    print("[view.py] finished bt scan")
    return jsonify({"status":"good"})
