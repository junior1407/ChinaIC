from imutils import face_utils
import dlib
import cv2
import numpy as np
import lib
import valdirlib as vl
import json
import matplotlib.pyplot as plt
plt.close('all')

predictorPath = "dnn/shape_predictor_68_face_landmarks.dat"
predictor5Path = "dnn/shape_predictor_5_face_landmarks.dat"
face_rec_model_path= "dnn/dlib_face_recognition_resnet_model_v1.dat"
detector = dlib.get_frontal_face_detector()
#detector = dlib.cnn_face_detection_model_v1("dnn/mmod_human_face_detector.dat")
predictor = dlib.shape_predictor(predictorPath)
predictor5 = dlib.shape_predictor(predictor5Path)
facerec = dlib.face_recognition_model_v1(face_rec_model_path)
frame = cv2.imread('poses/0037.jpg', cv2.IMREAD_COLOR)
#frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
height, width = frame.shape[:2]
resolution =(width, height)
dets = detector(frame, 0)
#db = []
print(dets)
#iterate faces found.
print(len(dets))
for (i, rect) in enumerate(dets):
    x, y, w, h = rect.left(), rect.top(), rect.width(), rect.height()
    tl = (x,y)
    br = (x + w, y + h)
    #if (lib.isFaceValid(tl,br, resolution)):
     #   cv2.rectangle(frame, tl, br, (255,0,0), 2)
    shape = predictor5(frame, rect) # 5 points
    chip = dlib.get_face_chip(frame, shape)
    shape = predictor(chip, dlib.rectangle(0,0,149,149))
        #descriptor = facerec.compute_face_descriptor(frame, shape)
        #print(descriptor)
        #shape = dlib.get_face_chip(frame, shape) #Align
    shape = face_utils.shape_to_np(shape) # to numpy Array
    for (x, y) in shape:
        pass
        #cv2.circle(chip, (x, y), 2, (0, 255, 0), -1)
    plt.figure()
    plt.imshow(chip)
    plt.show()
       #tl = (shape[0][0], shape[19][1])
        #br = (shape[16][0],shape[8][1])
        #print("New tl: ", tl, br)
        #cv2.rectangle(frame, tl, br, (0,255,0), 2)
        #print(shape)
       # new_shape = lib.normalizeShape(shape, tl, br)
       # vl.angleEstimator(frame, shape, resolution[0], resolution[1])
        #db.append({})

    # desenhe na imagem cada cordenada(x,y) que foi encontrado.
   #     i=0
    #    for (x, y) in shape:
     #      cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
      #     cv2.circle(frame, (new_shape[i][0], new_shape[i][1]), 2, (255, 255, 0), -1)
       #    i+=1
#cv2.imshow("Output", frame)
#plt.imshow(frame)
plt.show()
#cv2.waitKey()w
cv2.destroyAllWindows()
