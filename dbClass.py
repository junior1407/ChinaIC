import libTop as lb
import numpy as np
import heapq
class Database:
    
    def __init__(self):
         self.nextId = 0
         self.faces = {}
    def findBestClass(self, faceDescriptor):
        #distances  = [(iD, lb.faceDistance(faceDescriptor, entry[0])) for iD, entries in self.faces for entry in entries]
        distances = []  # [  (distance1, id1), (distance2, id2)]
        for iD, entries in self.faces.items():
            for entry in entries:
                d = lb.faceDistance(faceDescriptor, entry[0])
                heapq.heappush(distances, (d, iD))
        print()
        return distances[0]
            
    def addFace(self, faceDescriptor, imgCropped):
         if (len(self.faces.keys()) == 0):
            self.faces[self.nextId]= np.array([[faceDescriptor, imgCropped]])
         else:
             bestDistance, bestId = self.findBestClass(faceDescriptor)
             if (bestDistance > 0.6)

    def addImg(self, img, upsample=0, minimumScore = 0.22):
        facesDetected, scores, idx = lb.getFaceRects(img, 0)
        faceDescriptors = lb.getFaceDescriptors(img, facesDetected)
        for i in range(len(facesDetected)):
            #If the detection doesn't have a score big enough, ignore it.
            if (scores[i]< minimumScore):
                continue

            #If the part of the face is not visible, ignore it.
            if (lb.isFaceValid(img, facesDetected[i]) is False):
                continue
            x, y, w, h = facesDetected[i].left(),facesDetected[i].top(),facesDetected[i].width(), facesDetected[i].height()
            self.addFace(faceDescriptors[i], img[y:y+h, x:x+w])
    
   
            
        
        



            


            

