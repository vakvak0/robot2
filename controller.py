from select import select
from evdev import InputDevice, categorize, ecodes, KeyEvent
from moottori import *
from servo import *

gamepad = InputDevice('/dev/input/event0')

x = 127
y = 127
x1 = 127
y1 = 127

try:
	def controller():
		global x
		global y
		global x1
		global y1
		a = 0
		for event in gamepad.read_loop():
			if((event.code == 5) and (event.type == 3)):
				y = int(event.value)
			if((event.code == 2) and (event.type == 3)):
				x = int(event.value)
			if((event.code == 1) and (event.type == 3)):
				y1 = int(event.value)
			if((event.code == 0) and (event.type == 3)):
				x1 = int(event.value)

			l, r = xymotor(x, y)

			if abs(l) > 0.1 or abs(r) > 0.1:
				move(l, r)

			else:
				stop()
			pos = (2/255*y1-1)
			if pos > 0.1:
				a = a + 0.005
				if a > 1:
					a = 1
			if pos < -0.1:
				a = a - 0.005
				if a < -1:
					a = -1
			servO(a)
finally:
	stop()
