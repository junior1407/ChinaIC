
import cv2
import libTop as lb
import matplotlib.pyplot as plt
from dbClass import Database
from centroidTracker import CentroidTracker
import shutil
bd = Database()
import os
SKIP = 3
DISAPPEARED_MAX = 4
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX
ct = CentroidTracker(bd)
while cap.isOpened():
    status, frame = cap.read()
    faceRects = lb.getFaceRects(frame)
    retorno = ct.processRects(frame, faceRects)
    for r in retorno:
        tlbr = r[1]
        tl,br = tlbr
        classe= r[2]
        if (classe is not None):
            cv2.putText(frame, "Classe "+ str(classe), (tl[0], br[1]+30), font, 1, (255,0,0), 2, cv2.LINE_AA)
            cv2.rectangle(frame, tl, br, (255,0,0), 2)
    cv2.imshow("Output", frame)
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break

    
cv2.destroyAllWindows()
