"""
    This is a draft of the code without classes because it is adapted to the PC in which we are first implementing.
    So, it has specific values in its varibals
"""


from HandTrackingModule import HandDetector
import cv2
import numpy as np
import pyautogui
import time

# Variables
wCam, hCam = 640, 480  # 1280, 720
divLine = 240  # y position of the line
buttonPressed = False
bCounter = 0
bDelay = 15  # Limit on consecutive presses of a single button based of fps
pTime = 0  # Previews time
cTime = 0  # Current time
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    success, img = cap.read()

    # Image corrections
    img = cv2.flip(img, 1)  # 1: x flip ; 0: y flip
    cv2.line(img, (0, divLine), (wCam, divLine), (0, 255, 0), 4)
    hands, img = detector.findHands(img, flipType=False)

    if hands and buttonPressed is False:
        # 1. Find hand Landmarks
        hand = hands[0]
        cx, cy = hand["center"]  # center point of the hand
        lmList = hand["lmList"]  # List of 21 Landmark points

        fingers = detector.fingersUp(hand)  # List of which fingers are up
        # print(fingers)
        c = 0
        if cy <= divLine: # if hand is at the height of the face
            # left clic is pressed
            if fingers == [0, 0, 0, 0, 1]:
                print("Left click")
                pyautogui.click()
                buttonPressed = True

            # left clic is pressed
            if fingers == [0, 0, 0, 1, 1]:
                print("Right click")
                pyautogui.click(button='right')
                buttonPressed = True

            # key left pressed
            if fingers == [1, 0, 0, 0, 0]:
                print("Left")
                pyautogui.press('left')
                buttonPressed = True

            # key right pressed
            if fingers == [1, 1, 0, 0, 0]:
                print("Right")
                pyautogui.press('right')
                buttonPressed = True

            # key up pressed
            if fingers == [1, 1, 1, 0, 0]:
                print("Up")
                pyautogui.press('up')
                buttonPressed = True

            # key down pressed
            if fingers == [0, 1, 1, 0, 0]:
                print("Down")
                pyautogui.press('down')
                buttonPressed = True

            # ctrl + z
            if fingers == [0, 0, 1, 1, 1]:
                print("ctrl + z")
                pyautogui.hotkey('ctrl', 'z')
                buttonPressed = True

    # Button Pressed iterations
    if buttonPressed:
        bCounter += 1
        if bCounter > bDelay:
            bCounter = 0
            buttonPressed = False


    # Getting the fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)

    cv2.imshow("Virtual Mouse", img)
    key = cv2.waitKey(1)
    if key == 27:  # Press ESC to close te program
        break
