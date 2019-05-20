import pygame, sys
from pygame.locals import *
import RPi.GPIO as GPIO
from moottori import *

pygame.init()
BLACK = (0,0,0)
WIDTH = 100
HEIGHT = 100
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

windowSurface.fill(BLACK)
x = 0
o = 0
v = 0
while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == 273:
				o, v = 1, 1
				if event.key == 375:
					o = o - 1
				if event.key == 376:
					v = v - 1

			elif event.key == 274:
				o, v = -1, -1
				if event.key == 375:
					o = o + 1
				if event.key == 376:
					v = v + 1

			elif event.key == 375:
				o, v = -1, 1

			elif event.key == 376:
				o, v == 1, -1

		print(v,o)

		if event.type == KEYUP:
			if event.key == 273:
				o, v = 0, 0

