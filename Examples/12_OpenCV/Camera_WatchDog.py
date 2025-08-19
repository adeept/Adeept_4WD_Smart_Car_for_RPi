#!/usr/bin/env/python
# File name   : Camera_WatchDog.py
# Website     : www.Adeept.com
# Author      : Adeept
# Date        : 2025/03/10
import io
import time
import cv2
import imutils
import numpy as np
from picamera2 import Picamera2
from base_camera import BaseCamera
import datetime
from flask import Flask, render_template, Response


app = Flask(__name__)
class Camera(BaseCamera):
    def __init__(self):
        super().__init__()
        self.avg = None
        self.drawing = 0
        self.motionCounter = 0
        self.lastMovtionCaptured = datetime.datetime.now()

    def watchDog(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if self.avg is None:
            print("[INFO] starting background model...")
            self.avg = gray.copy().astype("float")
            return frame

        cv2.accumulateWeighted(gray, self.avg, 0.5)
        frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(self.avg))

        thresh = cv2.threshold(frameDelta, 5, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        for c in cnts:
            if cv2.contourArea(c) < 5000:
                continue
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            self.drawing = 1
            self.motionCounter += 1
            self.lastMovtionCaptured = datetime.datetime.now()

        if (datetime.datetime.now() - self.lastMovtionCaptured).seconds >= 0.5:
            self.drawing = 0

        return frame

    @staticmethod
    def frames():
        with Picamera2() as camera:
            camera.start()
            time.sleep(2)
            stream = io.BytesIO()
            camera_ins = Camera()
            try:
                while True:
                    camera.capture_file(stream, format='jpeg')
                    stream.seek(0)
                    frame = cv2.imdecode(np.frombuffer(stream.read(), dtype=np.uint8), cv2.IMREAD_COLOR)
                    processed_frame = camera_ins.watchDog(frame)
                    _, encoded_frame = cv2.imencode('.jpg', processed_frame)
                    yield encoded_frame.tobytes()
                    stream.seek(0)
                    stream.truncate()
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