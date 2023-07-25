import os, sys
from flask import render_template, jsonify, url_for, Response, stream_with_context
from IOT_Dashboard import app
from IOT_Dashboard.scripts.bt_ctrlr import * 

bt_devices = []

@app.route("/")
def render_homepage():
	"""
	Starts homepage for the webapp.
	"""

	return render_template("MainDashboard.html")

@app.route("/bt_rst")
def reset_bluetooth():
    print("Resetting Bluetooth Service...")
    os.system("sudo systemctl restart bluetooth")
    return jsonify({"status" : "reset complete"})


@app.route("/bt_scan")
def scan_for_bt_devices():
    print("[views.py] calling bt scan")
    global bt_devices
    bt_devices = run_bt_scanner()
    print("[view.py] finished bt scan")
    scan_results = []
    for dev in bt_devices:
        scan_results.append(vars(dev))

    return jsonify({"status":"good", "bt_devices": scan_results})

@app.route("/bt_connect/<dev_name>")
def connect_bt_dev(dev_name):
    global bt_devices
    print(f"[views.py] connect request sent for {dev_name}")
    for dev in bt_devices:
        print(f"Checking for dev: {dev.name}")
        if dev_name == dev.name:
            print(f"[views.pt] attempting to connect to bt device: {dev_name}")
            dev.connect()
            break

    return jsonify({"status": "successful"})
