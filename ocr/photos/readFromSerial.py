import serial
import time

arduino = serial.Serial(port='COM4', baudrate=115200, timeout)

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data

while True:
    num = input("Number: ")
    value = write_read(num)
    print(value)