#http://dlib.net/face_detector.py.html
#https://www.learnopencv.com/object-tracking-using-opencv-cpp-python/
#https://medium.com/machinelearningadvantage/find-all-faces-that-are-looking-directly-at-the-camera-with-c-59e8469696c1
#https://www.learnopencv.com/head-pose-estimation-using-opencv-and-dlib/
#https://github.com/ageitgey/face_recognition/issues/357
#https://answers.opencv.org/question/16796/computing-attituderoll-pitch-yaw-from-solvepnp/

from imutils import face_utils
import dlib
import cv2
import numpy as np
import valdirlib as vl
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
print(major_ver, major_ver, subminor_ver)

p = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)


detecting = True
tracker = cv2.TrackerMedianFlow_create()
cap = cv2.VideoCapture(0)
if cap.isOpened() == False:
    print("Erro na stream")

count = 10
while cap.isOpened():
    if (count < 10):
        count +=1
    else:
        count =0
        status, frame = cap.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #small_frame = cv2.resize(gray_frame, (0, 0), fx=0.25, fy=0.25) #Scaling to 1/4
        #print(np.max(small_frame))
        #rects = detector(gray_frame,0)
        #for i, d in enumerate(dets):
    #     print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
    #         i, d.left(), d.top(), d.right(), d.bottom()))
        #break

        rects = detector(gray_frame, 0)
        #print(len(rects))  
            # para cada face encontrada, encontre os pontos de interesse.
        for (i, rect) in enumerate(rects):
            # faça a predição e então transforme isso em um array do numpy.
            shape = predictor(gray_frame, rect)
            shape = face_utils.shape_to_np(shape)
            vl.angleEstimator(gray_frame, shape, 640, 480)
            # desenhe na imagem cada cordenada(x,y) que foi encontrado.
            #for (x, y) in shape:
            #    cv2.circle(gray_frame, (x, y), 2, (0, 255, 0), -1)


        if (status == False):
            print("Oopsie")
            break
    key = cv2.waitKey(1)
    if (key == ord('k')):
        #print(rects)
        #print(len(rects))
        break


    cv2.imshow("Output", gray_frame)
cap.release()
cv2.destroyAllWindows()