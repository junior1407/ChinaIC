import libTop as lb
import numpy as np
import heapq
import matplotlib.pyplot as plt
class Database:
    def __init__(self):
         self.nextId = 0
         self.faces = {}
    def findBestClass(self, faceDescriptor):
        distances = []  # [  (distance1, id1), (distance2, id2)]
        
        for iD, entries in self.faces.items():
            d = 0
            for entry in entries:
        ##        d = lb.faceDistance(faceDescriptor, entry[0])
                d+= lb.faceDistance(faceDescriptor, entry[0])
         ##   distances.append((iD, d))
            distances.append((iD, d/len(entries)))

        distances.sort(key= lambda x: x[1])        
        return distances[0]
    def addFace(self, faceDescriptor, imgCropped):
         if (len(self.faces.keys()) == 0):
            self.faces[0]= np.array([[faceDescriptor, imgCropped]])
            self.nextId+=1
            return 0
         else:
             bestId, bestDistance = self.findBestClass(faceDescriptor)             
             if (bestDistance >= 0.6):
                 self.faces[self.nextId] = np.array([[faceDescriptor, imgCropped]])
                 self.nextId+=1
                 return (self.nextId-1)
             elif (bestDistance >=0.4):
                self.faces[bestId] = np.append(self.faces[bestId],[[faceDescriptor, imgCropped]], axis=0)
                return bestId
             else:
                return bestId
    def identifyFace(self, img, rect):
        descriptor = lb.getFaceDescriptor(img, rect)
        x, y, w, h = rect.left(), rect.top(), rect.width(), rect.height()
        imgCropped = img[y:y + h, x:x + w]
        return self.addFace(descriptor, imgCropped)

    def addImg(self, img, upsample=0, minimumScore = 0.22):
        facesDetected= lb.getFaceRects(img, 0)
#        print(scores)
        faceDescriptors = lb.getFaceDescriptors(img, facesDetected)
        retorno = []
        for i in range(len(facesDetected)):
            #If the part of the face is not visible, ignore it.
            if (lb.isFaceValid(img, facesDetected[i]) is False):
                continue
            
            #if (not (abs(pitch) <= 20 and abs(roll)<=20 and abs(yaw)<=20)):
             #   continue

            x, y, w, h = facesDetected[i].left(),facesDetected[i].top(),facesDetected[i].width(), facesDetected[i].height()
            
            r = self.addFace(faceDescriptors[i], img[y:y+h, x:x+w]),(x,y),(x+w, y+h)
            #print(r)
            retorno.append(r)
        return retorno
   
            
        
        



            


            

