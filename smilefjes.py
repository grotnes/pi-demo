from sense_hat import SenseHat
import time
#import socket

sense = SenseHat()

def write_ip_addr():
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

def smilefjes():
	sense.set_pixel(2, 2, (0, 0, 255))
	sense.set_pixel(4, 2, (0, 0, 255))
	sense.set_pixel(3, 4, (100, 0, 0))
	sense.set_pixel(1, 5, (255, 0, 0))
	sense.set_pixel(2, 6, (255, 0, 0))
	sense.set_pixel(3, 6, (255, 0, 0))
	sense.set_pixel(4, 6, (255, 0, 0))
	sense.set_pixel(5, 5, (255, 0, 0))

write_ip_addr()
smilefjes()
