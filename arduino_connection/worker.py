import pickle
import threading
#import torch
import cv2
import numpy as np
import time
import serial
import traceback

import sys
sys.path.append('../')
# import my own modules from the parent directory

from ocr.photos.captureImageFromCamera import capture, returnCameraIndexes
# from sklearn import preprocessing  # label encoder, non so se devo importarlo prima di caricare con pickle

#from ocr.neuralnetwork.CNN import NeuralNetwork

# https://stackoverflow.com/questions/15457786/ctrl-c-crashes-python-after-importing-scipy-stats
import os
os.environ['FOR_DISABLE_CONSOLE_CTRL_HANDLER'] = '1'

# se non riesce a fare le foto il raspberry:
# >sudo rmmod uvcvideo
import subprocess
subprocess.run(['sudo', 'rmmod', 'uvcvideo'])
subprocess.run(['sudo', 'modprobe', 'uvcvideo', 'nodrop=1', 'timeout=5000', 'quirks=0x80'])
# >sudo modprobe uvcvideo nodrop=1 timeout=5000 quirks=0x80
"""
N_LABELS = 4

SAVES = '../ocr/neuralnetwork/'
with open(SAVES + 'labelEncoder.pickle', 'rb') as handle:
    encoder_wb = pickle.load(handle)
with open(SAVES + 'labelEncoderColor.pickle', 'rb') as handle:
    encoder_rgb = pickle.load(handle)

# load model for letters with torch
model_wb = NeuralNetwork(N_LABELS, True)
model_wb.load_state_dict(torch.load(SAVES + 'nn.torch'))
model_wb.eval()

model_rgb = NeuralNetwork(N_LABELS, False)
model_rgb.load_state_dict(torch.load(SAVES + 'nnColor.torch'))
model_rgb.eval()
"""
# left and right
letters = ['none', 'none']
colors = ['none', 'none']
mutex = threading.Lock()
run_event = threading.Event()

"""
 How this works:
    - the main thread is the one that communicates with the arduino
    - the other thread is the one that takes the pictures and uses the model
"""
"""
# use the model and the encoder to get the letter from the image
def torch_image_to_letter(img, model, encoder):
    out = model(img)[0]
    out = out.argmax(dim=0)
    out = np.array([out])
    out = encoder.inverse_transform(out)[0]
    return out

# convert the image to a torch tensor(black and white)
def image_to_torch_bw(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = img.astype('float32')
    img = torch.from_numpy(img)
    img = img.unsqueeze(0).unsqueeze(0)
    return img

# convert the image to a torch tensor(rgb)
def image_to_torch_rgb(img):
    img = img.astype('float32')
    img = torch.from_numpy(img)
    img = img.unsqueeze(0).permute(0, 3, 1, 2)
    return img
"""

def is_something(img):
    var = int(np.var(img))
    #print(str(var).zfill(6), '#' * (var // 100))
    return var > 1500

# thread function
def take_picture_and_check():
    global letters, colors

    camera_indexes = returnCameraIndexes()
    cap_left = cv2.VideoCapture(camera_indexes[0])
    cap_right = cv2.VideoCapture(camera_indexes[1])
    # capture images, use the model on the images, and then update the status
    while True:
        try:
            # take the pictures and convert them to torch tensors
            images = [capture(cap_left), capture(cap_right)]
            """
            bw = [image_to_torch_bw(x) for x in images]
            rgb = [image_to_torch_rgb(x) for x in images]
            # use the model to get the letter
            letters_tmp = [torch_image_to_letter(x, model_wb, encoder_wb) for x in bw]
            colors_tmp = [torch_image_to_letter(x, model_rgb, encoder_rgb) for x in rgb]

            if letters != letters_tmp:
                print('Qualcosa e\' cambiato(letter)!!', letters_tmp)
            if colors != colors_tmp:
                print('Qualcosa e\' cambiato(color)!!', colors_tmp)
            # update the status
            with mutex:
                letters = letters_tmp
                colors = colors_tmp
            """
            new_colors = [('yellow' if is_something(x) else 'none') for x in images]
            with mutex:
                colors = new_colors
                
        except KeyboardInterrupt:
            print('KeyboardInterrupt in thread')
            break
        # exit message from main thread
        if run_event.is_set():
            print('Exiting thread from event trigger')
            break

    cap_left.release()
    cap_right.release()

PORT = '/dev/ttyS0'


thread = threading.Thread(target=take_picture_and_check)
thread.start()


arduino = serial.Serial(port=PORT, baudrate=9600, timeout=.1)

def wait_arduino():
    print('waiting')
    if not arduino.is_open:
        arduino.open()
    print('opened')

    arduino.write(b'sta')
    print('connecting')

    while True:
        if arduino.in_waiting >= 3:
            if arduino.read(1) == b's'and arduino.read(1) == b't' and arduino.read(1) == b'a':
                print('connected!')
                break


KITS = {
    'h': b'3',
    's': b'2',
    'n': b'0',
    'red': b'2',
    'yellow': b'1',
    'green': b'0',
}
    

def watch_and_communicate():
    try:
        while True:
            # wait request
            while True:
                if arduino.in_waiting:
                    msg = arduino.read(1)
                    if msg == b'?':
                        break
                    else:
                        print('Wrong msg: ', msg)
            print('Recived')
            # respond
            with mutex:
                # skeleton, print or listen with the arduino
                #harmed victim 3 kit
                #stable victim 2 kit
                #unarmed victim 0 kit

                left = b'N0'
                right = b'N0'

                if colors[0] != 'none':
                    left = b'S' + KITS[colors[0]]
                elif letters[1] != 'none':
                    left = b'S' + KITS[letters[0]]
                    
                if colors[1] != 'none':
                    right = b'S' + KITS[colors[1]]
                elif letters[1] != 'none':
                    right = b'S' + KITS[letters[1]]

                message = b'!' + left + right + b'\n'

                print('Message: ', message)

            arduino.flush()
            arduino.write(message)

    except KeyboardInterrupt:
        print('KeyboardInterrupt in main thread')

    # exit the thread
    run_event.set()
    thread.join()

while True:
    try:
        wait_arduino()
        watch_and_communicate()
    except KeyboardInterrupt:
        print('KeyboardInterrupt in main thread')
        break
    except:
        print('Unexpected error:', sys.exc_info()[0])
        traceback.print_exc()
        print('Restarting...')
        time.sleep(1)
