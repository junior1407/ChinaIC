import cv2
import libTop as lb
import matplotlib.pyplot as plt
from dbClass import Database
import shutil
bd = Database()
import os
SKIP = 3

nextId = 0
db = []
lista = os.listdir('video')
count = 0
iD=0
lista.sort()
print(lista)
for l in lista:
    frame = cv2.imread('video/'+ l, cv2.IMREAD_COLOR)
    detections = bd.addImg(frame)
    for det in detections:
        classe, tl, br = det
        cv2.rectangle(frame, tl, br, (255,0,0), 2)
    cv2.imshow("Output", frame)
    iD+=1
    cv2.waitKey(0)
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
