import numpy as np
import libTop as lt
import cv2

def getCenter(tlbr):
    tl, br = tlbr
    return (tl[0] + br[0]) / 2, (tl[0] + br[0]) / 2


class CentroidTracker:
    def __init__(self, bd):
        self.trackers = []
        self.bd = bd
        # [tracker, (tl,br), class, disappearances]
        self.MAX_DISTANCE = 20
        self.MAX_DISAPPEARANCES = 20
        self.ACCEPTABLE_DISTANCE = 80

    def findBestTracker(self, center, takenTrackers):
        minimumDistance = -1
        bestTracker = -1
        for i, t in enumerate(self.trackers):
            if i in takenTrackers:
                continue
            currDistance = lt.distance(center, getCenter(t[1]))
            if bestTracker == -1:
                minimumDistance = currDistance
                bestTracker = i
            elif currDistance < minimumDistance:
                minimumDistance = currDistance
                bestTracker = i
        return minimumDistance, bestTracker

    def processRects(self, img, rects):
        notDeleted = []
        toBeDeleted = []
        for i, t in enumerate(self.trackers):
            if not (t[3] >= self.MAX_DISAPPEARANCES):
                ok, bbox = self.trackers[i][0].update(img)
                tl = (int(bbox[0]), int(bbox[1]))
                br = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                self.trackers[i][1] = (tl, br)
                notDeleted.append(t)
            else:
                toBeDeleted.append(t)
        self.trackers = notDeleted
        takenTrackers = {}
        for i, rect in enumerate(rects):
            x, y, w, h = rect.left(), rect.top(), rect.width(), rect.height()
            tl = (x, y)
            br = (x + w, y + h)
            center = getCenter((tl, br))
            minDistance, bestTrackerIndex = self.findBestTracker(center, takenTrackers)
            if (minDistance == -1):
                t = cv2.TrackerKCF_create()
                t.init(img, (x,y,w,h))
                classe = self.bd.identifyFace(img, rect)
                temp = [t, (tl,br), classe , 0]
                self.trackers.append(temp)
                takenTrackers[len(self.trackers)- 1] = 1
            elif minDistance <= self.ACCEPTABLE_DISTANCE:
                takenTrackers[bestTrackerIndex] = 1
                newTracker = cv2.TrackerKCF_create()
                newTracker.init(img, (x, y, w, h))
                self.trackers[bestTrackerIndex][0] = newTracker
                self.trackers[bestTrackerIndex][1] = (tl,br)
                self.trackers[bestTrackerIndex][3] = 0
            else:
                t = cv2.TrackerKCF_create()
                t.clear()
                t.init(img, (x, y, w, h))
                classe = self.bd.identifyFace(img, rect)
                temp = [t, (tl, br), classe, 0]
                self.trackers.append(temp)
                takenTrackers[len(self.trackers) - 1] = 1
        for i, t in enumerate(self.trackers):
            if i not in takenTrackers:
                self.trackers[i][3]+=1
        return self.trackers
