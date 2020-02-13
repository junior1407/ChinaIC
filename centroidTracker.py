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
        self.MAX_DISAPPEARANCES = 1
        self.ACCEPTABLE_DISTANCE = 300
        self.MAX_IDENTIFICATIONS = 20

    def findBestTracker(self, center, rectIndex):
        lista = []
        for i, t in enumerate(self.trackers):
            currDistance = lt.distance(center, getCenter(t[1]))
            if (currDistance <= self.ACCEPTABLE_DISTANCE):
                lista.append([rectIndex, i, currDistance])
        return lista

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
        self.trackers = notDeleted
        allDistances = []
        takenTrackers = {}
        takenRect = {}
        if len(rects)>=2:
            print()
        for i, rect in enumerate(rects):
            x, y, w, h = rect.left(), rect.top(), rect.width(), rect.height()
            tl = (x, y)
            br = (x + w, y + h)
            center = getCenter((tl, br))
            temp = self.findBestTracker(center, i)
            allDistances.extend(temp)
        if (len(allDistances) == 0):
            for i, rect in enumerate(rects):
                x, y, w, h = rect.left(), rect.top(), rect.width(), rect.height()
                tl = (x, y)
                br = (x + w, y + h)
                center = getCenter((tl, br))
                t = cv2.TrackerKCF_create()
                t.init(img, (x, y, w, h))
                classe = self.bd.identifyFace(img, rect)
                temp = [t, (tl, br), classe, 0,1]
                self.trackers.append(temp)
                takenTrackers[len(self.trackers) - 1] = 1
                takenRect[i] = 1
        else:
            while len(allDistances) != 0:
                if (len(allDistances)>=2):
                    print()
                allDistances.sort(key=lambda x: x[2])
                indexRect, indexTracker, distance = allDistances.pop(0)

                x, y, w, h = rects[indexRect].left(), rects[indexRect].top(), rects[indexRect].width(), rects[
                    indexRect].height()
                tl = (x, y)
                br = (x + w, y + h)
                takenTrackers[indexTracker] = 1
                takenRect[indexRect] = 1
                newTracker = cv2.TrackerKCF_create()
                newTracker.init(img, (x, y, w, h))
                self.trackers[indexTracker][0] = newTracker
                self.trackers[indexTracker][1] = (tl, br)
                self.trackers[indexTracker][3] = 0
                if self.trackers[indexTracker][4] < self.MAX_IDENTIFICATIONS:
                    self.bd.identifyFace(img, rects[indexRect])
                    self.trackers[indexTracker][4]+=1

                allDistances = [elem for elem in allDistances if (not ((elem[0] == indexRect) or (elem[1] == indexTracker)))]
            pass
        for i ,rect in enumerate(rects):
            if i not in takenRect:
                x, y, w, h = rects[i].left(), rects[i].top(), rects[i].width(), rects[i].height()
                tl = (x, y)
                br = (x + w, y + h)
                takenRect[i] = 1
                newTracker = cv2.TrackerKCF_create()
                classe = self.bd.identifyFace(img, rect)
                newTracker.init(img, (x, y, w, h))
                temp = [newTracker, (tl,br), classe, 0, 1]
                self.trackers.append(temp)
                takenTrackers[len(self.trackers) - 1] = 1
        for i, t in enumerate(self.trackers):
            if i not in takenTrackers:
                self.trackers[i][3] += 1
        return self.trackers
