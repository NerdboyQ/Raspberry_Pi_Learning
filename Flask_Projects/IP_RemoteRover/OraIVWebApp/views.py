from flask import render_template, jsonify, url_for, Response, stream_with_context
from OraIVWebApp import app, scripts
from flask_sqlalchemy import SQLAlchemy
import requests
from OraIVWebApp.scripts.OraIV import OraIV
from scripts.video_feed import CamFeed
import scripts.OraIV 
import json
import time

picam = None
ora = OraIV()

@app.route("/")
def render_homepage():
	"""
	Starts homepage for the webapp.
	"""

	return render_template("ControlView.html")

@app.route("/drive_cmd/<cmd>", methods=['GET','POST'])
def handle_drive_cmds(cmd):
	speed = 0.5
	print("drive cmd:", cmd)
	if  cmd.find("stop") != -1:
		ora.stop_motors()
	elif cmd.find("drive_F") != -1:
		ora.drive_forward(speed)
	elif cmd.find("drive_R") != -1:
		ora.drive_reverse(speed)
	elif cmd.find("drive_left") != -1:
		ora.drive_left(speed)
	elif cmd.find("drive_right") != -1:
		ora.drive_right(speed)
	elif cmd.find("diagonal_F_left") != -1:
		ora.diagl_forward(speed)
	elif cmd.find("diagonal_F_right") != -1:
		ora.diagr_forward(speed)
	elif cmd.find("diagonal_R_left") != -1:
		ora.diagl_reverse(speed)
	elif cmd.find("diagonal_R_right") != -1:
		ora.diagr_reverse(speed)
	elif cmd.find("rotate_left") != -1:
		ora.rotate_ccw(speed)
	elif cmd.find("rotate_right") != -1:
		ora.rotate_cw(speed)
	else:
		return jsonify({"status" : "error, invalid drive command."}) 
	#ora.test_motors()
	return jsonify({"status": "good"})

@app.route('/vid_feed')
def streamVideo():
	"""
	Handles constant refreshing of picam feed.  
	"""
	global picam
	if picam == None:
		picam = CamFeed()
	else:
		#del picam
		time.sleep(0.1)
		#picam = CamFeed()
		time.sleep(0.1)
	return Response(gen(picam), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen(cam):
	"""
	Triggers the Pi Camera to begin generating the live video feed
	"""
	while (True):
		frame = cam.get_frame()
		yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')