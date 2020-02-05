import cv2
import numpy as np
import lib
import valdirlib as vl
import json
import matplotlib.pyplot as plt
import os
import libTop as lb
from dbClass import Database
import shutil
bd = Database()
lista = os.listdir('poses')
for l in lista:
    print(l)
    currImg = cv2.imread('poses/'+ l, cv2.IMREAD_COLOR)
    bd.addImg(currImg)
   # currImg = cv2.resize(currImg, (0, 0), fx=0.5, fy=0.5)
    
    
shutil.rmtree('bd', ignore_errors=True)
os.mkdir('bd')
#for k,v in bd['faces'].items():
 #   i=0
  #  os.mkdir('bd/'+str(k))
   # for elem in v:
    #    cv2.imwrite('bd/'+str(k)+'/'+str(i)+'.jpg', elem[1])
     #   i+=1


#euclidean_distance = np.linalg.norm(np.array(descript1)-np.array(descript2))
#plt.figure(200)
#plt.subplot(1,2,1)
#plt.imshow(cv2.cvtColor(andre1, cv2.COLOR_BGR2RGB))
#plt.subplot(1,2,2)
#dlib.get_face_chip(andre2, shape2)
#plt.imshow(cv2.cvtColor(andre2, cv2.COLOR_BGR2RGB))
#plt.title("Euclidean distance = "+str(euclidean_distance))

##print(euclidean_distance)
#rint(dets1)
#plt.show()