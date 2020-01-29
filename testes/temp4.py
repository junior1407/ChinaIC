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
    for face in face_locations:
        top, right, bottom, left = face
        cv2.rectangle(image, (left*4, top*4), (right*4, bottom*4), (0, 0, 255) , 2)
    cv2.imshow("Output", image)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    process_this_frame = not process_this_frame
cv2.destroyAllWindows()
cap.release()   