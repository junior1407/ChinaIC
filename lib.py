import numpy as np


predictorPath = "dnn/shape_predictor_68_face_landmarks.dat"
def isFaceValid(tl, br, resolution):
    if((tl[0]>=0 and tl[0]<=resolution[0]) and 
        (tl[1]>=0 and tl[1]<=resolution[1]) and 
        (br[0]>=0 and tl[0]<=resolution[0]) and
        (br[1]>=0 and tl[0]<=resolution[1])):
        return True
    

def normalizeShape(old_shape, tl, br):


    min_x = tl[0] #35 
    max_x = br[0] # 113
    min_y = tl[1] #64
    max_y = br[1] # 148

    RANGE_X = max_x-min_x
    coeff = RANGE_X / 50
    RANGE_Y = (max_y-min_y)/coeff
    RANGE_X = RANGE_X / coeff

    
    a_x = (RANGE_X)/(max_x - min_x)
    b_x = - (a_x * min_x)
    a_y = (RANGE_Y)/(max_y - min_y)
    b_y = - (a_y * min_y)
    old_shape = old_shape.astype('float32')
    for i in range(len(old_shape)):
        print(old_shape[i], " -> ", end='')
        old_shape[i][0] = old_shape[i][0] * a_x + b_x
        old_shape[i][1] = old_shape[i][1]  * a_y + b_y
        print(old_shape[i])
    return old_shape
