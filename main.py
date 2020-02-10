#http://dlib.net/face_detector.py.html
#https://www.learnopencv.com/object-tracking-using-opencv-cpp-python/
#https://medium.com/machinelearningadvantage/find-all-faces-that-are-looking-directly-at-the-camera-with-c-59e8469696c1
#https://www.learnopencv.com/head-pose-estimation-using-opencv-and-dlib/
#https://github.com/ageitgey/face_recognition/issues/357
#https://answers.opencv.org/question/16796/computing-attituderoll-pitch-yaw-from-solvepnp/
#https://medium.com/xailient/face-tracking-in-python-using-xailient-face-detector-and-dlib-8345c5db27b8

from imutils import face_utils
import dlib
import cv2
import numpy as np
import valdirlib2 as vl
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
import time
print(major_ver, major_ver, subminor_ver)

p = "dnn/shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)

detecting = True
tracker = cv2.TrackerMedianFlow_create()
cap = cv2.VideoCapture(0)
if cap.isOpened() == False:
    print("Erro na stream")

N = 3
count = N
tracker = cv2.TrackerMIL_create()
found=0
while cap.isOpened():
    if (count < N):     
        count +=1
    else:
        count =0
        status, frame = cap.read()
        if (found == 1):
            ok, bbox = tracker.update(frame)
            print(ok)
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25) #Scaling to 1/4
        #print(np.max(small_frame))
        #dets = detector(frame,0)
        #for i, d in enumerate(dets):k
    #     print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
    #         i, d.left(), d.top(), d.right(), d.bottom()))
        #break

      #  dets = detector(frame, 0)
        #print(len(dets))  
            # para cada face encontrada, encontre os pontos de interesse.
     #   for (i, rect) in enumerate(dets):
            # faça a predição e então transforme isso em um array do numpy.
           # shape = predictor(frame, rect)
           # shape = face_utils.shape_to_np(shape)
           # vl.angleEstimator(frame, shape)
            # desenhe na imagem cada cordenada(x,y) que foi encontrado.
          #  for (x, y) in shape:
           #     cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)



        if (status == False):
            print("Oopsie")
            break
        cv2.imshow("Output", frame)
        if (cv2.waitKey(1) & 0xFF == ord('q')):
            bbox = cv2.selectROI(frame, False)
            tracker.init(frame, bbox)
            found=1
        if (cv2.waitKey(1) & 0xFF == ord('k')):
            break


    
cap.release()
cv2.destroyAllWindows()