from imutils import face_utils
import dlib
import cv2
import numpy as np
import math

def get3DFaceModel():
    model_points = np.array([
                            (0.0, 0.0, 0.0),             # Nose tip
                            (0.0, -330.0, -65.0),        # Chin
                            (-225.0, 170.0, -135.0),     # Left eye left corner
                            (225.0, 170.0, -135.0),      # Right eye right corne
                            (-150.0, -150.0, -125.0),    # Left Mouth corner
                            (150.0, -150.0, -125.0)      # Right mouth corner
                         
                        ])
    return model_points

def angleEstimator(img, points, width, height):
    size = img.shape
    indexes = [30, 8, 36, 45, 48, 54]
    image_points = [points[i] for i in indexes]
    image_points_np= np.array(image_points, dtype="double")
    model_points = get3DFaceModel()
    center = (size[1]/2, size[0]/2)
    focal_length = center[0] / np.tan(60/2 * np.pi / 180)
    camera_matrix = np.array(
                         [[focal_length, 0, center[0]],
                         [0, focal_length, center[1]],
                         [0, 0, 1]], dtype = "double"
                         )

    
    dist_coeffs = np.zeros((4,1)) # Assuming no lens distortion
    
    (success, rotation_vector, translation_vector) = cv2.solvePnP(
        model_points, image_points_np, camera_matrix,
         dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)
    #(success, rotation_vector, translation_vector) = cv2.solvePnP(model_points,
    # image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)

    
    axis = np.float32([[500,0,0], 
                          [0,500,0], 
                          [0,0,500]])
                          
    imgpts, jac = cv2.projectPoints(axis, rotation_vector, translation_vector, camera_matrix, dist_coeffs)
    modelpts, jac2 = cv2.projectPoints(model_points, rotation_vector, translation_vector, camera_matrix, dist_coeffs)
    rvec_matrix = cv2.Rodrigues(rotation_vector)[0]

    proj_matrix = np.hstack((rvec_matrix, translation_vector))
    eulerAngles = cv2.decomposeProjectionMatrix(proj_matrix)[6] 

    
    pitch, yaw, roll = [math.radians(_) for _ in eulerAngles]

    pitch = math.degrees(math.asin(math.sin(pitch)))
    roll = -math.degrees(math.asin(math.sin(roll)))
    yaw = math.degrees(math.asin(math.sin(yaw)))
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(img, "Pitch: "+ '{0:.2f}'.format(pitch), (420, 25), font, 1.0, (0, 255, 0), 1)
    cv2.putText(img, "Yawn: "+ '{0:.2f}'.format(yaw), (420, 50), font, 1.0, (0, 255, 0), 1)
    cv2.putText(img, "Roll:  "+ '{0:.2f}'.format(roll), (420, 75), font, 1.0, (0, 255, 0), 1)   # cv2.putText(img, "Rol" + str(euler[2]), (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    
    print(pitch,roll, yaw)