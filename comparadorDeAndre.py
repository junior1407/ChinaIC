from imutils import face_utils
import dlib
import cv2
import numpy as np
import lib
import valdirlib as vl
import json
import matplotlib.pyplot as plt

predictorPath = "dnn/shape_predictor_68_face_landmarks.dat"
face_rec_model_path= "dnn/dlib_face_recognition_resnet_model_v1.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictorPath)
facerec = dlib.face_recognition_model_v1(face_rec_model_path)
andre1= cv2.imread('poses/valdir2.jpeg', cv2.IMREAD_COLOR)
#andre1= cv2.resize(andre1, (0, 0), fx=0.5, fy=0.5)
andre2= cv2.imread('poses/boys.jpeg', cv2.IMREAD_COLOR)
#andre2= cv2.resize(andre2, (0, 0), fx=0.5, fy=0.5)

height, width = andre1.shape[:2]
resolution =(width, height)

dets1 = detector(andre1, 0)
shape1 = predictor(andre1, dets1[0])
andre1 = dlib.get_face_chip(andre1, shape1)
dets1 = detector(andre1, 0)
shape1 = predictor(andre1, dets1[0])
descript1 = facerec.compute_face_descriptor(andre1, shape1)

dets2 = detector(andre2, 1)
shape2 = predictor(andre2, dets2[2])
andre2 = dlib.get_face_chip(andre2, shape2)
dets2 = detector(andre2, 1)
shape2 = predictor(andre2, dets2[0])
descript2 = facerec.compute_face_descriptor(andre2, shape2),

euclidean_distance = np.linalg.norm(np.array(descript1)-np.array(descript2))
plt.figure(200)
plt.subplot(1,2,1)
plt.imshow(cv2.cvtColor(dlib.get_face_chip(andre1, shape1), cv2.COLOR_BGR2RGB))
plt.subplot(1,2,2)
#dlib.get_face_chip(andre2, shape2)
plt.imshow(cv2.cvtColor(dlib.get_face_chip(andre2, shape2), cv2.COLOR_BGR2RGB))
plt.title("Euclidean distance = "+str(euclidean_distance))
plt.show(block=False)

print(euclidean_distance)
print(dets1)
key = cv2.waitKey()
plt.show()