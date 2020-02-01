from imutils import face_utils
import dlib
import cv2
import numpy as np
import valdirlib as vl
import matplotlib.pyplot as plt
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
p = "dnn/shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)
frame = cv2.imread('sample.png', cv2.IMREAD_COLOR)

dets = detector(frame, 0)
for (i, rect) in enumerate(dets):
    # faça a predição e então transforme isso em um array do numpy.
    shape = predictor(frame, rect)
    teste = dlib.get_face_chip(frame, shape)
    shape = face_utils.shape_to_np(shape)
    #print(shape)
    plt.figure()
    plt.imshow(cv2.cvtColor(teste, cv2.COLOR_BGR2RGB))
    plt.show(block=False)
    vl.angleEstimator(frame, shape, 640, 480)
    # desenhe na imagem cada cordenada(x,y) que foi encontrado.
    for (x, y) in shape:
        cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
plt.figure()
plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
plt.show()
    #cv2.imshow("Output", frame)
key = cv2.waitKey()

cv2.destroyAllWindows()