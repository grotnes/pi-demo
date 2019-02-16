from sense_hat import SenseHat
from time import sleep
#import socket

sense = SenseHat()
sense.low_light = True

def write_ip_addr(event):
	if event.action != 'pressed':
		return
	import netifaces as ni
	ni.ifaddresses('eth0')
	ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
	print ip  # should print "192.168.100.37"
	#print dir(ni)
	print ni.interfaces()

	for interface in ni.interfaces():
		if interface == "lo":
			continue
	
		print "Found interface " + interface
		ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
		print "IP = " + ip
		sense.show_message(interface + ":" + ip)

def smilefjes(event):
	if event.action != 'pressed':
		return
	sense.set_pixel(2, 2, (0, 0, 255))
	sense.set_pixel(4, 2, (0, 0, 255))
	sense.set_pixel(3, 4, (100, 0, 0))
	sense.set_pixel(1, 5, (255, 0, 0))
	sense.set_pixel(2, 6, (255, 0, 0))
	sense.set_pixel(3, 6, (255, 0, 0))
	sense.set_pixel(4, 6, (255, 0, 0))
	sense.set_pixel(5, 5, (255, 0, 0))

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
	init_dot()
	x_calc = 3 # Float number. Knowing cursors exact position
	y_calc = 3 # Float number. Knowing cursors exact position
	x_pos = 3 # Integer, knowing current cursor position
	y_pos = 3 # Integer, knowing current cursor position
	x_previous = 3 # Integer, knowing previous cursor position
	y_previous = 3 # Integer, knowing previous cursor position
	previous_color = sense.get_pixel(x_previous, y_previous)

	while True:
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
		print("x_pos={0}, y_pos={1}, change={2}, x_prev={3}, y_prev={4}".format(x_pos, y_pos, change, x_calc, y_calc))

		if (change == 1):
			sense.set_pixel(x_previous, y_previous, previous_color)
			previous_color = sense.get_pixel(x_pos, y_pos)
			sense.set_pixel(x_pos, y_pos, (255,255,255))
			x_previous = x_pos
			y_previous = y_pos


# Make "write_ip_addr" run when joystick pushed up
sense.stick.direction_up = write_ip_addr

# Make "smilefjes" run when joystick pushed down
sense.stick.direction_down = smilefjes

#write_ip_addr()
#smilefjes()
dot()
