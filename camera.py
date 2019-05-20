from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

camera = PiCamera()
camera.resolution = (640, 360)
camera.rotation = 0
rawCapture = PiRGBArray(camera, size=(640, 360))
time.sleep(0.1)

def nothing(x):
    pass


def increase_brightness(img, value=30):
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	h, s, v = cv2.split(hsv)

	lim = 255 - value
	v[v > lim] = 255
	v[v <= lim] += value

	final_hsv = cv2.merge((h, s, v))
	img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
	return img

def main():

	cv2.namedWindow("image")
	cv2.createTrackbar('brightness','image',22,200,nothing)
	cv2.createTrackbar('alpha','image',0,255,nothing)
	cv2.createTrackbar('beta','image',0,255,nothing)
#	cv2.createTrackbar('tresh','image',75,255,nothing)
#	cv2.createTrackbar('tole','image',4,10,nothing)
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		image = frame.array
		bright = cv2.getTrackbarPos('brightness','image')
		alpha = cv2.getTrackbarPos('alpha','image')
		beta = cv2.getTrackbarPos('beta','image')
		tresh = cv2.getTrackbarPos('tresh','image')
		tole = cv2.getTrackbarPos('tole','image')

		image = increase_brightness(image, value=bright)



		cv2.imshow("image", image)
		rawCapture.truncate(0)
		key = cv2.waitKey(1) & 0xFF

if __name__ == "__main__":
	main()
