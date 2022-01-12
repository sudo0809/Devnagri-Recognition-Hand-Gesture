from logging import captureWarnings
from flask import Flask, render_template, Response, request
from flask.wrappers import Request
import cv2
import numpy as np
from numpy.core.fromnumeric import size
import HandTrackingModule as htm
from utils import *
from keras.models import load_model


WIDTH = 480  # x-axis
HEIGHT = 640  # y-axis
WHITE = (255, 255, 255)  # white color
BLACK = (0, 0, 0)


app = Flask(__name__)
camera = cv2.VideoCapture(0)
detector = htm.handDetector(detectionCon=0.8, trackCon=0.8)
global erase, capture, imgCanvas
erase = 0
capture = 0


def generate_frame():
    xp, yp = 0, 0
    global erase, capture
    global imgCanvas
    imgCanvas = np.zeros((WIDTH, HEIGHT, 3), np.uint8)
    cursor = np.zeros((WIDTH, HEIGHT, 3), np.uint8)
    # print("gen_function again")

    while True:
        success, frame = camera.read()
        frame = detector.findHands(frame)
        cursor = np.zeros((WIDTH, HEIGHT, 3), np.uint8)
        fingers_list = detector.findPosition(frame, draw=False)
        if len(fingers_list) != 0:
            index_y, index_x = fingers_list[8][1:]
            middle_y, middle_x = fingers_list[12][1:]

            fingersup = detector.fingersUp()
            # so if the fingers are up they will be 1 in numerical form

            if fingersup[1] and fingersup[2] and fingersup[3] == 0:
                cv2.rectangle(frame, (index_x, index_y),
                              (middle_x, middle_y), (255, 0, 255), cv2.FILLED)
                xp, yp = 0, 0
                cv2.circle(cursor, (index_x, index_y), 15, (255, 0, 0), 3)
                # print("Selection mode")

            if fingersup[1] and fingersup[2] == 0:
                cv2.circle(frame, (index_x, index_y),
                           10, (255, 0, 255), cv2.FILLED)
                # print("Drawing mode")
                if xp == 0 and yp == 0:
                    xp, yp = index_x, index_y
                cv2.line(frame, (xp, yp), (index_x, index_y),
                         (255, 255, 255), 10)
                cv2.line(imgCanvas, (xp, yp),
                         (index_x, index_y), (255, 255, 255), 10)

                xp, yp = index_x, index_y

            if fingersup[1] and fingersup[2] and fingersup[3] and fingersup[4]:
                # eraser mode
                cv2.circle(cursor, (index_x, index_y), 15, (255, 100, 140), 3)
                if xp == 0 and yp == 0:
                    xp, yp = index_x, index_y

                cv2.line(frame, (xp, yp), (index_x, index_y), BLACK, 20)
                cv2.line(imgCanvas, (xp, yp), (index_x, index_y), BLACK, 20)
                xp, yp = index_x, index_y

        final_canvas = overlayimage(cursor, imgCanvas)

        if success:
            detect_face(frame)

        if capture:
            capture = 0

        if erase:
            erase = 0
            print("Here")
            imgCanvas = np.zeros((WIDTH, HEIGHT, 3), np.uint8)

        frame = cv2.hconcat([frame, final_canvas])
        screen = frame

        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', screen)
            screen = buffer.tobytes()
            yield(b"--frame\r\n"
                  b"Content-Type: image/jpeg\r\n\r\n" + screen + b"\r\n")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def video():
    return Response(generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/requests', methods=['GET', 'POST'])
def tasks():

    if request.method == 'POST':
        if request.form.get('click') == 'capture':
            global capture
            capture = 1
            model = load_model('model\devnagri_model_2.h5')
            predict_img = prepare_image(imgCanvas)
            prediction, letter = get_key(np.argmax(model.predict(predict_img)))
            print(prediction, letter)
            return render_template('index.html', prediction_text="the letter is {}".format(letter))

        if request.form.get('erase') == 'clear_screen':
            global erase
            erase = 1
    elif request.method == 'GET':
        return render_template('index.html')
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
