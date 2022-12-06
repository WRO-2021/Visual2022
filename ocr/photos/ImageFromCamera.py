import cv2
import time
from checCameras import returnCameraIndexes

#sinistra L1.png ... 
#destra L1.png ...

camera_indexes = returnCameraIndexes()

def capture(cap, size=16):
        (grabbed, frame) = cap.read()
        return cv2.resize(frame, (size, size))

def takePicture(cap, letter='', num= 0, path = '../images/', name=None):
        resized = capture(cap)
        if name is None:
                path += letter + str(num) + '.png'
        else:
                path += name + '.png'
        cv2.imwrite(path + letter + str(num) + '.png', resized)


def main():
        i = 0
        path = '../images/'
        caps = [
                cv2.VideoCapture(camera_indexes[0]),
                cv2.VideoCapture(camera_indexes[1])
        ]
        while True:
                try:
                        print("cacca")
                        i += 1

                
                        takePicture(caps[0],'L', i, path)
                        takePicture(caps[1],'R', i, path)

                        time.sleep(0.5)
                        print("culo")
                except KeyboardInterrupt:
                        print("KeyboardInterrupt")
                        break

                for cap in caps:
                        cap.release()

if __name__ == "__main__":
        main()
