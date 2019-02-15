"""
Demo of Python with Raspberry PI using SenseHat
By: Erik Grøtnes
Created 15.02.2019

"""

from sense_hat import SenseHat
sense = SenseHat()

blue = (0, 0, 255)
yellow = (255, 255, 0)

while True:
  sense.show_message("IP address...", text_colour=yellow, back_colour=blue, scroll_speed=0.05)
