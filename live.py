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
videoCapture = cv2.VideoCapture(0)
if videoCapture.isOpened() == False:
    print("Erro na stream")
count = 0
iD=0
while(videoCapture.isOpened()):
    _status, frame = videoCapture.read()
    if (count < SKIP):
        count+=1
    else:
        count=0
        #rects = lb.getFaceRects(frame)
        bd.addImg(frame)
        cv2.imshow("Output", frame)
        cv2.imwrite("video/" + "{:04d}".format(iD) +".jpg", frame)
        iD+=1
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break

    
videoCapture.release()
cv2.destroyAllWindows()

shutil.rmtree('bd', ignore_errors=True)
os.mkdir('bd')
for k,v in bd.faces.items():
    i=0
    os.mkdir('bd/'+str(k))
    for elem in v:
        cv2.imwrite('bd/'+str(k)+'/'+str(i)+'.jpg', elem[1])
        i+=1
