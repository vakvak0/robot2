from gpiozero import PWMOutputDevice
from time import sleep

#///////////////// Define Motor Driver GPIO Pins /////////////////
# Motor A, Left Side GPIO CONSTANTS
PWM_FRONT_RIGHT_PIN = 17 # IN1 - Forward Drive
PWM_FRONT_LEFT_PIN = 19	 # IN2 - Reverse Drive
# Motor B, Right Side GPIO CONSTANTS
PWM_BACK_RIGHT_PIN = 4	 # IN1 - Forward Drive
PWM_BACK_LEFT_PIN = 6	 # IN2 - Reverse Drive


FRFp = 20 #etu oikea eteen
FRRp = 21 #etu oikea taakse
FLFp = 16 #etu vasen eteen
FLRp = 14 #etu vasen taakse
BRFp = 5 #taka oikea eteen
BRRp = 7 #taka oikea taakse
BLFp = 8 #taka vasen eteen
BLRp = 11 #taka vasen taakse
# Initialise objects for H-Bridge PWM pins
# Set initial duty cycle to 0 and frequency to 1000
FR = PWMOutputDevice(PWM_FRONT_RIGHT_PIN, True, 0, 1000)
FL = PWMOutputDevice(PWM_FRONT_LEFT_PIN, True, 0, 1000)

BR = PWMOutputDevice(PWM_BACK_RIGHT_PIN, True, 0, 1000)
BL = PWMOutputDevice(PWM_BACK_LEFT_PIN, True, 0, 1000)

FRF = PWMOutputDevice(FRFp, True, 0, 1000)
FRR = PWMOutputDevice(FRRp, True, 0, 1000)

FLF = PWMOutputDevice(FLFp, True, 0, 1000)
FLR = PWMOutputDevice(FLRp, True, 0, 1000)

BRF = PWMOutputDevice(BRFp, True, 0, 1000)
BRR = PWMOutputDevice(BRRp, True, 0, 1000)

BLF = PWMOutputDevice(BLFp, True, 0, 1000)
BLR = PWMOutputDevice(BLRp, True, 0, 1000)

def moveline(ang, err, maxa, maxe, speed, tole):

	tole = tole / 10
	speed = speed / 10

	if ang > maxa:
		ang = maxa

	if ang < -maxa:
		ang = -maxa

	if err > maxe:
		err = maxe

	if err < -maxe:
		err = -maxe

	a = ang/maxa
	e = err/maxe

	print(round(a,3),round(e,3),maxa,maxe)

	if e > tole:
		move((1-e+a/2)*speed, 1*speed)
	elif e < -tole:
		move(1*speed, (1-abs(e)+a/2)*speed)
	elif a > 0:
		move((1-a)*speed, 1*speed)
	elif a <= 0:
		move(1*speed, (1-abs(a))*speed)

def move(r,l,x=0):

	if r > 1:
		r = 1
	if r < -1:
		r = -1
	if l > 1:
		l = 1
	if l < -1:
		l = -1

	if x > 0:
		r = r/x
		l = l/x

	FR.value = abs(r)
	FL.value = abs(l)
	BR.value = abs(r)
	BL.value = abs(l)

	if r != abs(r):
		FRF.value = 0
		FRR.value = 1
		BRF.value = 0
		BRR.value = 1
	else:
		FRF.value = 1
		FRR.value = 0
		BRF.value = 1
		BRR.value = 0

	if l != abs(l):
		FLF.value = 0
		FLR.value = 1
		BLF.value = 0
		BLR.value = 1
	else:
		FLF.value = 1
		FLR.value = 0
		BLF.value = 1
		BLR.value = 0

def stop():
	FR.value = 0
	FL.value = 0
	BR.value = 0
	BL.value = 0

	FRF.value = 0
	FRR.value = 0
	FLF.value = 0
	FLR.value = 0

	BRF.value = 0
	BRR.value = 0
	BLF.value = 0
	BLR.value = 0

def xymotor(x,y):
	x, y = 2/255*x-1,2/255*y-1
	l, r = (y+y*x+x),(y+y*(-x)-x)
	if abs(l) > 1 or abs(r) > 1:
		if abs(l) > abs(r):
			l, r = l/abs(l), r/abs(l)
		elif abs(r) > abs(l):
			l, r = l/abs(r), r/abs(r)
	return -l, -r
