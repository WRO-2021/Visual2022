import cv2
import imutils
import time

#sinistra L1.png ... 
#destra L1.png ...
i = 0

path = '../images/'

def takePicture():
        (grabbed, frame) = cap.read()
        cv2.imwrite(path + 'L' + str(i) + '.png', frame)

def takePicture1():
        (grabbed, frame1) = cap1.read()
        cv2.imwrite(path +'R' + str(i) + '.png', frame1)

cap = cv2.VideoCapture(0)
cap1 = cv2.VideoCapture(2)

while True:
    print("cacca")
    i += 1

    takePicture()
    takePicture1()

    img = cv2.imread(path +'L' + str(i) + '.png')
    resized = cv2.resize(img, (16, 16))
    cv2.imwrite(path + 'L' + str(i) + '.png', resized)

    img1 = cv2.imread(path +'R' + str(i) + '.png')
    resized1 = cv2.resize(img1, (16, 16))
    cv2.imwrite(path +'R' + str(i) + '.png', resized1)

    time.sleep(0.5)
    print("culo")

cap.release()
cap1.release()
