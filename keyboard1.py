import pygame, sys, time
from pygame.locals import *

pygame.init()

FPS=30
fpsClock=pygame.time.Clock()

width=400
height=300
DISPLAYSURF=pygame.display.set_mode((width,height),0,32)


UP='up'
LEFT='left'
RIGHT='right'
DOWN='down'

direction = None

o, v = 0, 0

def liike(x = 0):
	global o, v
	if direction == K_UP:
		o, v = 1, 1
	elif direction == K_DOWN:
		o, v = -1, -1
	if direction == K_LEFT:
		o, v = 1, -1
	elif direction == K_RIGHT:
		o, v = -1, 1
	return o, v

while True:

	x = 0
	for event in pygame.event.get():
		if event.type==QUIT:
			pygame.quit()
			sys.exit()

		if event.type == KEYDOWN:
			direction = event.key
		if event.type == KEYUP:
			if (event.key == direction):
				direction = None

	nopeus = liike(x)
	if direction == None:
		nopeus = 0, 0
	print(nopeus)

	pygame.display.update()
	fpsClock.tick(FPS)
