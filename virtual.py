import cv2
import mediapipe as mp 
import mathfunc
import pyautogui

prev_y = None

screen_width, screen_height = pyautogui.size()
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False, 
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
) #confidence score for hand detection is 0.7 even the tracking as well and one hand only

def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]
        return hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
    return None

def scroll_with_finger(index_finger_tip):
    global prev_y

    if index_finger_tip is None:
        return

    current_y = index_finger_tip.y  # Y is in normalized coordinates (0 to 1)

    if prev_y is not None:
        delta = current_y - prev_y  # positive = moved down, negative = moved up

        # You can tweak this threshold
        if abs(delta) > 0.01:
            scroll_amount = int(delta * 1000)  # scale for pyautogui
            pyautogui.scroll(-scroll_amount)  # negative = scroll down, positive = scroll up

    prev_y = current_y

def move_mouse(index_finger_tip):
    if index_finger_tip is not None:
        x = int(index_finger_tip.x * screen_width)
        y = int(index_finger_tip.y * screen_height)
        pyautogui.moveTo(x,y)

def is_right_click(landmarks_list, thumb_index_dist):
    return (mathfunc.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) < 50 and 
            mathfunc.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12] > 90 and thumb_index_dist > 50)) #checks if index is bent, middle is straight and thumb is out

def is_left_click(landmarks_list, thumb_index_dist):
    return (mathfunc.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) > 90 and 
            mathfunc.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12] < 50 and thumb_index_dist > 50)) #checks if index is staright, middle is bent and thumb is out
        

    

def detect_gestures(frame, landmarks_list, processed):
    if len(landmarks_list) >= 21:
        
        #first need point to track mouse 
        index_finger_tip = find_finger_tip(processed)
        #print(index_finger_tip)
        
        thumb_index_dist = mathfunc.get_distance([landmarks_list[4], landmarks_list[5]]) #thumb (4) and index (5)
        
        #angle at 6 to check if index is upright
        
        if thumb_index_dist < 50 and mathfunc.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) > 90:
            #now move mouse
            move_mouse(index_finger_tip)
            
        elif thumb_index_dist > 50 and mathfunc.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) > 90 and mathfunc.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) > 90:
            scroll_with_finger(index_finger_tip)
            
        #LEFT CLICK HERE

            
    
def main():
    cap = cv2.VideoCapture(1)
    draw = mp.solutions.drawing_utils #draw landmarks of the hand
    try:
        while cap.isOpened():
            ret, frame = cap.read() #returning a boolean value if it was able to read
            
            if not ret: #if false
                break 
            frame = cv2.flip(frame, 1) #mirroring
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #opencv uses bgr
            
            processed = hands.process(frameRGB) #set up from above
            
            landmarks_list = [] #will contain all landmarks
            
            if processed.multi_hand_landmarks:
                hand_landmarks = processed.multi_hand_landmarks[0] #out of many taking first hand
                draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS) #draw all connects using original frame NOT RGB
                
                for lm in hand_landmarks.landmark:
                    landmarks_list.append((lm.x, lm.y))
                #print(landmarks_list) #prints all 21 x, y for each capture 
                
            detect_gestures(frame, landmarks_list, processed)
            
            cv2.imshow('Frame', frame) #show the frame captured
            if cv2.waitKey(1) & 0xFF == ord('q'): #wait for millisecond unless key is q then break
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
if __name__ == '__main__':
    main()
