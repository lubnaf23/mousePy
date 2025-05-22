import numpy as np 

def get_angle(a, b, c):
    #direction of vectors
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0]) #subracting em to get angle b/w em
    angle = np.abs(np.degrees(radians))
    return angle

def get_distance(landmark_list):
    if len(landmark_list) < 2: #2 lm to calc dist if not return nothing
        return
    
    (x1, y1), (x2, y2) = landmark_list[0], landmark_list[1] #x and y from first 2 lm
    L = np.hypot(x2 - x1, y2 - y1) #calculates dist 
    return np.interp(L, [0, 1], [1, 1000]) #scaling 