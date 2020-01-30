from imutils import face_utils
import dlib
import cv2
import numpy as np
import lib
import valdirlib as vl
import json

p = "dnn/shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)
frame = cv2.imread('poses/C.jpg', cv2.IMREAD_COLOR)
frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
height, width = frame.shape[:2]
resolution =(width, height)
print(resolution)
dets = detector(frame, 0)
db = []

#print(dets)
#print(len(dets))  
    # para cada face encontrada, encontre os pontos de interesse.
for (i, rect) in enumerate(dets):
    #print(i)
    #print(rect)
    x, y, w, h = rect.left(), rect.top(), rect.width(), rect.height()

    tl = (x,y)
    br = (x + w, y + h)
   # print(tl,br)
    if (lib.isFaceValid(tl,br, resolution)):
        cv2.rectangle(frame, tl, br, (255,0,0), 2)    # faça a predição e então transforme isso em um array do numpy.
        shape = predictor(frame, rect)
        shape = face_utils.shape_to_np(shape)
        tl = (shape[0][0], shape[19][1])
        br = (shape[16][0],shape[8][1])
        print("New tl: ", tl, br)
        cv2.rectangle(frame, tl, br, (0,255,0), 2)
        #print(shape)
        new_shape = lib.normalizeShape(shape, tl, br)
        vl.angleEstimator(frame, shape, resolution[0], resolution[1])
        db.append({})


    # desenhe na imagem cada cordenada(x,y) que foi encontrado.
        i=0
        for (x, y) in shape:
           cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
           cv2.circle(frame, (new_shape[i][0], new_shape[i][1]), 2, (255, 255, 0), -1)
           i+=1
cv2.imshow("Output", frame)
cv2.waitKey()
cv2.destroyAllWindows()
