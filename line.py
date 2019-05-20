from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import RPi.GPIO as GPIO
from sensor import *
from moottori import *

camera = PiCamera()
camera.resolution = (640, 360)
#640 360
scale = (320,180)
scalex = 320
scaley = 180
camera.rotation = 0
rawCapture = PiRGBArray(camera, size=(640, 360))
time.sleep(0.1)

x_last = 320
y_last = 180

state = 1
tresh = 75

def nothing(x):
    pass

def frame():
	global img
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		cv2.namedWindow("image")
		image = frame.array
		image = cv2.resize(image,(200,100))
		cv2.imshow("image",image)
		rawCapture.truncate(0)
		key = cv2.waitKey(1) & 0xFF

def main():
	global state
	global tresh
	global x_last
	global y_last
	try:
		cv2.namedWindow("image")
		cv2.createTrackbar('angle','image',50,80,nothing)
		cv2.createTrackbar('error','image',230,350,nothing)
		cv2.createTrackbar('speed','image',0,10,nothing)
		cv2.createTrackbar('tresh','image',75,255,nothing)
		cv2.createTrackbar('tole','image',4,10,nothing)
		for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
			image = frame.array
#			print(image)
			image = cv2.resize(image,scale)
			Blackline = cv2.inRange(image, (0,0,0), (tresh,tresh,tresh))
			kernel = np.ones((3,3), np.uint8)
			Blackline = cv2.erode(Blackline, kernel, iterations=5)
			Blackline = cv2.dilate(Blackline, kernel, iterations=9)
			contours_blk, hierarchy_blk = cv2.findContours(Blackline.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

			contours_blk_len = len(contours_blk)
			if contours_blk_len > 0 :
				if contours_blk_len == 1 :
					blackbox = cv2.minAreaRect(contours_blk[0])
				else:
					canditates=[]
					off_bottom = 0
					for con_num in range(contours_blk_len):
						blackbox = cv2.minAreaRect(contours_blk[con_num])
						(x_min, y_min), (w_min, h_min), ang = blackbox
						box = cv2.boxPoints(blackbox)
						(x_box,y_box) = box[0]
						if y_box > 358 :
							off_bottom += 1
						canditates.append((y_box,con_num,x_min,y_min))
					canditates = sorted(canditates)
					if off_bottom > 1:
						canditates_off_bottom=[]
						for con_num in range ((contours_blk_len - off_bottom), contours_blk_len):
							(y_highest,con_highest,x_min, y_min) = canditates[con_num]
							total_distance = (abs(x_min - x_last)**2 + abs(y_min - y_last)**2)**0.5
							canditates_off_bottom.append((total_distance,con_highest))
						canditates_off_bottom = sorted(canditates_off_bottom)
						(total_distance,con_highest) = canditates_off_bottom[0]
						blackbox = cv2.minAreaRect(contours_blk[con_highest])
					else:
						(y_highest,con_highest,x_min, y_min) = canditates[contours_blk_len-1]
						blackbox = cv2.minAreaRect(contours_blk[con_highest])
				(x_min, y_min), (w_min, h_min), ang = blackbox
				x_last = x_min
				y_last = y_min
				if ang < -45 :
					ang = 90 + ang
				if w_min < h_min and ang > 0:
					ang = (90-ang)*-1
				if w_min > h_min and ang < 0:
					ang = 90 + ang
				setpoint = scalex/2
				error = int(x_min - setpoint)
				ang = int(ang)
				box = cv2.boxPoints(blackbox)
				box = np.int0(box)
				cv2.drawContours(image,[box],0,(0,0,255),3)
				cv2.putText(image,str(ang),(10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
				cv2.putText(image,str(error),(10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
				cv2.line(image, (int(x_min),scaley-40 ), (int(x_min),scaley-60 ), (255,0,0),3)
				maxe = cv2.getTrackbarPos('error','image')
				maxa = cv2.getTrackbarPos('angle','image')
				speed = cv2.getTrackbarPos('speed','image')
				tresh = cv2.getTrackbarPos('tresh','image')
				tole = cv2.getTrackbarPos('tole','image')


				if button() == 1 and state == 0:
					state = 1
					time.sleep(1)
				if state == 1:
					moveline(ang, error, maxa, maxe, speed, tole)
				if button() == 1:
					state = 0
					stop()
					time.sleep(1)

#			image = cv2.resize(image,(640,360))
			cv2.imshow("image", image)
			rawCapture.truncate(0)
			key = cv2.waitKey(1) & 0xFF
	except KeyboardInterrupt:
		stop()


if __name__ == "__main__":
	main()
