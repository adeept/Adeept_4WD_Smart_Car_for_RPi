#!/usr/bin/env/python
# File name   : Camera_FindColor.py
# Website     : www.Adeept.com
# Author      : Adeept
# Date        : 2025/03/10
import io
import time
import cv2
import numpy as np
from picamera2 import Picamera2
from base_camera import BaseCamera
import os
from flask import Flask, render_template, Response

app = Flask(__name__)
class Camera(BaseCamera):
    @staticmethod
    def frames():
        # Open the camera using Picamera2
        with Picamera2() as camera:
            # Start the camera
            camera.start()
            # Wait for 2 seconds to let the camera warm up
            time.sleep(2)
            # Create a ByteIO object to store image data
            stream = io.BytesIO()
            # Create an elliptical structuring element for morphological operations
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            try:
                while True:
                    # Capture an image from the camera and save it to the ByteIO stream in JPEG format
                    camera.capture_file(stream, format='jpeg')
                    # Move the pointer of the ByteIO stream to the beginning
                    stream.seek(0)
                    # Read data from the ByteIO stream and decode it into an image
                    frame = cv2.imdecode(np.frombuffer(stream.read(), dtype=np.uint8), cv2.IMREAD_COLOR)
                    # Convert the image from BGR color space to HSV color space
                    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    # Define the lower bound of yellow in the HSV color space
                    lower = np.array([20, 100, 100], dtype=np.uint8)
                    # Define the upper bound of yellow in the HSV color space
                    upper = np.array([30, 255, 255], dtype=np.uint8)
                    # Create a mask based on the color range
                    mask = cv2.inRange(hsv, lower, upper)
                    # Perform erosion operation on the mask, with 2 iterations
                    mask = cv2.erode(mask, kernel, iterations=2)
                    # Perform dilation operation on the mask, with 2 iterations
                    mask = cv2.dilate(mask, kernel, iterations=2)
                    # Find contours in the mask
                    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    for contour in contours:
                        # If the contour area is greater than 500
                        if cv2.contourArea(contour) > 500:
                            # Calculate the bounding rectangle of the contour
                            x, y, w, h = cv2.boundingRect(contour)
                            # Draw a green rectangle on the original image to mark the object's position
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            # Add the text label "Yellow Object" above the rectangle
                            cv2.putText(frame, "Yellow Object", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    # Encode the processed image into JPEG format
                    _, encoded_frame = cv2.imencode('.jpg', frame)
                    # Return the encoded image data through a generator
                    yield encoded_frame.tobytes()
                    # Move the pointer of the ByteIO stream to the beginning
                    stream.seek(0)
                    # Clear the content of the ByteIO stream
                    stream.truncate()
            finally:
                # Stop the camera
                camera.stop()
@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    yield b'--frame\r\n'
    while True:
        frame = camera.get_frame()
        yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)