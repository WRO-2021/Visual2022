import cv2
import imutils
import time
from PIL import Image

#sinistra L1.png ... 
#destra L1.png ...
i = 0

while True:
    i += 1
    cap = cv2.VideoCapture(0)
    frame = cap.read()
    cap1 = cv2.VideoCapture(1)
    frame1 = cap1.read()


    def takePicture():
        (grabbed, frame) = cap.read()
        cv2.waitKey(1)
        cv2.imwrite('L' + str(i) + '.png', frame)
        cap.release()
        
    def takePicture1():
        (grabbed, frame1) = cap1.read()
        cv2.waitKey(1)
        cv2.imwrite('R' + str(i) + '.png', frame1)
        cap1.release()

    takePicture()
    takePicture1()

    img = cv2.imread('L' + str(i) + '.png')
    resized = cv2.resize(img, (16, 16))
    cv2.imwrite('L' + str(i) + '.png', resized)

    img1 = cv2.imread('R' + str(i) + '.png')
    resized1 = cv2.resize(img1, (16, 16))
    cv2.imwrite('L' + str(i) + '.png', resized1)

    time.sleep(0.5)