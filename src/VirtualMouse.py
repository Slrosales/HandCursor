"""
    In the UML there are classes like "Draw" and "User",
    however it is not in the code because the backend structure is being re-planned.

"""


from HandTrackingModule import HandDetector
import cv2
import numpy as np
import pyautogui
import time


class Dimensions:
    def __init__(self, height, width, other):
        self.heigth = height
        self.width = width
        self.other = other


class TimeV:
    def __init__(self, DELAY, prev_time, current_time):
        self.DELAY = DELAY
        self.prev_time = prev_time
        self.current_time = current_time
        self.fps_ = 0

    def calc_fps(self):
        self.current_time = time.time()
        self.fps_ = 1 / (self.current_time - self.prev_time)
        self.prev_time = self.current_time
        return self.fps_


class ScreenPoints:
    def __init__(self, x0, y0, x, y):
        self.x0 = x0
        self.y0 = y0
        self.x = x
        self.y = y


class Moves:
    def __init__(self, fingers):
        self.fingers = fingers

    def move_cursor(self):
        if hands and self.fingers == [0, 1, 0, 0, 0]:
            print("move")
            # Move mouse
            pyautogui.moveTo(xInd, yInd)
            # time.sleep(0.00001)

    def finger_moves(self):
        if cy <= screen.other:  # if hand is at the height of the face
            # left clic is pressed
            if fingers == [0, 0, 0, 0, 1]:
                print("Left click")
                pyautogui.click()

            # right clic is pressed
            if self.fingers == [0, 0, 0, 1, 1]:
                print("Right click")
                pyautogui.click(button='right')

            # key left pressed
            if self.fingers == [1, 0, 0, 0, 0]:
                print("Left")
                pyautogui.press('left')

            # key right pressed
            if self.fingers == [0, 0, 1, 1, 1]:
                print("Right")
                pyautogui.press('right')

            # key up pressed
            if self.fingers == [1, 1, 1, 0, 0]:
                print("Up")
                pyautogui.press('up')

                # key down pressed
            if self.fingers == [0, 1, 1, 0, 0]:
                print("Down")
                pyautogui.press('down')

            # Stop the commands
            if fingers == [1, 1, 1, 1, 1]:
                time.sleep(0.00001)


class Camera:
    def _init_(self):
        pass

    def turn_video_on(self):
        OPT_CLOSE = "Cerrar el programa"
        OPT_1 = "Camara 1"
        OPT_2 = "Camara 2"
        OPT_3 = "Otra"

        opt = pyautogui.confirm(
            "Bienvenidx, a continuacón escoge que cámara usarás", "Elegir cámara",
            [OPT_1, OPT_2, OPT_3, OPT_CLOSE]
        )

        if opt == OPT_1:
            cam = 0
        elif opt == OPT_2:
            cam = 1
        elif opt == OPT_3:
            cam = int(pyautogui.prompt("Ingresa el número de la cámara", "Elegir otra cámara"))
        elif opt == OPT_CLOSE:
            exit(1)

        return cv2.VideoCapture(cam)


screen = Dimensions(pyautogui.size()[1], pyautogui.size()[0], 250)

timev = TimeV(15, 0, 0)

points = ScreenPoints(0, 0, screen.width, screen.heigth)

counter = 0

# screen aspect ratio
aspect_ratio_scr = (points.x - points.x0) / (points.y - points.y0)
XY_INI = 100

# Booleans Var
button_pressed = False
pyautogui.FAILSAFE = False  # Allows move the cursor to the bottom of the scr.

# Video on
camera = Camera()
cap = camera.turn_video_on()  # 0: main camera; 1: external camera

# Hand Detector
detector = HandDetector(maxHands=1)

while True:
    success, img = cap.read()
    if not success:
        pyautogui.alert("Esa camara no esta disponible", "ERROR")
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
        moves = Moves(fingers)
        moves.move_cursor()
        moves.finger_moves()

    # Button Pressed iterations
    if button_pressed:
        counter += 1
        if counter > 15:
            counter = 0
            button_pressed = False

    # Getting the fps
    fps = timev.calc_fps()

    cv2.putText(output, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)

    cv2.imshow("Virtual Mouse", output)

    key = cv2.waitKey(1)
    if key == 27:  # Press ESC to close te program
        break
