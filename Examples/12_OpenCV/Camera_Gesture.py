#!/usr/bin/env/python
# File name   : Camera_Gesture.py
# Website     : www.Adeept.com
# Author      : Adeept
# Date        : 2025/03/10
import io
import time
import cv2
import numpy as np
from picamera2 import Picamera2
from base_camera import BaseCamera
from flask import Flask, render_template, Response

app = Flask(__name__)
class Camera(BaseCamera):
    @staticmethod
    def frames():
        with Picamera2() as camera:
            camera.start()
            time.sleep(2)
            
            try:
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
                # Define the range of skin color in the HSV color space
                lower_skin = np.array([0, 20, 70], dtype=np.uint8)
                upper_skin = np.array([20, 255, 255], dtype=np.uint8)
                while True:
                    frame = camera.capture_array()
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    mask = cv2.inRange(hsv, lower_skin, upper_skin)
                    mask = cv2.medianBlur(mask, 5)

                    # Morphological operations: erosion and dilation
                    # mask = cv2.erode(mask, kernel, iterations=2)
                    # mask = cv2.dilate(mask, kernel, iterations=2)
                    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
                    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    if contours:
                        max_contour = max(contours, key=cv2.contourArea)
                        if cv2.contourArea(max_contour) > 500:
                            hull = cv2.convexHull(max_contour, returnPoints=False)
                            defects = cv2.convexityDefects(max_contour, hull)
                            if defects is not None:
                                num_defects = 0
                                for i in range(defects.shape[0]):
                                    s, e, f, d = defects[i, 0]
                                    start = tuple(max_contour[s][0])
                                    end = tuple(max_contour[e][0])
                                    far = tuple(max_contour[f][0])
                                    # Calculate the angle to determine if it is a convexity defect
                                    a = np.sqrt((end[0] - start[0]) ** 2+(end[1] - start[1]) ** 2)
                                    b = np.sqrt((far[0] - start[0]) ** 2+(far[1] - start[1]) ** 2)
                                    c = np.sqrt((end[0] - far[0]) ** 2+(end[1] - far[1]) ** 2)
                                    angle = np.arccos((b ** 2 + c ** 2 - a ** 2)/(2 * b * c)) * 57.2958
                                    if angle <= 90:
                                        num_defects += 1
                                        cv2.circle(frame, far, 5, [0, 0, 255], -1)
                                    if d > 10000:  
                                        num_defects += 1
                                if num_defects == 0:
                                    cv2.putText(frame, "Fist", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                                elif num_defects >= 4:
                                    cv2.putText(frame, "Open Hand", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                    
                    yield cv2.imencode('.jpg', frame)[1].tobytes()
   
            finally:
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