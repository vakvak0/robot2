from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
from moottori import *
from sensor import *

camera = PiCamera()
camera.resolution = (640, 360)
#200 180
camera.rotation = 0
rawCapture = PiRGBArray(camera, size=(640, 360))
time.sleep(0.1)
state = 0

try:
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		image = frame.array
		Blackline = cv2.inRange(image, (0,0,0), (70,70,70))
		kernel = np.ones((3,3), np.uint8)
		Blackline = cv2.erode(Blackline, kernel, iterations=5)
		Blackline = cv2.dilate(Blackline, kernel, iterations=9)
		contours_blk, hierarchy_blk = cv2.findContours(Blackline.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		if button() == 1 and state == 0:
			state = 1
			time.sleep(1)

		if len(contours_blk) > 0:
			blackbox = cv2.minAreaRect(contours_blk[0])
			(x_min, y_min), (w_min, h_min), ang = blackbox
			if ang < -45 :
				ang = 90 + ang
			if w_min < h_min and ang > 0:
				ang = (90-ang)*-1
			if w_min > h_min and ang < 0:
				ang = 90 + ang
			setpoint = 320
			error = int(x_min - setpoint)
			ang = int(ang)
			box = cv2.boxPoints(blackbox)
			box = np.int0(box)
			cv2.drawContours(image,[box],0,(0,0,255),3)
			cv2.putText(image,str(ang)+" ang",(10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
			cv2.putText(image,str(error)+" err",(10, 320), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
			cv2.line(image, (int(x_min),200 ), (int(x_min),250 ), (255,0,0),3)

			a = ang
			e = error

			maxa = 50
			maxe = 230

			if state == 1:
				if ang > maxa:
					a = maxa

				if ang < -maxa:
					a = -maxa

				if error > maxe:
					e = maxe

				if error < -maxe:
					e = -maxe

				a = a/maxa
				e = e/maxe
				print(round(a,3),round(e,3))

				if e > 0.4:
					move(1-e+a/2,1)
				elif e < -0.4:
					move(1,1-abs(e)+a/2)
				elif a > 0:
					move(1-a,1)
				elif a <= 0:
					move(1,1-abs(a))
				if button() == 1:
					state = 0
					stop()
					time.sleep(1)

		cv2.imshow("orginal with line", image)
		rawCapture.truncate(0)
		key = cv2.waitKey(1) & 0xFF
except KeyboardInterrupt:
	stop()

