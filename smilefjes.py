from sense_hat import SenseHat
from time import sleep
from random import randint
import logging
import socket
import threading

# Setting up logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('/home/pi/pi-demo/logfile.txt')
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.debug('#### Started. ####')


########################


sense = SenseHat()
sense.low_light = True

# Define global variables
active = "Dot" # Active subprogram
busy   = False  # Status

def telnet_client():
	wlan = ""
	while wlan == "":
		import netifaces as ni
		interfaces = ni.interfaces()
		logger.debug("Searching for IP in ")
		logger.debug(interfaces)

		for interface in ni.interfaces():
			if interface != "wlan0":
				continue
	
			logger.debug("Found interface " + interface + ", ")
			try:
				ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
				logger.debug("IP = \"" + ip +"\"")
				wlan = str(ip)
			except:
				pass
		if wlan == "":
			logger.debug("Waiting for net.")
			sleep(5)

	connected = False
	while not connected:
		try:
			logger.debug("Binding to interface...")
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.bind((wlan, 2323))
			connected = True
		except Exception as e:
			logging.debug('Could not connect: ' + str(e))
			sleep(5)
			connected = False

	logger.debug("Listening for incoming connections.")
	s.listen(1)
	conn, addr = s.accept()
	connected = True
	logger.info("Incoming Telnet from ")
	logger.info(addr)
	received = ""
	while connected:
		data = conn.recv(1024)
		if (ord(data[0]) != 13):
			received += data
			conn.sendall(data) # Echo
			continue
			
		logger.info(received)
		if received.startswith("quit"):
			s.shutdown(socket.SHUT_RDWR)
			s.close()
			connected = False
			logger.info("Closed connection.")
			sleep(1)
		received = ""	 # Clear the received string

def write_ip_addr():
	logger.info("Starts Write IP addr")
	try:
		global busy, active, f
		busy = True
		active = ""
		import netifaces as ni
		logger.debug("Listing interfaces.")
		interfaces = ni.interfaces()
		#print(interfaces)
		logger.debug("Found interfaces ")
		logger.debug(interfaces)

		for interface in ni.interfaces():
			if interface == "lo":
				continue
	
			#print "Found interface " + interface
			logger.info("Found interface " + interface + ", ")
			#print(ni.ifaddresses(interface))
			try:
				ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
				#print "IP = " + ip
				logger.info("IP = " + ip +".")
				sense.show_message(interface + ":" + ip)
			except:
				pass
		busy = False
	except Exception as e:
		logging.error('Error occurred ' + str(e))

def smilefjes():
	global busy, active
	logger.info("Starts Smilefjes.")
	busy = True
	active = ""
	sense.clear()
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
	logger.info("Starts Dot")
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
	global active
	global busy
	global f
	if event.action == 'pressed' and busy == False:
		logger.info("Got event " + event.direction + ". Busy = ")
		logger.info(busy)
		logger.info("active was '"+active+"'")
		if event.direction == 'up':
			active = "IP"
		if event.direction == 'down':
			active = "Smilefjes"
		if event.direction == 'left':
			active = "Dot"
		if event.direction == 'right':
			active = "Magic"
		if event.direction == 'middle':
			active = "Quit"
		logger.info("Active is now " + active)
		logger.debug("Requested action "+active+".")
	else:
		logger.info("Keypress ignored. Action="+event.action+" Busy =")
		logger.info(busy)
		logger.info("active was '"+active+"'")

def magic_eigth():
	logger.info("Starts Magic Eigth")
	global active,busy
	active = "Magic"
	busy = False
	r = (255,0,0)
	w = (255,255,255)
	b = (0,0,255)
	magic_message = [
		"Ta en kake",
		"Spis lunch",
		"Tid for lekser",
		"En gang til",
		"Hopp over et kast",
		"Syng en sang",
		"Fortell en vits",
		"Sett deg ned",
		"Trust me",
		"Have fun"
	]
	# Set up where each colour will display
	pause_picture = [
	  [
	    b, b, b, b, b, b, b, b,
	    b, b, b, b, b, b, b, b,
	    b, b, b, b, b, b, b, b,
	    b, b, b, w, b, b, b, b,
	    b, b, b, b, b, b, b, b,
	    b, b, b, b, b, b, b, b,
	    b, b, b, b, b, b, b, b,
	    b, b, b, b, b, b, b, b
	  ], [
	    b, b, b, b, b, b, b, b,
	    b, b, b, b, b, b, b, b,
	    b, b, b, b, b, b, b, b,
	    b, b, b, b, b, b, b, b,
	    b, b, b, w, b, b, b, b,
	    b, b, b, b, b, b, b, b,
	    b, b, b, b, b, b, b, b,
	    b, b, b, b, b, b, b, b
	  ], [
	    b, b, b, b, b, b, b, b,
	    b, b, b, b, b, b, b, b,
	    b, b, b, b, b, b, b, b,
	    b, b, b, b, b, b, b, b,
	    b, b, b, b, w, b, b, b,
	    b, b, b, b, b, b, b, b,
	    b, b, b, b, b, b, b, b,
	    b, b, b, b, b, b, b, b
	  ], [
	    b, b, b, b, b, b, b, b,
	    b, b, b, b, b, b, b, b,
	    b, b, b, b, b, b, b, b,
	    b, b, b, b, w, b, b, b,
	    b, b, b, b, b, b, b, b,
	    b, b, b, b, b, b, b, b,
	    b, b, b, b, b, b, b, b,
	    b, b, b, b, b, b, b, b
	  ]
	]

	p = 0
	while active == "Magic":
		# Display wait-screen
		sense.set_pixels(pause_picture[p])
		p += 1
		if p>= 4:
			p = 0
		sleep(0.1)

		# Check if PI is shaken
		acceleration = sense.get_accelerometer_raw()
		x = acceleration['x']
		y = acceleration['y']
		z = acceleration['z']

		x = abs(x)
		y = abs(y)
		z = abs(z)

		if x > 3 or y > 3 or z > 3:
			shake = True
		else:
			shake = False

		# Write message if PI is shaken
		if shake:
			random = randint(0,9)
			busy = True
			sense.show_message(magic_message[random])
			sleep(1)
			busy = False

# Make handles for joystick events
sense.stick.direction_up     = handle_joystick
sense.stick.direction_down   = handle_joystick
sense.stick.direction_left   = handle_joystick
sense.stick.direction_right  = handle_joystick
sense.stick.direction_middle = handle_joystick

busy = False
active = "Dot"
threading.Thread(target=telnet_client).start()

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
	if active == "Magic":
		magic_eigth()
	if active == "Quit":
		sense.clear((120,0,255))
		#quit()
	#active = ""
	busy = False
	logger.debug("Venter paa input")
	sleep(0.1)
