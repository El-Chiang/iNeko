# coding=utf-8
import requests
import json
import cv2


# Loading cat-face detector
cat_path = 'haarcascade_frontalcatface.xml'
face_cascade = cv2.CascadeClassifier(cat_path)


def recogn_face(img_url):
    img = requests.get(img_url)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.delectMultiScale(
        gray,
        scaleFactor=1.02,
        minNeighbors=3,
        minSize=(150, 150),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    if faces == ():
        return "NULL"
    for (x, y, w, h) in faces:
        cut_img = img[y: y + h, x: x + w]
    response = {
        'cut_img': cut_img,
        'x': x,
        'y': y,
        'w': w,
        'h': h
    }
    response = json.dumps(response)
    return response
    