from sense_hat import SenseHat
from time import sleep
#import socket

sense = SenseHat()
sense.low_light = True

# Define global variables
active = "dot" # Active subprogram
busy   = False  # Status

def write_ip_addr():
	print("Starts Write IP addr")
	global busy, active
	busy = True
	active = ""
	import netifaces as ni
	#ni.ifaddresses('eth0')
	#ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
	#print ip  # should print "192.168.100.37"
	#print dir(ni)
	print ni.interfaces()

	for interface in ni.interfaces():
		if interface == "lo":
			continue
	
		print "Found interface " + interface
		print(ni.ifaddresses(interface))
		try:
			ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
			print "IP = " + ip
			sense.show_message(interface + ":" + ip)
		except:
			pass
	busy = False

def smilefjes():
	global busy, active
	print("Starts Smilefjes.")
	busy = True
	active = ""
	sense.set_pixel(2, 2, (0, 0, 255))
	sense.set_pixel(4, 2, (0, 0, 255))
	sense.set_pixel(3, 4, (100, 0, 0))
	sense.set_pixel(1, 5, (255, 0, 0))
	sense.set_pixel(2, 6, (255, 0, 0))
	sense.set_pixel(3, 6, (255, 0, 0))
	sense.set_pixel(4, 6, (255, 0, 0))
	sense.set_pixel(5, 5, (255, 0, 0))
	busy = False

def init_dot():
	# Draws the screen background for the "dot" program
	# Define some colours
	g = (0, 255, 0) # Green
	b = (0, 0, 0) # Black
	r = (255,0,0) # Red
	
	
	# Set up where each colour will display
	creeper_pixels = [
	    r, r, r, r, r, r, r, r,
	    r, g, g, g, g, g, g, r,
	    r, g, g, g, g, g, g, r,
	    r, g, g, g, g, g, g, r,
	    r, g, g, g, g, g, g, r,
	    r, g, g, g, g, g, g, r,
	    r, g, g, g, g, g, g, r,
	    r, r, r, r, r, r, r, r
	]
	# Display these colours on the LED matrix
	sense.set_pixels(creeper_pixels)	
	
def dot():
	# Make a dot that moves when you flip
	global busy, active
	print("Starts Dot")
	busy = True
	active = "Dot"
	init_dot()
	x_calc = 3 # Float number. Knowing cursors exact position
	y_calc = 3 # Float number. Knowing cursors exact position
	x_pos = 3 # Integer, knowing current cursor position
	y_pos = 3 # Integer, knowing current cursor position
	x_previous = 3 # Integer, knowing previous cursor position
	y_previous = 3 # Integer, knowing previous cursor position
	previous_color = sense.get_pixel(x_previous, y_previous)
	busy = False

	while active == "Dot":
		acceleration = sense.get_accelerometer_raw()
		x = acceleration['x']
		y = acceleration['y']
		z = acceleration['z']
	
		x_calc += x
		y_calc += y

		x_pos = int(round(x_calc, 0))
		y_pos = int(round(y_calc, 0))

		# Stop dot from going over edge
		if (x_pos < 0):
			x_pos = 0
			x_calc = 0
		if (y_pos < 0):
			y_pos = 0
			y_calc = 0
		if (x_pos > 7):
			x_pos = 7
			x_calc = 7
		if (y_pos > 7):
			y_pos = 7
			y_calc = 7

		if (x_pos - x_previous != 0):
			change = 1
		elif (y_pos - y_previous != 0):
			change = 1
		else:
			change = 0

		#print("x_pos={0}, y_pos={1}, change={2}, x={3}, y={4}, z={5}".format(x_pos, y_pos, change, x, y, z))
		#print("x_pos={0}, y_pos={1}, change={2}, x_prev={3}, y_prev={4}".format(x_pos, y_pos, change, x_calc, y_calc))

		if (change == 1):
			sense.set_pixel(x_previous, y_previous, previous_color)
			previous_color = sense.get_pixel(x_pos, y_pos)
			sense.set_pixel(x_pos, y_pos, (255,255,255))
			x_previous = x_pos
			y_previous = y_pos


def handle_joystick(event):
	global active, busy
	if event.action == 'pressed':# and busy == False:
		if event.direction == 'up':
			active = "IP"
		if event.direction == 'down':
			active = "Smilefjes"
		if event.direction == 'left':
			active = "Dot"
		if event.direction == 'right':
			active = "Blue"
		if event.direction == 'middle':
			active = "Quit"

def blue():
	print("Starts Blue")
	sense.clear((0,0,255))

# Make handles for joystick events
sense.stick.direction_up     = handle_joystick
sense.stick.direction_down   = handle_joystick
sense.stick.direction_left   = handle_joystick
sense.stick.direction_right  = handle_joystick
sense.stick.direction_middle = handle_joystick

busy = False
active = "Dot"
while True:
	if active == "IP":
		sense.clear((0,0,255))
		write_ip_addr()
	if active == "Smilefjes":
		sense.clear((0,0,255))
		smilefjes()
	if active == "Dot":
		sense.clear((0,0,255))
		dot()
	if active == "Blue":
		blue()
	if active == "Quit":
		sense.clear((0,0,255))
		quit()
	print("Venter paa input")
	sleep(0.5)
