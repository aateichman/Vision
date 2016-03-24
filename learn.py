import RPi.GPIO as gpio
import time
class move:

    def __init__(self, RF,RB,LF,LB,SLEEP):
       self.RF = RF
       self.RB = RB
       self.LF = LF
       self.LB = LB
       self.SLEEP = SLEEP

    def getRF(self):
        return self.RF
    def getRB(self):
        return self.RB
    def getLF(self):
        return self.LF
    def getLB(self):
        return self.LB
    def getSleep(self):
        return self.SLEEP

class gpioHelp: 
	def __init__(self):
	gpio.setwarnings(False)
	gpio.setmode(gpio.BCM)
	gpio.setup(22, gpio.OUT)
	gpio.setup(4, gpio.OUT)
	gpio.setup(17, gpio.OUT)
	gpio.setup(27, gpio.OUT)

	def Move(self,Move):
		gpio.output(4,Move.getRB)
		gpio.output(17,Move.getLB)
		gpio.output(22,Move.getRF)
		gpio.output(27,Move.getLF)
		time.sleep(Move.sleep)

moveHELP = gpioHelp()

def moveForward(self, t):
	for x in range (0,100):
		d = move(gpio.HIGH,gpio.LOW,gpio.HIGH,gpio.LOW,10)
		moveHELP.Move(d);


	





