import base64
import requests

import argparse
import cv2

from firebase import firebase
firebase = firebase.FirebaseApplication('https://picupload-82a83.firebaseio.com/', None)

def get_as_base64(url):
	return base64.b64encode(requests.get(url).content)

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)


url="https://firebasestorage.googleapis.com/v0/b/picupload-82a83.appspot.com/o/pic?alt=media&token=bf691324-6ebf-4460-a7be-758db0a1aa67"
fh=open("C:/Users/Aprameya/Desktop/iotia3/dummy.jpg","wb")
fh.write(base64.b64decode(get_as_base64(url)))
fh.close()

 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image",
	default="C:/Users/Aprameya/Desktop/iotia3/dummy.jpg",
	help="path to the input image")
ap.add_argument("-c", "--cascade",
	default="C:/Users/Aprameya/Desktop/iotia3/haarcascade_frontalface_default.xml",
	help="path to face detector haar cascade")
args = vars(ap.parse_args())

# load the input image and convert it to grayscale
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# load the cat detector Haar cascade, then detect cat faces
# in the input image
detector = cv2.CascadeClassifier(args["cascade"])
counr=0
ret=image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.equalizeHist(gray)
rects = detector.detectMultiScale(gray, scaleFactor=1.3,
	minNeighbors=4, minSize=(1, 1))

for (i, (x, y, w, h)) in enumerate(rects):
	cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
	cv2.putText(image, "face #{}".format(i + 1), (x, y - 10),
		cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
	i=i+1
	
print(i)
result = firebase.put('/uploadValue', 'pic',i)
print("dumped")
vis = image.copy()
#draw_rects(vis, rects, (0, 255, 0))

cv2.imshow('facedetect', vis)
cv2.waitKey(0)
cv2.destroyAllWindows()