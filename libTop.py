from imutils import face_utils
import dlib
import cv2
import numpy as np
import lib
import valdirlib2 as vl
import json
import matplotlib.pyplot as plt
import math
from scipy import stats

predictorPath5 = "dnn/shape_predictor_5_face_landmarks.dat"
predictorPath = "dnn/shape_predictor_68_face_landmarks.dat"
faceRecPath = "dnn/dlib_face_recognition_resnet_model_v1.dat"
detector = dlib.get_frontal_face_detector()
#detector = dlib.cnn_face_detection_model_v1("dnn/mmod_human_face_detector.dat")
predictor = dlib.shape_predictor(predictorPath)
predictor5 = dlib.shape_predictor(predictorPath5)
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
    
def distance(centroid1, centroid2):
    x_1, y_1 = centroid1
    x_2, y_2 = centroid2
    return math.sqrt( ((x_1-x_2)**2)+((y_1-y_2)**2) )

def getFaceRects(img, upsample=0):
    #return detector.run(img, 0)
    return detector(img, upsample)
    #for 

def getFaceLandmarks(img, rects, points = 5):
    if (points == 5):    
        return [predictor5(img, f) for f in rects]
    return [predictor(img, f) for f in rects]

def getFaceDescriptor(img, rect):
    rects =  dlib.rectangles()
    rects.append(rect)
    return getFaceDescriptors(img, rects)[0]

def getFaceDescriptors(img, rects, jitter = 0):
    landmarks5 = getFaceLandmarks(img, rects)
    #chips = dlib.get_face_chips(img, landmarks5)
    descriptors = []
    for l5 in landmarks5:
        c = dlib.get_face_chip(img, l5)
        new_rs = dlib.rectangles()
        new_rs.append(dlib.rectangle(0,0,149,149))
        l = getFaceLandmarks(c, new_rs, points=68)
        descriptors.append(np.array(faceRec.compute_face_descriptor(c,l[0],jitter)))
        
    #descriptors = [faceRec.compute_face_descriptor(c, getFaceLandmarks(c, 
  #                                dlib.rectangle(0,0,149,149), points=68), jitter)for c in chips]
   # descriptors=  [np.array(faceRec.compute_face_descriptor(img, l, jitter)) for l in landmarks]
    #directions = [vl.angleEstimator(img, face_utils.shape_to_np(l)) for l in landmarks]
    return descriptors


def faceDistance(faceDescriptor1, faceDescriptor2):
    #ks = stats.ks_2samp(faceDescriptor1, faceDescriptor2)
    #print(ks)
    #print(np.linalg.norm(faceDescriptor1-faceDescriptor2))
    #return ks[0]
    return np.linalg.norm(faceDescriptor1-faceDescriptor2)

