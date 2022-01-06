import cv2
import numpy as np
from symbols import *


def detect_face(frame):
    face_cascade = cv2.CascadeClassifier(
        'face_detection/haarcascade_frontalface_alt.xml')
    faces = face_cascade.detectMultiScale(frame, 1.3, 5)

    if (len(faces) == 0):
        return

    for face in faces:
        x, y, w, h = face
        offset = 10  # extending 10 pixels oon all of the sides
        face_section = frame[y-offset:y+h+offset, x-offset:x+w+offset]
        face_section = cv2.resize(face_section, (100, 100))
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)


def overlayimage(main_img, stable_img):
    # main_img keeps updating frame-wise
    # main_img is a stable image and doesnt update every frame
    canvasGray = cv2.cvtColor(stable_img, cv2.COLOR_BGR2GRAY)
    _, canvasInv = cv2.threshold(
        canvasGray, 50, 255, cv2.THRESH_BINARY_INV)
    canvasInv = cv2.cvtColor(canvasInv, cv2.COLOR_GRAY2BGR)
    imgCanvasCursor = cv2.bitwise_and(main_img, canvasInv)
    imgCanvasCursor = cv2.bitwise_or(imgCanvasCursor, stable_img)
    return imgCanvasCursor


def prepare_image(img):
    dim = (32, 32)  # beacuse we trained the model with this dimention of images
    # img = cv2.imread(img, cv2.IMREAD_UNCHANGED)
    resized_img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    resized_img = resized_img[:, :, :3]  # we need only 3 channels

    final_img = resized_img[np.newaxis, ...]  # adding new axis for the model
    return final_img


def get_key(value):
    for key, val in symbol_map.items():
        if val == value:
            return key, letters[value]
