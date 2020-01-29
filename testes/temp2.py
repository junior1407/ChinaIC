# import the necessary packages
from imutils import face_utils
import dlib
import cv2
import face_recognition
# Vamos inicializar um detector de faces (HOG) para então
# fazer a predição dos pontos da nossa face.
#p é o diretorio do nosso modelo já treinado, no caso, ele está no mesmo diretorio
# que esse script
p = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)

cap = cv2.VideoCapture(0)
process_this_frame = True
while True:
    # Obtendo nossa imagem através da webCam e transformando-a preto e branco.
    _, image = cap.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (0, 0), fx=0.25, fy=0.25)
    face_locations = face_recognition.face_locations(gray)
    #print(face_locations)
    for face in face_locations:
        top, right, bottom, left = face
        cv2.rectangle(image, (left*4, top*4), (right*4, bottom*4), (0, 0, 255) , 2)

    # Detectando as faces em preto e branco.
    #rects = detector(gray, 0)

    # para cada face encontrada, encontre os pontos de interesse.
    #for (i, rect) in enumerate(rects):
        # faça a predição e então transforme isso em um array do numpy.
        #shape = predictor(gray, rect)
        #shape = face_utils.shape_to_np(shape)
    
        # desenhe na imagem cada cordenada(x,y) que foi encontrado.
        #for (x, y) in shape:
            #cv2.circle(image, (x, y), 2, (0, 255, 0), -1)
    
    # Mostre a imagem com os pontos de interesse.
    cv2.imshow("Output", image)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    process_this_frame = not process_this_frame
cv2.destroyAllWindows()
cap.release()   