import sys
import cv2
import time
import sys


# sinistra L1.png ...
# destra L1.png ...

def capture(cap, size=28):
    (grabbed, frame) = cap.read()
    return cv2.resize(frame, (size, size))


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
    from checCameras import returnCameraIndexes
    camera_indexes = returnCameraIndexes()

    print(f'{camera_indexes=}')
    path = '../data/images/'
    loading = ['|', '/', '-', '\\']
    caps = [cv2.VideoCapture(camera_indexes[i]) for i in camera_indexes]
    match len(caps):
        case 0:
            print('No camera found')
            exit(1)
        case 1:
            print('Only one camera found')
            labels = ['L']
        case 2:
            labels = ['L', 'R']
        case _:
            print('More than two cameras found')
            exit(1)

    start_index = get_start_index(path)
    print(f'{start_index=}')
    for i in infinity(start_index):
        try:
            for cap, label in zip(caps, labels):
                takePicture(cap, label, i, path)

            time.sleep(0.5)
            sys.stdout.write(f'\rCapturing index {i=}, {loading[i % len(loading)]}')
            sys.stdout.flush()

        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            break

        time.sleep(1)

    for cap in caps:
        cap.release()


if __name__ == "__main__":
    main()
