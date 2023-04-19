import sys
import cv2
import time
import sys


# sinistra L1.png ...
# destra R1.png ...

def returnCameraIndexes():
    # checks the first 10 indexes.
    arr = []
    for index in range(10):
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            arr.append(index)
            cap.release()
    return arr


def capture(cap, size=24):
    (grabbed, frame) = cap.read()
    img = cv2.resize(frame, (size, size))
    img = cv2.equalizeHist(img)
    return img


def takePicture(cap, letter='', num=0, path='../data/images/', name=None):
    resized = capture(cap)
    if name is None:
        path += letter + str(num) + '.png'
    else:
        path += name + '.png'
    cv2.imwrite(path, resized)


def infinity(start=0):
    i = start
    while True:
        yield i
        i += 1


def get_start_index(path):
    import os
    files = os.listdir(path)
    if 'data.json' in files:
        files.remove('data.json')
    if len(files) == 0:
        return 0
    else:
        return max([int(x.split('.')[0][1:]) for x in files]) + 1


def main():
    camera_indexes = returnCameraIndexes()

    print(f'{camera_indexes=}')
    path = '../data/images/'
    loading = ['|', '/', '-', '\\']
    caps = [cv2.VideoCapture(camera_indexes[i]) for i in camera_indexes]
    if len(caps) == 0:
        print('No camera found')
        exit(1)
    elif len(caps) == 1:
        print('Only one camera found')
        labels = ['L']
    elif len(caps) == 2:
        labels = ['L', 'R']
    else:
        print('More than two cameras found')
        exit(1)

    start_index = get_start_index(path)
    print(f'{start_index=}')
    for i in infinity(start_index):
        try:
            for cap, label in zip(caps, labels):
                takePicture(cap, label, i, path)

            time.sleep(0.5)
            print(f'\rCapturing index {i=}, {loading[i % len(loading)]}', end='')

        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            break

    for cap in caps:
        cap.release()


if __name__ == "__main__":
    main()
