import cv2
import libTop as lb
import matplotlib.pyplot as plt
from dbClass import Database
import shutil
bd = Database()
import os
SKIP = 3
DISAPPEARED_MAX = 4
lista = os.listdir('video')
lista.sort()
font = cv2.FONT_HERSHEY_SIMPLEX
trackers = [] # [[tracker, classe, (tl,br), disappeared]]
#tracker = cv2.TrackerMIL_create() 
for l in lista:
    frame = cv2.imread('video/'+ l, cv2.IMREAD_COLOR)
    faceRects = lb.getFaceRects(frame)
    for i in range(len(trackers)):
        if (trackers[i][3] == DISAPPEARED_MAX):
            trackers[i] = None
        else:
            ok, bbox = trackers[i].update(frame)
            if ok:
                tl = (int(bbox[0]), int(bbox[1]))
                br = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                trackers[i][3] = (tl,br)
            else:   
                print("Classe " + str(trackers[i][1]) + " foi perdida")
                trackers[i]=None
    trackers = [t for t in trackers if t is not None ]
    for t in trackers:
        for f in faceRects:
            
    for i in range(len(faceRects)):
        x, y, w, h = faceRects[i].left(), faceRects[i].top(),faceRects[i].width(), faceRects[i].height()
        tl = (x,y)
        br = (x + w, y + h)
        distances.append([])
        for j in range(len(trackers)):
            d = lb.distance(trackers[j][3],(tl,br))
            
            

    detections = bd.addImg(frame)
    classe=None
    for det in detections:
        classe, tl, br = det
        if (classe is not None):
            cv2.putText(frame, "Classe "+ str(classe), (tl[0], br[1]+30), font, 1, (255,0,0), 2, cv2.LINE_AA)
            cv2.rectangle(frame, tl, br, (255,0,0), 2)
        else:
            pass
    cv2.imshow("Output", frame)
   # if (classe is not None):
       # cv2.waitKey(0)
    #cv2.waitKey(0)
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break

    
cv2.destroyAllWindows()

shutil.rmtree('bd', ignore_errors=True)
os.mkdir('bd')
for k,v in bd.faces.items():
    i=0
    os.mkdir('bd/'+str(k))
    for elem in v:

        cv2.imwrite('bd/'+str(k)+'/'+str(i)+'.jpg', elem[1])
        i+=1
