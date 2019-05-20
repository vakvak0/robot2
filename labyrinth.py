from sensor import *
from moottori import *
from time import sleep, time
from statistics import median
events = []
state = 0
done = 0

def lista():
	l=[]
	for i in range(3):
		l.append(front())
	return median(l)


def first():
	global done
	while lista() < 10 and state == 1:
		move(-1,1)
	while lista() > 10 and state == 1:
		move(0.6,0.6)
	done = 1

def main():
	aika = 4
	boolean = 0
	max = 10

	eteen2, eteen1 = 0.6 , 0.6
	vasemmalle2 ,vasemmalle1 = -0.1 , 0.6
	oikealle2, oikealle1 = 0.6 , 0
	käänvas2, käänvas1 = 0.05 , 0.7
	käänoi2, käänoi1 = 1 , -0.6

	global state

	tick = time()

	#ETEENPÄIN
	while left() == 0 and right() == 0 and lista() > max and state == 1:
		if time()-tick > aika:
			move(1,1)
		else:
			move(eteen1, eteen2)
		if boolean == 0:
			events.append(1)
			boolean = 1

		if button() == 1:
			state = 0
			stop()
			sleep(1)
		print("1")
	boolean = 0

	#VÄISTÄÄ VASEMMALLE
	while left() == 0 and right() == 1 and lista() > max and state == 1:
		if time()-tick > aika:
			move(1,-1)
		else:
			move(vasemmalle1 ,vasemmalle2)

		if button() == 1:
			state = 0
			stop()
			sleep(1)
		print("2")

	#KÄÄNTYY VASEMMALLE NOPEASTI
	while left() == 1 and right() == 1 and lista() > max and state == 1:
		if time()-tick > 7:
			move(1,-1)
		else:
			move(käänvas1, käänvas2)
		if boolean == 0:
			events.append(3)
			boolean = 1

		if button() == 1:
			state = 0
			stop()
			sleep(1)
		print("3")
	boolean = 0

	#VÄISTÄÄ OIKEALLE
	while left() == 1 and right() == 0 and lista() > max and state == 1:
		if time()-tick > aika:
			move(-1,1)
		else:
			move(oikealle1, oikealle2)

		if button() == 1:
			state = 0
			stop()
			sleep(1)
		print("4")

	#KÄÄNTYY PAIKALLAAN OIKEALLE
	while lista() <= max and state == 1:
		if time()-tick > aika:
			move(-1,1)
		else:
			move(käänoi1, käänoi2)
		if boolean == 0:
			events.append(5)
			boolean = 1
		if button() == 1:
			state = 0
			stop()
			sleep(1)
		print("5")
	boolean = 0


if __name__ == "__main__":
	try:
		while True:
			btn = button()
			if btn == 1 and state == 0:
				state = 1
				print("ass")
				sleep(1)

			if state == 1:
			#	if done == 0:
			#		first()
				main()

	except KeyboardInterrupt:
		r = events.count(5)
		l = events.count(3)
		if r == 0:
			r = 0.001
		if l == 0:
			l = 0.001
		sum = r + l
		print(sum,r,l,"   ","oikealle",round(r/sum*100, 3),"%","vasemmalle",round(l/sum*100, 3),"%")
