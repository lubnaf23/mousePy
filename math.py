import numpy as np 

def get_angle(a, b, c):
    #direction of vectors
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0]) #subracting em to get angle b/w em
    angle = np.abs(np.degrees(radians))
    return angle
