from imutils import face_utils
import dlib
import cv2
import numpy as np
import lib
import valdirlib2 as vl
import json
import matplotlib.pyplot as plt

predictorPath = "dnn/shape_predictor_68_face_landmarks.dat"
faceRecPath = "dnn/dlib_face_recognition_resnet_model_v1.dat"
detector = dlib.get_frontal_face_detector()
#detector = dlib.cnn_face_detection_model_v1("dnn/mmod_human_face_detector.dat")
predictor = dlib.shape_predictor(predictorPath)
faceRec = dlib.face_recognition_model_v1(faceRecPath)


def isFaceValid(img, rect):
    height, width = img.shape[:2]
    resolution =(width, height)
    x, y, w, h = rect.left(), rect.top(), rect.width(), rect.height()
    tl = (x,y)
    br = (x + w, y + h)
    if((tl[0]>=0 and tl[0]<=resolution[0]) and 
        (tl[1]>=0 and tl[1]<=resolution[1]) and 
        (br[0]>=0 and br[0]<=resolution[0]) and
        (br[1]>=0 and br[1]<=resolution[1])):
        return True
    return False
    

def getFaceRects(img, upsample=0):
    return detector.run(img, 0)
    #return detector(img, upsample)

def getFaceLandmarks(img, rects):
    return [predictor(img, f) for f in rects]

def getFaceDescriptors(img, rects, jitter = 0):
    landmarks = getFaceLandmarks(img, rects)
    return [np.array(faceRec.compute_face_descriptor(img, l, jitter)) for l in landmarks]

def faceDistance(faceDescriptor1, faceDescriptor2):
    return np.linalg.norm(faceDescriptor1-faceDescriptor2)

