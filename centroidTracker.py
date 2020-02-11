import numpy as np
import libTop as lt
import cv2
class CentroidTracker:
    def __init__(self):
        self.trackers=[] 
        # [tracker, center, class, disappearances]
        self.MAX_DISTANCE = 5
        self.MAX_DISAPPEARANCES = 10
        self.ACCEPTABLE_DISTANCE = 2


    def findBestTracker(self, center, takenTrackers):
        minimumDistance = -1
        bestTracker = -1
        for i, t in enumerate(self.trackers):
            if (i in takenTrackers):
                continue
            currDistance = lt.distance(center, t[1])
            if (bestTracker==-1):
                minimumDistance=currDistance
                bestTracker = i
            elif currDistance < minimumDistance:
                minimumDistance=currDistance
                bestTracker = i    
        return minimumDistance, bestTracker
            
            
    def processRects(self, img, rects):
        if len(rects)==0:
            pass
            return
            #Iterate all trackers with +1 disappearance
        takenTrackers = {}
        missingRects = {}
        for i, rect in enumerate(rects):
            x, y, w, h = rect.left(), rect.top(),rect.width(), rect.height()
            center = ((2*x+w)//22, (2*y+h)//2)
            minDistance, bestTrackerIndex = self.findBestTracker(center,takenTrackers)
            if (minDistance == -1):
                pass #Nesse caso. É pra criar um tracker.
            elif (minDistance <= self.ACCEPTABLE_DISTANCE):
                #Atualizar tracker
                takenTrackers[bestTrackerIndex] = 1
                newTracker = cv2.TrackerMIL_create()
                newTracker.init(img, (x,y,w,h))
                self.trackers[bestTrackerIndex][0] = newTracker
                self.trackers[bestTrackerIndex][1] = center
                self.trackers[bestTrackerIndex][2] = 0
            else:
                missingRects[i] = 1
                
                
        
        