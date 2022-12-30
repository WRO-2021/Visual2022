import sys
import cv2
import time


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


def main():
    path = '../data/images/'
    loading = ['|', '/', '-', '\\']
    caps = [
        cv2.VideoCapture(camera_indexes[0]),
        cv2.VideoCapture(camera_indexes[1])
    ]
    for i in infinity(1):
        try:

            takePicture(caps[0], 'L', i, path)
            takePicture(caps[1], 'R', i, path)

            time.sleep(0.5)
            sys.stdout.write(f'\rCapturing index {i=}, {loading[i % len(loading)]}')
            sys.stdout.flush()

        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            break

    for cap in caps:
        cap.release()


if __name__ == "__main__":
    from checCameras import returnCameraIndexes

    camera_indexes = returnCameraIndexes()
    main()
