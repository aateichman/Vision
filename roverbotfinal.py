## Importing Libraries
import RPi.GPIO as gpio
import time
from Tkinter import *
from threading import Thread

##Setting up output pins on Raspberry Pi
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(22, gpio.OUT)
gpio.setup(4, gpio.OUT)
gpio.setup(17, gpio.OUT)
gpio.setup(27, gpio.OUT)
gpio.setup(18, gpio.OUT)
gpio.setup(23, gpio.OUT)
gpio.setup(24, gpio.OUT)
gpio.setup(5, gpio.OUT)
gpio.output(18, gpio.HIGH)
gpio.output(23, gpio.HIGH)
gpio.output(24, gpio.HIGH)
gpio.output(5, gpio.HIGH)

##Designating global variables
rev_val = None
light_val = None

##Main function that instantiates threads and the Rover class (GUI)
def main():
	control_thread = Thread(target=controls)
	control_thread.daemon = True
	control_thread.start()
	light_thread = Thread(target=lights)
	light_thread.daemon = True
	light_thread.start()
	rev_thread = Thread(target=rev_lights)
	rev_thread.daemon = True
	rev_thread.start()
	Rover()
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		print ("\nTHREADS DISABLED")
		gpio.cleanup()

##Creates a window using tkinter that allows key strokes to act as input, which call various functions
def controls():
	def key_press(event):
		global light_val
		global rev_val
		key_press = event.char
		if (key_press.lower() == 'w'):
			motor_forward()
			rev_val = 1
		if (key_press.lower() == 's'):
			motor_reverse()
			rev_val = 0
		if (key_press.lower() == 'd'):
			motor_right()
			rev_val = 1
		if (key_press.lower() == 'a'):
			motor_left()
			rev_val = 1
		if (key_press.lower() == 'f'):
			motor_stop()
			rev_val = 1
		if (key_press.lower() == 't'):
			light_val = 0
		if (key_press.lower() == 'y'):
			light_val = 1
	root = Tk()
	root.title("Controls")
	root.bind('<KeyPress>', key_press)
	root.mainloop()

##This function, which runs as a thread, turns the lights on and off indefinately
def lights():
	while True:
		if light_val == 0:
			time.sleep(0.3)
			gpio.output(18, gpio.LOW)
			time.sleep(0.15)
			gpio.output(23, gpio.LOW)
			time.sleep(0.15)
			gpio.output(24, gpio.LOW)
			time.sleep(0.45)
			gpio.output(18, gpio.HIGH)
			gpio.output(23, gpio.HIGH)
			gpio.output(24, gpio.HIGH)
		else:
			time.sleep(0.1)
##A function that also runs as a thread, that turns the blinking lights on when the rover is reversing
def rev_lights():
	while True:
		if rev_val == 0:
			gpio.output(5, gpio.LOW)
			time.sleep(0.8)
			gpio.output(5, gpio.HIGH)
			time.sleep(0.8)
		else:
			time.sleep(0.1)
##These are all functions that send values to the output pins and run the motors
def motor_forward():
	gpio.output(22, gpio.LOW)
	gpio.output(27, gpio.LOW)
	gpio.output(4, gpio.HIGH)
	gpio.output(17, gpio.HIGH)

def motor_reverse():
	gpio.output(22, gpio.HIGH)
	gpio.output(27, gpio.HIGH)
	gpio.output(4, gpio.LOW)
	gpio.output(17, gpio.LOW)

def motor_left():
	gpio.output(22, gpio.LOW)
	gpio.output(27, gpio.HIGH)
	gpio.output(4, gpio.LOW)
	gpio.output(17, gpio.HIGH)
	time.sleep(0.4)
	gpio.output(22, gpio.LOW)
	gpio.output(27, gpio.LOW)
	gpio.output(4, gpio.LOW)
	gpio.output(17, gpio.LOW)

def motor_right():
	gpio.output(22, gpio.HIGH)
	gpio.output(27, gpio.LOW)
	gpio.output(4, gpio.HIGH)
	gpio.output(17, gpio.LOW)
	time.sleep(0.4)
	gpio.output(22, gpio.LOW)
	gpio.output(27, gpio.LOW)
	gpio.output(4, gpio.LOW)
	gpio.output(17, gpio.LOW)

