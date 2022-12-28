import pickle
import threading
import torch
import sys
sys.path.append('../')
from ocr.photos.ImageFromCamera import capture
from ocr.photos.checCameras import returnCameraIndexes
from sklearn import preprocessing # label encoder
from ocr.neuralnetwork.CNN import NeuralNetwork
import cv2
import numpy as np
import time

SAVES = '../ocr/neuralnetwork/'
encoder = None
with open(SAVES + 'labelEncoder.pickle', 'rb') as handle:
    encoder = pickle.load(handle)
# load model with torch
model = NeuralNetwork(2)
model.load_state_dict(torch.load(SAVES + 'nn.torch'))
model.eval()

# left and right
letter_reading = ['none', 'none']
mutex = threading.Lock()
run_event = threading.Event()

def torchImage_to_letter(img):
    out = model(img)[0]
    out = out.argmax(dim=0)
    out = np.array([out])
    out = encoder.inverse_transform(out)[0]
    return out

def image_to_torch(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = img.astype('float32')
    img = torch.from_numpy(img)
    img = img.unsqueeze(0).unsqueeze(0)
    return img


def take_picture_and_check():
    global letter_reading
    global mutex
    global model

    camera_indexes = returnCameraIndexes()
    capLeft = cv2.VideoCapture(camera_indexes[0])
    capRight = cv2.VideoCapture(camera_indexes[1])
    # capture images, use the model on the images, and then update the status
    while True:
        try:
            images = [capture(capLeft), capture(capRight)]
            images = [image_to_torch(x) for x in images]
            letters = [torchImage_to_letter(x) for x in images]
            with mutex:
                if letters != letter_reading:
                    print('Qualcosa e\' cambiato!!', letters)
                letter_reading = letters
        except KeyboardInterrupt:
            break
        # exit message from main thread
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

            #harmed victim 3 kit
            #stable victim 2 kit
            #unarmed victim 0 kit
            print(letter_reading)
except KeyboardInterrupt:
    print('KeyboardInterrupt in main thread')

#exit the thread
run_event.set()
thread.join()

