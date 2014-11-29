#!/usr/bin/python
from RepeatedTimer import RepeatedTimer
import picamera
import time
import os.path
import glob
import signal
import sys
import RPi.GPIO as GPIO
import random
import PIL
import io
import ConfigParser

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw


camera = picamera.PiCamera()
config = ConfigParser.ConfigParser()
sequence = 0


def signal_handler(signal, frame):
        print("Exit")
        sys.exit(0)

def init():
	global sequence
	global interval
	
	config.read("./config.ini")
	interval = int(config.get('capture', 'interval'))
	signal.signal(signal.SIGINT, signal_handler)
	root = get_root();
	print "Root is {}".format(root)
	files = glob.glob(root + '/[0-9][0-9][0-9][0-9][0-9].' + config.get('capture', 'format'))
	if len(files) == 0:
		print "No files"
	else:
		newest = "";
		for file in files:
			filename = os.path.basename(file);
			if filename > newest:
				newest = filename;
		sequence = int(newest[:5]) + 1 

def get_root():
	root = time.strftime(config.get('files', 'root'), time.localtime())
	if not os.path.exists(root):
		print "Root does not exist ({}), creating it ...".format(root)
		os.makedirs(root)
	return root

def capture():
	global sequence
	sequence += 1
	root = get_root()
	path = "%s/%05d.%s"  % (root, sequence, config.get('capture', 'format'))
	print "Capturing to %s" % path
	
	if config.getboolean('overlay', 'enable'):
		stream = io.BytesIO()
		camera.capture( stream, format=config.get('capture', 'format') )
		final_overlay_text = time.strftime(config.get('overlay', 'text'), time.localtime())
		stream.seek(0)
		
		image = Image.open(stream)
		draw = ImageDraw.Draw(image)
		font = ImageFont.truetype(config.get('overlay', 'font_name'), int(config.get('overlay', 'font_size')))
		print "Added overlay " + final_overlay_text
		draw.text((int(config.get('overlay', 'offset_x')), int(config.get('overlay', 'offset_y')) ), final_overlay_text, config.get('overlay', 'font_color'),font=font)
		draw = ImageDraw.Draw(image)
		image.save(path)
	else:
		camera.capture( path, format=config.get('capture', 'format') )
	print "Wrote file %s" % path

def main():
	try:
		init()
		camera.vflip = config.getboolean('capture', 'vertical_flip')
		camera.hflip = config.getboolean('capture', 'horizontal_flip')
		try:
			camera.resolution = (int( config.get('capture', 'width') ), int( config.get('capture', 'height') ))
			print "Using resolution %sx%s" % (int( config.get('capture', 'width') ), int( config.get('capture', 'height') ))
		except:
			camera.resolution = (2592, 1944)
			print "Using default resolution (2592x1944)"
#		time.sleep(2)
		camera.start_preview()
		print "Started"
		rt = RepeatedTimer(interval, capture)
		while (True):
			time.sleep(60)
			print "Alive"
	finally:
		camera.stop_preview()
		camera.close()

main()

