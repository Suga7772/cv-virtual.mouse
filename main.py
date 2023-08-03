import cv2 # opencv library
# detecting hand
import mediapipe as mp
# moving mouse via finger landmark
import pyautogui

# open camera
cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
# get overall screen width and size
screen_width, screen_height = pyautogui.size()

index_y = 0  # distance for clicking mechanism between index finger and thumb

while True:
    _, frame = cap.read()
    # flipping frame as image is mirror from going right to left
    frame = cv2.flip(frame, 1)
    # extract height, width from output screen
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    # display landmarks on your hand
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            # get id of every landmark , so conversion to enumeration
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                # tip of index finger
                # coordinates, explicitly typecast to convert to integers)
                x = int(landmark.x*frame_width)
                y = int(landmark.y*frame_height)

                # 8 landmark is tip of index finger , outlining it as yellow
                if id == 8:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    # mapping the frame. divide within the size of frame and multiply with the index x and y axis
                    index_x = screen_width/frame_width*x
                    index_y = screen_height/frame_height*y

                    pyautogui.moveTo(index_x, index_y) # is bound within frameweight, does not go outside frame

                # clicking mechanism for thumb circle on its tip
                if id == 4:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    # mapping the frame. divide within the size of frame and multiply with the index x and y-axis
                    thumb_x = screen_width/frame_width*x
                    thumb_y = screen_height/frame_height*y

                    print("outside:", abs(index_y - thumb_y))
                    # absolute difference
                    if abs(index_y - thumb_y) < 25:
                        pyautogui.click()
                        pyautogui.sleep(1)
                        print("click")

    cv2.imshow('virtual mouse', frame)
    cv2.waitKey(1) # delay
