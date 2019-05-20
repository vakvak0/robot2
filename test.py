from moottori import *
from time import time

tick = time()

while True:
	if time()-tick > 3:
		print("3 sec")
