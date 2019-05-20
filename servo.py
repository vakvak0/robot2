from gpiozero import Servo
from time import sleep

myGPIO=18

a = 0

myCorrection=0.4
maxPW=(2.0+myCorrection)/1000
minPW=(1.0-myCorrection)/1000

servo = Servo(myGPIO,min_pulse_width=minPW,max_pulse_width=maxPW)

def servO(x):
	global a
	if a == x:
		servo.value = None
	else:
		servo.value = x
	a = x

def main():
	x = int(input())
	servo.value x
	sleep(1)

if __name__ == "__main__":
	main()
