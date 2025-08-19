#!/usr/bin/env/python
# File name   : DynamicsMatrix.py
# Website     : www.Adeept.com
# Author      : Adeept
# Date        : 2025/07/24
import time
import board
import busio
from adafruit_ht16k33 import matrix

i2c = busio.I2C(board.SCL, board.SDA)

matrix_display = matrix.Matrix16x8(i2c, address=0x70)

# Define the pixel data of the smiling face
smile_array1 = bytes([
    0x00,0x00,0x04,0x02,0x02,0x24,0x40,0x40,
    0x40,0x40,0x24,0x02,0x02,0x04,0x00,0x00,
])
smile_array2 = bytes([
  0x00,0x08,0x4,0x02,0x04,0x08,0x00,0x00,
  0x00,0x00,0x08,0x4,0x02,0x04,0x08,0x00,
])

# initialization function
def setup():
    matrix_display.fill(0)  # Clear the matrix
    matrix_display.brightness = 1.0  # set brightness (0.0-1.0)
    
# Display smiley face function
def display_array(array):
    for i in range(8):  
        matrix_display._buffer[i*2+1] = array[i]
        matrix_display._buffer[i*2+2] = array[i+8]
    matrix_display.show()

def loop():
    try:
        while True:
            display_array(smile_array1)
            time.sleep(1)
            display_array(smile_array2)
            time.sleep(1)
    except KeyboardInterrupt:
        matrix_display.fill(0) 
        print("\nThe LED matrix has safely stopped")

if __name__ == "__main__":
    setup()
    loop()