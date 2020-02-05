import libTop as lb
class Database:
    def __init__(self):
         self.nextId = 0
         self.faces = {}
    def addImg(img, upsample=0, minimumScore = 0.22):
        facesDetected, scores, idx = lb.getFaceRects(img, 0)
        faceDescriptors = lb.getFaceDescriptors(img, facesDetected)
        for i in range(len(facesDetected)):
            #If the detection doesn't have a score big enough, ignore it.
            if (score[i]< minimumScore):
                continue

            #If the part of the face is not visible, ignore it.
            if (lb.isFaceValid(img, facesDetected[i]) is False):
                continue
            x, y, w, h = facesDetected.left(),facesDetected.top(),facesDetected.width(), facesDetected.height()
            addFace(faceDescriptors[i], img[y:y+h, x:x+w])
    
    def addFace(faceDescriptor, imgCropped):
        if (len(face))
        
        



            


            

