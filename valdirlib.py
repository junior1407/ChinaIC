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

def getCameraMatrix(width, height):
    matrix = np.array([
        [width, 0, width/2],
        [0,width, height/2],
        [0,0,1]
    ], dtype="double")
    return matrix
def getCameraMatrixNinja(focal_length, width, height):
    matrix = np.array([
        [focal_length, 0, width/2],
        [0,focal_length, height/2],
        [0,0,1]
    ], dtype="double")
    return matrix



def getAxes(rotation_vector):
    rot,_ = cv2.Rodrigues(rotation_vector)
    matrix = np.array([
        [rot[0][0], rot[0][1],rot[0][2],0],
        [rot[1][0], rot[1][1],rot[1][2],0],
        [rot[2][0], rot[2][1],rot[2][2],0]
        ], dtype="double")
    temp = cv2.decomposeProjectionMatrix(matrix)
    return temp[6]
    

def getEulerMatrix(rotation_vector):
    r,_ = cv2.Rodrigues(rotation_vector)
    yaw = 0
    pitch = 1
    roll = 2
    euler1 = [0,0,0] #yaw, pitch, roll 
    euler2 = [0,0,0]
    if (abs(r[2][0])>=1):
        euler1[yaw] = 0
        euler2[yaw] = 0
        if (r[2][0]<0):  #gimbal locked down
            delta = math.atan2(r[0][1], r[0][2])
            euler1[pitch] = math.pi / 2
            euler2[pitch] = math.PI / 2
            euler1[roll] = delta
            euler2[roll] = delta
        else:
            delta = math.atan2(-r[0][1], -r[0][2])
            euler1[pitch] = math.pi / 2
            euler2[pitch] = math.PI / 2
            euler1[roll] = delta
            euler2[roll] = delta
    else:
        euler1[pitch] = -math.asin(r[2][0]);
        euler2[pitch] = math.pi - euler1[pitch];

        euler1[roll] = math.atan2(r[2][1] / math.cos(euler1[pitch]), r[2][2] / math.cos(euler1[pitch]));
        euler2[roll] = math.atan2(r[2][1] / math.cos(euler2[pitch]), r[2][2] / math.cos(euler2[pitch]));

        euler1[yaw] = math.atan2(r[1][0] / math.cos(euler1[pitch]), r[0][0] / math.cos(euler1[pitch]));
        euler2[yaw] = math.atan2(r[1][0] / math.cos(euler2[pitch]), r[0][0] / math.cos(euler2[pitch]));
    return euler1


def angleEstimator2(img, points, width, height):

    indexes = [30, 8, 36, 45, 48, 54]
    image_points = [points[i] for i in indexes]
    image_points_np= np.array(image_points, dtype="double")
    model_points = get3DFaceModel()
    camera_matrix = getCameraMatrix(width, height)
    dist_coeffs = np.zeros((4,1)) # Assuming no lens distortion
    (success, rotation_vector, translation_vector) = cv2.solvePnP(
        model_points, image_points_np, camera_matrix,
         dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)
    
    euler = getEulerMatrix(rotation_vector)
    yaw = (180 * euler[0])/math.pi
    pitch = (180 * euler[1])/math.pi
    roll = (180 * euler[2])/math.pi
    pitch = math.copysign(1, pitch) * 180 - pitch;
    font = cv2.FONT_HERSHEY_DUPLEX

    cv2.putText(img, "Pitch: "+ '{0:.2f}'.format(pitch), (420, 25), font, 1.0, (255, 255, 255), 1)
    cv2.putText(img, "Yawn: "+ '{0:.2f}'.format(yaw), (420, 50), font, 1.0, (255, 255, 255), 1)
    cv2.putText(img, "Roll:  "+ '{0:.2f}'.format(roll), (420, 75), font, 1.0, (255, 255, 255), 1)   # cv2.putText(img, "Rol" + str(euler[2]), (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)
    p1 = ( int(image_points_np[0][0]), int(image_points_np[0][1]))
    p2 = ( int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))
    #cv2.line(img, p1, p2, (255,0,0), 2)


def angleEstimator(img, points, width, height):

    indexes = [30, 8, 36, 45, 48, 54]
    image_points = [points[i] for i in indexes]
    image_points_np= np.array(image_points, dtype="double")
    model_points = get3DFaceModel()
    camera_matrix = getCameraMatrix(width, height)
    dist_coeffs = np.zeros((4,1)) # Assuming no lens distortion
    (success, rotation_vector, translation_vector) = cv2.solvePnP(
        model_points, image_points_np, camera_matrix,
         dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)
    
    euler = getAxes(rotation_vector)
    font = cv2.FONT_HERSHEY_DUPLEX

    euler[0][0] = math.copysign(1, euler[0][0]) * 180 - euler[0][0];
    cv2.putText(img, "Pitch: "+ '{0:.2f}'.format(euler[0][0]), (420, 25), font, 1.0, (255, 255, 255), 1)
    cv2.putText(img, "Yawn: "+ '{0:.2f}'.format(euler[1][0]), (420, 50), font, 1.0, (255, 255, 255), 1)
    cv2.putText(img, "Roll:  "+ '{0:.2f}'.format(euler[2][0]), (420, 75), font, 1.0, (255, 255, 255), 1)   # cv2.putText(img, "Rol" + str(euler[2]), (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)
    p1 = ( int(image_points_np[0][0]), int(image_points_np[0][1]))
    p2 = ( int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))
    cv2.line(img, p1, p2, (255,0,0), 2)


