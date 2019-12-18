import cv2
import numpy as np
 
image_points = np.array([
                            (359, 391),     # Nose tip
                            (399, 561),     # Chin
                            (337, 297),     # Left eye left corner
                            (513, 301),     # Right eye right corne
                            (345, 465),     # Left Mouth corner
                            (453, 469)      # Right mouth corner
                        ], dtype="double")

teste = [(10,10), (20,20)]
matrixx = np.array(teste, dtype="double")
print(matrixx)
 