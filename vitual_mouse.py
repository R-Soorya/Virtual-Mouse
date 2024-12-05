import cv2
import numpy as np
import mediapipe as mp
import pyautogui
from pynput.mouse import Button, Controller

mouse = Controller()

screen_width, screen_height =  pyautogui.size()

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode = False,
    model_complexity = 1,
    min_detection_confidence = .7,
    min_tracking_confidence = .7,
    max_num_hands = 1
)


def get_angle(a,b,c):

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1]- b[1], a[0]- b[0])
    angle = np.abs(np.degrees(radians))
    return angle

def get_distance(landmark_list):

    if len(landmark_list) < 2:
        return
    (x1, y1), (x2, y2) = landmark_list[0], landmark_list[1]
    L = np.hypot(x2-x1, y2-y1)
    return np.interp(L,[0,1],[0,1000])

def move_mouse(index_finger_tip):

    if index_finger_tip is not None:
        x = int(index_finger_tip.x * screen_width)
        y = int(index_finger_tip.y * screen_height)
        pyautogui.moveTo(x,y)


def left_click(landmark_list, thumb_index_dist):

    return (get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
            get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) > 90 and
            thumb_index_dist > 50
            )

def right_click(landmark_list, thumb_index_dist):

    return (get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90 and
            get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
            thumb_index_dist > 50
            )

def double_click(landmark_list, thumb_index_dist):

    return (get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
            get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
            thumb_index_dist > 50
            )
            
def detect_gestures(frame, landmark_list, results):

    if len(landmark_list) >= 21:

        index_finger_tip = results.multi_hand_landmarks[0].landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
        
        thumb_index_dist = get_distance([landmark_list[4], landmark_list[5]])

        if thumb_index_dist < 50 and get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90:
            move_mouse(index_finger_tip)

        elif left_click(landmark_list, thumb_index_dist):
            mouse.press(Button.left)
            mouse.release(Button.left)
            cv2.putText(frame, "Left Click", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        elif right_click(landmark_list, thumb_index_dist):
            mouse.press(Button.right)
            mouse.release(Button.right)
            cv2.putText(frame, "Right Click", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        elif double_click(landmark_list, thumb_index_dist):
            pyautogui.doubleClick()
            cv2.putText(frame, "Double Clikc", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 2)
            
cap = cv2.VideoCapture(0)
draw = mp.solutions.drawing_utils

try:
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        frame = cv2.flip(frame, 1)
        frameGRB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(frameGRB)

        landmark_list = []

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)

            for lm in hand_landmarks.landmark:
                landmark_list.append((lm.x, lm.y))

        detect_gestures(frame, landmark_list, results)

        # print(landmark_list)

        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

finally:
    cap.release()
    cv2.destroyAllWindows()