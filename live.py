import cv2
import libTop as lb
import matplotlib.pyplot as plt
SKIP = 5

nextId = 0
db = []
videoCapture = cv2.VideoCapture(0)
if videoCapture.isOpened() == False:
    print("Erro na stream")
count = 0
while(videoCapture.isOpened()):
    _status, frame = videoCapture.read()
    if (count < SKIP):
        count+=1
    else:
        count=0
        rects = lb.getFaceRects(img)

        cv2.imshow("Output", frame)
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break

    
videoCapture.release()
cv2.destroyAllWindows()
