# coding=utf-8
import requests
import json
import os
import cv2
import time

def recogn_face(img_url):

    # Loading cat-face detector
    cat_path = 'haarcascade_frontalcatface.xml'
    face_cascade = cv2.CascadeClassifier(cat_path)

    img = requests.get(img_url)
    fname = 'temp.jpg'
    f = open(fname, 'wb')
    f.write(img.content)
    f.close()
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.02,
        minNeighbors=3,
        minSize=(150, 150),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    os.remove(fname)
    if faces == ():
        return "NULL"
    for (x, y, w, h) in faces:
        cut_img = img[y: y + h, x: x + w]
    path = '/' + str(time.time()) + '.jpg'
    cv2.imwrite(path, cut_img)
    response = {
        'cut_img': '/' + path,
        'x': str(x),
        'y': str(y),
        'w': str(w),
        'h': str(h)
    }
    response = json.dumps(response)
    print(response)
    return response


recogn_face('https://raw.githubusercontent.com/El-Chiang/iNeko/master/images/pipi/63.jpg')