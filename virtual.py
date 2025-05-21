import cv2
import mediapipe as mp 
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False, 
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
) #confidence score for hand detection is 0.7 even the tracking as well and one hand only
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
            
                print(landmarks_list) #prints all 21 x, y for each capture 
            
            cv2.imshow('Frame', frame) #show the frame captured
            if cv2.waitKey(1) & 0xFF == ord('q'): #wait for millisecond unless key is q then break
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
if __name__ == '__main__':
    main()
