
#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger

def front():
	front = GroveUltrasonicRanger(18)
	sleep(0.01)
	return front.get_distance()

def right():
	global l
	right = 26
	GPIO.setup(right, GPIO.IN)
	return GPIO.input(right)


def left():
	left = 24
	GPIO.setup(left, GPIO.IN)
	return GPIO.input(left)

def button():
	pin = 22
	GPIO.setup(pin, GPIO.IN)
	return GPIO.input(pin)

def main():
	front = GroveUltrasonicRanger(18)
	right = 26
	left = 24

	GPIO.setup(right, GPIO.IN)
	GPIO.setup(left, GPIO.IN)

	while True:
		distance = front.get_distance()
		leftd = GPIO.input(left)
		rightd = GPIO.input(right)
		print(round(distance,3),leftd,rightd,button())
		sleep(0.1)

	sleep(1)

if __name__ == '__main__':
    main()
