import cv2
import libTop as lb
import matplotlib.pyplot as plt
from dbClass import Database
import shutil
bd = Database()
import os
SKIP = 3
lista = os.listdir('video')
lista.sort()
font = cv2.FONT_HERSHEY_SIMPLEX 
for l in lista:
    frame = cv2.imread('video/'+ l, cv2.IMREAD_COLOR)
    detections = bd.addImg(frame)
    classe=None
    for det in detections:
        classe, tl, br = det
        if (classe is not None):
            cv2.putText(frame, str(classe), (tl[0], br[1]), font, 1, (255,0,0), 2, cv2.LINE_AA)
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
