from imutils import face_utils
import dlib
import cv2
import numpy as np
import lib
import valdirlib as vl
import json
import matplotlib.pyplot as plt
import os
import libTop as lb
address = "C:\\Users\\TOCA\\Andre\\ChinaIC\\poses"
lista = os.listdir(address)
import shutil
bd = {}

idNumber = 0
for l in lista:
    currImg = cv2.imread('poses/'+ l, cv2.IMREAD_COLOR)
   # currImg = cv2.resize(currImg, (0, 0), fx=0.5, fy=0.5)
    
    facesDetected = lb.getFaceRects(currImg, 0)
    faceDescriptors = lb.getFaceDescriptors(currImg, facesDetected)
    if (len(faceDescriptors) != len(facesDetected)):
        print("Putz")
    i=0
    for candidatoFd in faceDescriptors:
        print("k")
        if (l == 'IMG-20190613-WA0015.jpg'):
            print('cheguei')
            
        x, y, w, h = facesDetected[i].left(), facesDetected[i].top(), facesDetected[i].width(), facesDetected[i].height()
        tl = (x,y)
        br = (x + w, y + h)
        height, width = currImg.shape[:2]
        resolution =(width, height)
        print(lb.isFaceValid(tl,br,resolution))
        if (lb.isFaceValid(tl,br,resolution) is False):
            continue
                
            # plt.figure()
           # plt.subplot(121)
            
           # plt.subplot(122)
           # plt.show()
            
        if (len(bd.keys()) == 0):
            bd[idNumber] = []
            bd[idNumber].append((candidatoFd, currImg[y:y+h, x:x+w], l))
            idNumber+=1
        else:
            diferente = 1
            stop = 0
            for k,v in bd.items(): #Iterando pessoas
                distances = []
                if (stop == 1):
                    break
                for elem in v: # Iterando fotos de uma pessoa
                    distance = lb.faceDistance(candidatoFd, elem[0])
                    plt.imshow(elem[1])
                    print(distance)
                    distances.append(distance)
                minima = np.min(distances)
                if (minima > 0.5):
                    print("Pessoa diferente")
                    #bd[idNumber] = []
                    #bd[idNumber].append((candidatoFd, currImg[y:y+h, x:x+w]))
                    #idNumber+=1
                    #break
                elif (minima >= 0.1 and minima <= 0.49):
                    diferente = 0
                    stop = 1
                    print("Igual, mas vale add")
                    bd[k].append((candidatoFd, currImg[y:y+h, x:x+w], l))
                    break
                else:
                    diferente = 0
                    stop = 1
                    print("Igual, mas faça nada")
            if (diferente ==1):
                print("Adicionou")
                bd[idNumber] = []
                bd[idNumber].append((candidatoFd, currImg[y:y+h, x:x+w], l))
                idNumber+=1           
            i+=1
            pass
    
shutil.rmtree('C:\\Users\\TOCA\\Andre\\ChinaIC\\bd', ignore_errors=True)
os.mkdir('C:\\Users\\TOCA\\Andre\\ChinaIC\\bd')
for k,v in bd.items():
    i=0
    os.mkdir('C:\\Users\\TOCA\\Andre\\ChinaIC\\bd\\'+str(k))
    for elem in v:
        cv2.imwrite('C:\\Users\\TOCA\\Andre\\ChinaIC\\bd\\'+str(k)+'\\'+str(i)+'.jpg', elem[1])
        i+=1


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