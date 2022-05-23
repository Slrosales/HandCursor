from HandTrackingModule import HandDetector
import cv2
import numpy as np
import pyautogui
import time
from win32api import GetSystemMetrics

class Dimensions:
    def _init_(self, height, width, other):
        self.heigth = height
        self.width = width
        self.other = other


class TimeV:
    def _init_(self, DELAY, counter, prev, current):
        self.DELAY = DELAY
        self.counter = counter
        self.prev = prev
        self.current = current


class ScreenPoints:
    def _init_(self, x0, y0, x, y):
        self.x0 = x0
        self.y0 = y0
        self.x = x
        self.y = y


class Cam:
    def _init_(self):
        pass

    def turn_video_on(camera):
        return cv2.VideoCapture(camera)


screen = Dimensions(pyautogui.size()[1], pyautogui.size()[0], 250)

timev = TimeV(15, 0, 0, 0)

points = ScreenPoints(0, 0, GetSystemMetrics(0), GetSystemMetrics(1))

# screen aspect ratio
aspect_ratio_scr = (points.x - points.x0) / (points.y - points.y0)
XY_INI = 100

# Booleans Var
button_pressed = False
pyautogui.FAILSAFE = False  # Allows move the cursor to the bottom of the scr.

# Video on
cap = Cam.turn_video_on(0)  # 0: main camera; 1: external camera      PREGUNTAR CUÁL CÁMARA

# Hand Detector
detector = HandDetector(maxHands=1)

while True:
    success, img = cap.read()
    if not success:
        break

    # Image corrections
    cam_dim = Dimensions(img.shape[0], img.shape[1], img.shape[2]) # Cam dimensions
    img = cv2.flip(img, 1)  # 1: x flip ; 0: y flip
    cv2.line(img, (0, screen.other), (cam_dim.width, screen.other), (0, 255, 0), 4)  # Line to divide the img
    hands, img = detector.findHands(img, flipType=False)


    # Auxiliary image area
    area = Dimensions(1, cam_dim.width - XY_INI * 2, 0)
    area = Dimensions(int(area.width / aspect_ratio_scr), area.width, 0)

    image_rect = np.zeros(img.shape, np.uint8)  # new cap with black background
    image_rect = cv2.rectangle(image_rect, (XY_INI, XY_INI), (XY_INI + area.width, XY_INI + area.heigth),
                               (255, 0, 0), -1)
    output = cv2.addWeighted(img, 1, image_rect, 0.7, 0)

    if hands and button_pressed is False:
        # 1. Find hand Landmarks
        hand = hands[0]
        cx, cy = hand["center"]  # center point of the hand
        lmList = hand["lmList"]  # List of 21 Landmark points

        xInd = int(np.interp(lmList[8][0], (XY_INI, XY_INI + area.width), (points.x0, points.x)))
        yInd = int(np.interp(lmList[8][1], (XY_INI, XY_INI + area.heigth), (points.y0, points.y)))

        fingers = detector.fingersUp(hand)  # List of which fingers are up

        # Move cursor
        if hands and fingers == [0, 1, 0, 0, 0]:
            print("move")
            # Move mouse
            pyautogui.moveTo(xInd, yInd)
            # time.sleep(0.00001)

        if cy <= screen.other: # if hand is at the height of the face
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
        timev.counter += 1
        if timev.counter > timev.DELAY:
            timev.counter = 0
            button_pressed = False

    # Getting the fps
    timev.current = time.time()
    fps = 1 / (timev.current - timev.prev)
    timev.prev = timev.current

    cv2.putText(output, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)

    cv2.imshow("Virtual Mouse", output)

    key = cv2.waitKey(1)
    if key == 27:  # Press ESC to close te program
        break
cv2.destroyAllWindows()
