"""
    This is a draft of the code without classes because it is adapted to the PC in which we are first implementing.
    So, it has specific values in its varibals
"""

from HandTrackingModule import HandDetector
import cv2
import numpy as np
import pyautogui
import time

# Screen Var
width_scr, height_scr = pyautogui.size()  # Screen size
DIV_LINE = 250 # y position of the line

# Time Var
DELAY = 15  # Limit on consecutive presses of a single button based of fps
counter = 0
prev_time = 0
current_time = 0

# Screen Points
SCREEN_X_INI = 0
SCREEN_Y_INI = 0
SCREEN_X_FIN = 1920
SCREEN_Y_FIN = 1080

# screen aspect ratio
aspect_ratio_scr = (SCREEN_X_FIN - SCREEN_X_INI) / (SCREEN_Y_FIN - SCREEN_Y_INI)
XY_INI = 100

# Booleans Var
button_pressed = False
pyautogui.FAILSAFE = False  # Allows move the cursor to the bottom of the scr.

# Video on
cap = cv2.VideoCapture(1)  # 0: main camera; 1: external camera

# Hand Detector
detector = HandDetector(maxHands=1)

while True:
    success, img = cap.read()
    if not success:
        break

    # Image corrections
    cam_height, cam_width, channel = img.shape  # Cam dimensions
    img = cv2.flip(img, 1)  # 1: x flip ; 0: y flip
    cv2.line(img, (0, DIV_LINE), (cam_width, DIV_LINE), (0, 255, 0), 4)  # Line to divide the img
    hands, img = detector.findHands(img, flipType=False)

    # Auxiliary image area
    area_width = cam_width - XY_INI * 2
    area_height = int(area_width / aspect_ratio_scr)

    image_rect = np.zeros(img.shape, np.uint8)  # new cap with black background
    image_rect = cv2.rectangle(image_rect, (XY_INI, XY_INI), (XY_INI + area_width, XY_INI + area_height),
                               (255, 0, 0), -1)
    output = cv2.addWeighted(img, 1, image_rect, 0.7, 0)

    if hands and button_pressed is False:
        # 1. Find hand Landmarks
        hand = hands[0]
        cx, cy = hand["center"]  # center point of the hand
        lmList = hand["lmList"]  # List of 21 Landmark points

        xInd = int(np.interp(lmList[8][0], (XY_INI, XY_INI + area_width), (SCREEN_X_INI, SCREEN_X_FIN)))
        yInd = int(np.interp(lmList[8][1], (XY_INI, XY_INI + area_height), (SCREEN_Y_INI, SCREEN_Y_FIN)))

        fingers = detector.fingersUp(hand)  # List of which fingers are up

        # Move cursor
        if hands and fingers == [0, 1, 0, 0, 0]:
            print("move")
            # Move mouse
            pyautogui.moveTo(xInd, yInd)
            # time.sleep(0.00001)

        if cy <= DIV_LINE: # if hand is at the height of the face
            # left clic is pressed
            if fingers == [0, 0, 0, 0, 1]:
                print("Left click")
                pyautogui.click()
                button_pressed = True

            # left clic is pressed
            if fingers == [0, 0, 0, 1, 1]:
                print("Right click")
                pyautogui.click(button='right')
                button_pressed = True

            # key left pressed
            if fingers == [1, 0, 0, 0, 0]:
                print("Left")
                pyautogui.press('left')
                button_pressed = True

            # key right pressed
            if fingers == [1, 1, 0, 0, 0]:
                print("Right")
                pyautogui.press('right')
                button_pressed = True

            # key up pressed
            if fingers == [1, 1, 1, 0, 0]:
                print("Up")
                pyautogui.press('up')
                button_pressed = True

            # key down pressed
            if fingers == [0, 1, 1, 0, 0]:
                print("Down")
                pyautogui.press('down')
                button_pressed = True

            # ctrl + z
            if fingers == [0, 0, 1, 1, 1]:
                print("ctrl + z")
                pyautogui.hotkey('ctrl', 'z')
                button_pressed = True

    # Button Pressed iterations
    if button_pressed:
        counter += 1
        if counter > DELAY:
            counter = 0
            button_pressed = False

    # Getting the fps
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time

    cv2.putText(output, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)

    cv2.imshow("Virtual Mouse", output)

    key = cv2.waitKey(1)
    if key == 27:  # Press ESC to close te program
        break
cv2.destroyAllWindows()
