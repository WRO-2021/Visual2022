import pickle
import threading
import torch
from torch import nn
import cv2
import sys
sys.path.append('../ocr/photos/')
from ImageFromCamera import capture
from checCameras import returnCameraIndexes

# left and right
letter_reading = ['_', '_']
mutex = threading.Lock()
run_event = threading.Event()

model = pickle.load(open('../neuralnetwork/nn.pickle', 'rb'))

def convert_from_tensor(tensor):
    return tensor.detach().numpy()

def take_picture_and_check():
    global letter_reading
    global mutex
    global model

    camera_indexes = returnCameraIndexes()
    capLeft = cv2.VideoCapture(camera_indexes[0])
    capRight = cv2.VideoCapture(camera_indexes[1])
    while True:
        try:
            images = [capture(capLeft), capture(capRight)]
            letters = [ model.predict(image) for image in images]
            with mutex:
                letter_reading = [convert_from_tensor(letter) for letter in letters]
        except KeyboardInterrupt:
            break
        if(run_event.is_set()):
            break

    capLeft.release()
    capRight.release()

thread = threading.Thread(target=take_picture_and_check)
thread.start()

try:
    while True:
        with mutex:
            # skeleton, print or listen with the arduino

            print(letter_reading)
except KeyboardInterrupt:
    print('KeyboardInterrupt in main thread')
    pass

#exit the thread
run_event.set()
thread.join()

