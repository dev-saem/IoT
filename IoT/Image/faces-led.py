import numpy as np
import cv2
import pickle

import RPi.GPIO as GPIO
from time import sleep
import threading

detect_state = False
led_status = 0


def controlDevice(detect_state):
    while detect_state:
        if(led_status == 1):
            GPIO.output(4, 1)
        else:
            GPIO.output(4, 0)


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.OUT, initial=GPIO.LOW)

global t
detect_state = True
t = threading.Thread(target=controlDevice, args=(detect_state,))
t.daemon = True
t.start()

face_cascade = cv2.CascadeClassifier(
    'cascades/data/haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_smile.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("./recognizers/face-trainner.yml")

labels = {"person_name": 1}
with open("pickles/face-labels.pickle", 'rb') as f:
	og_labels = pickle.load(f)
	labels = {v: k for k, v in og_labels.items()}

cap = cv2.VideoCapture(0)

while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
	for (x, y, w, h) in faces:
		# print(x,y,w,h)
		roi_gray = gray[y:y+h, x:x+w]  # (ycord_start, ycord_end)
		roi_color = frame[y:y+h, x:x+w]

    	# recognize? deep learned model predict keras tensorflow pytorch scikit learn
		id_, conf = recognizer.predict(roi_gray)
		if conf >= 4 and conf <= 85:
			font = cv2.FONT_HERSHEY_SIMPLEX
			name = labels[id_]
			color = (255, 255, 255)
			stroke = 2
			cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)

			if name == "obama":
				led_status = 1
			else:
				led_status = 0

		img_item = "7.png"
		cv2.imwrite(img_item, roi_color)

		color = (255, 0, 0)  # BGR 0-255
		stroke = 2
		end_cord_x = x + w
		end_cord_y = y + h
		cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
		# subitems = smile_cascade.detectMultiScale(roi_gray)
		# for (ex,ey,ew,eh) in subitems:
		# cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

	GPIO.setup(4, GPIO.OUT, initial=GPIO.LOW)
	# Display the resulting frame
	cv2.imshow('frame', frame)
	if cv2.waitKey(20) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
