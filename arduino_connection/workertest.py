import pickle
import threading
import cv2
import sys
import serial
sys.path.append('../ocr/photos/')
from ImageFromCamera import capture
from checCameras import returnCameraIndexes

arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1)
# left and right
# 's', 'h', 'u', 'red'...
letter_reading = ['_', '_']
mutex = threading.Lock()
run_event = threading.Event()

def convert_from_tensor(tensor):
    return tensor.detach().numpy()

def take_picture_and_check():
    global letter_reading
    global mutex
    global model

    print('starting thread')

    camera_indexes = returnCameraIndexes()
    print(camera_indexes)
    capLeft = cv2.VideoCapture(camera_indexes[0])
    capRight = cv2.VideoCapture(camera_indexes[1])

    print('starting image loop')
    while True:
        try:
            images = [capture(capLeft), capture(capRight)]
            letters = input("dimmi il lato: ")#[1 for output in images]
            print('captured')
            with mutex:
                letter_reading = input("dimmi cosa vedi: ")#['red' for letter in letters]
        except KeyboardInterrupt:
            break
        if(run_event.is_set()):
            print('exiting from thread photos')
            break

    capLeft.release()
    capRight.release()

thread = threading.Thread(target=take_picture_and_check)
thread.start()

try:
    while True:
        while arduino.readline() != "readCamera":
            pass
        with mutex:
            # skeleton, print or listen with the arduino
            #harmed victim 3 kit
            #stable victim 2 kit
            #unarmed victim 0 kit
            message = ""

            if letter_reading[0] == "_":
                arduino.write(bytes(letter_reading[1], 'utf-8'))
            else:
                arduino.write(bytes(letter_reading[0], 'utf-8'))
except KeyboardInterrupt:
    print('KeyboardInterrupt in main thread')
    pass

#exit the thread
run_event.set()
thread.join()