def motor_stop():
	gpio.output(22, gpio.LOW)
	gpio.output(27, gpio.LOW)
	gpio.output(4, gpio.LOW)
	gpio.output(17, gpio.LOW)

#These functions assign values to variables that either let the light threads run or go into a sleep
def lights_on():
	global light_val
	light_val = 0

def lights_off():
	global light_val
	light_val = 1

#This class sets up my buttons for my GUI
class Rover():
	def __init__(self):
		self.myContainer1 = Frame()
		self.myContainer1.grid(row = 0, column = 0)
		self.myContainer2 = Frame()
		self.myContainer2.grid(row = 0, column = 2)
		
		self.button1 = Button(self.myContainer1)
		self.button1.configure(text = "Forward", background = "blue", foreground = "white")
		self.button1.grid(row = 0, column = 1)
		self.button1.bind("<Button>", self.motor_forward)

		self.button2 = Button(self.myContainer1)
		self.button2.configure(text = "Reverse", background = "blue", foreground = "white")
		self.button2.grid(row = 1, column = 1)
		self.button2.bind("<Button>", self.motor_reverse)

		self.button3 = Button(self.myContainer1)
		self.button3.configure(text = "Right", background = "blue", foreground = "white")
		self.button3.grid(row = 1, column = 2)
		self.button3.bind("<Button>", self.motor_right)

		self.button4 = Button(self.myContainer1)
		self.button4.configure(text = "Left", background = "blue", foreground = "white")
		self.button4.grid(row = 1, column = 0)
		self.button4.bind("<Button>", self.motor_left)

		self.button5 = Button(self.myContainer1)
		self.button5.configure(text = "Stop", background = "red", foreground = "white")
		self.button5.grid(row = 2, column = 1)
		self.button5.bind("<Button>", self.motor_stop)

		self.button6 = Button(self.myContainer2)
		self.button6.configure(text = "Lights On!", background = "white", foreground = "black")
		self.button6.grid(row = 0, column = 1)
		self.button6.bind("<Button>", self.lights_on)

		self.button7 = Button(self.myContainer2)
		self.button7.configure(text = "Lights Off!", background = "black", foreground = "white")
		self.button7.grid(row = 1, column = 1)
		self.button7.bind("<Button>", self.lights_off)
		
	def motor_forward(self,event):
		global rev_val
		rev_val = 1
		gpio.output(22, gpio.LOW)
		gpio.output(27, gpio.LOW)
		gpio.output(4, gpio.HIGH)
		gpio.output(17, gpio.HIGH)
	
	def motor_reverse(self,event):
		global rev_val
		rev_val = 0
		gpio.output(22, gpio.HIGH)
		gpio.output(27, gpio.HIGH)
		gpio.output(4, gpio.LOW)
		gpio.output(17, gpio.LOW)
	
	def motor_right(self,event):
		global rev_val
		rev_val = 1
		gpio.output(22, gpio.HIGH)
		gpio.output(27, gpio.LOW)
		gpio.output(4, gpio.HIGH)
		gpio.output(17, gpio.LOW)
		time.sleep(0.4)
		gpio.output(22, gpio.LOW)
		gpio.output(27, gpio.LOW)
		gpio.output(4, gpio.LOW)
		gpio.output(17, gpio.LOW)

	def motor_left(self,event):
		global rev_val
		rev_val = 1
		gpio.output(22, gpio.LOW)
		gpio.output(27, gpio.HIGH)
		gpio.output(4, gpio.LOW)
		gpio.output(17, gpio.HIGH)
		time.sleep(0.4)
		gpio.output(22, gpio.LOW)
		gpio.output(27, gpio.LOW)
		gpio.output(4, gpio.LOW)
		gpio.output(17, gpio.LOW)
		
	def motor_stop(self,event):
		global rev_val
		rev_val = 1
		gpio.output(22, gpio.LOW)
		gpio.output(27, gpio.LOW)
		gpio.output(4, gpio.LOW)
		gpio.output(17, gpio.LOW)
		
	def lights_on(self,event):
		global light_val
		light_val = 0

	def lights_off(self,event):
		global light_val
		light_val = 1

#Finally, call the main function to start the program
main()
