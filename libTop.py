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
predictor = dlib.shape_predictor(predictorPath)
faceRec = dlib.face_recognition_model_v1(faceRecPath)

def getFaceRects(img, upsample=0):
    return faceLocations = detector(img, upsample)

def getFaceLandmarks(img, rects):
    return [predictor(img, f) for f in faceLocations]

def getFaceDescriptors(img, rects, jitter = 0):
    landmarks = getFaceLandmarks(img, rects)
    return [np.array(fareRec(img, l, jitter)) for l in landmarks]

def faceDistance(faceDescriptor1, faceDescriptor2):
    return np.linalg.norm(faceDecscriptor1-faceDescriptor2)

