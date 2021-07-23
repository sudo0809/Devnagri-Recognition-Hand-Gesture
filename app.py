from logging import captureWarnings
from flask import Flask, render_template, Response, request
import cv2
from flask.wrappers import Request
import numpy as np
import HandTrackingModule as htm
from utils import *


app = Flask(__name__)
camera = cv2.VideoCapture(0)
# camera.set(3, 1920)
# camera.set(4, 1080)
detector = htm.handDetector(detectionCon=0.8, trackCon=0.8)
global erase, capture
erase = 0
capture = 0


# def detect_face(frame):
#     face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
#     faces = face_cascade.detectMultiScale(frame, 1.3, 5)

#     if (len(faces) == 0):
#         return

#     for face in faces:
#         x, y, w, h = face
#         offset = 10  # extending 10 pixels oon all of the sides
#         face_section = frame[y-offset:y+h+offset, x-offset:x+w+offset]
#         face_section = cv2.resize(face_section, (100, 100))
#         cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)


# def overlayimage(main_img, stable_img):
#     # main_img keeps updating frame-wise
#     # main_img is a stable image and doesnt update every frame
#     canvasGray = cv2.cvtColor(stable_img, cv2.COLOR_BGR2GRAY)
#     _, canvasInv = cv2.threshold(
#         canvasGray, 50, 255, cv2.THRESH_BINARY_INV)
#     canvasInv = cv2.cvtColor(canvasInv, cv2.COLOR_GRAY2BGR)
#     imgCanvasCursor = cv2.bitwise_and(main_img, canvasInv)
#     imgCanvasCursor = cv2.bitwise_or(imgCanvasCursor, stable_img)
#     return imgCanvasCursor


def generate_frame():
    xp, yp = 0, 0
    global erase, capture
    # global imgCanvas
    imgCanvas = np.zeros((480, 640, 3), np.uint8)
    cursor = np.zeros((480, 640, 3), np.uint8)
    print("gen_function again")

    while True:
        success, frame = camera.read()
        frame = detector.findHands(frame)
        cursor = np.zeros((480, 640, 3), np.uint8)
        fingers_list = detector.findPosition(frame, draw=False)
        if len(fingers_list) != 0:
            index_y, index_x = fingers_list[8][1:]
            middle_y, middle_x = fingers_list[12][1:]

            fingersup = detector.fingersUp()
            # so if the fingers are up they will be 1 in numerical form

            if fingersup[1] and fingersup[2]:
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

        final_canvas = overlayimage(cursor, imgCanvas)

        if success:
            detect_face(frame)

        if capture:
            capture = 0
            now = "frame_img.png"   # datetime.datetime.now()
            # path = os.path.sep.join(['shots', "shot_{}.png".format(str(now).replace(":",''))])
            cv2.imwrite(now, frame)

        if erase:
            erase = 0
            print("Here")
            imgCanvas = np.zeros((480, 640, 3), np.uint8)

        frame = cv2.hconcat([frame, final_canvas])
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield(b"--frame\r\n"
                  b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


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
        if request.form.get('erase') == 'clear_screen':
            global erase
            erase = 1
    elif request.method == 'GET':
        return render_template('index.html')
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
