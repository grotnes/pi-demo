from sense_hat import SenseHat

sense = SenseHat()
sense.low_light = True

# Define some colours
g = (0, 255, 0) # Green
b = (0, 0, 0) # Black
r = (255,0,0) # Red
u = (0, 0, 255) # Blue
w = (255,255,255) # White
	
	
# Set up where each colour will display
smiley = [
    b, w, w, w, b, w, w, w,
    b, u, u, w, b, u, u, w,
    b, w, w, w, b, w, w, w,
    b, b, b, b, g, b, b, b,
    b, b, b, b, b, b, b, b,
    b, w, b, b, b, b, w, b,
    b, b, w, w, w, w, b, b,
    b, b, b, b, b, b, b, b
]
# Display these colours on the LED matrix
sense.set_pixels(smiley)	
