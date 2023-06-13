import cv2
import numpy as np
import pyautogui
from VirtualMouse import scr_settings as scs
from VirtualMouse.HandTrackingModule import HandDetector
from VirtualMouse.HandTrackingModule import Moves

# Video settings
screen = scs.Dimensions(pyautogui.size()[1], pyautogui.size()[0])
camera = scs.Start()
cap = camera.turn_video_on()

screen_points = scs.ScreenPoints(x=screen.width, y=screen.height)

# Command and action settings
options_window = scs.WindowOpt()
options_window.window.mainloop()
acc_opt = options_window.selected_options
moves_dic = options_window.configuration

# fps and delay settings
time_v = scs.TimeV()
fps = time_v.calc_fps()
delay = camera.define_fps(fps)

# Screen aspect ratio
aspect_ratio_scr = (screen_points.x - screen_points.x0) / (screen_points.y - screen_points.y0)
XY_INI = 100
DELAY_COUNT = 0
DIV_LINE = 250

# Booleans var
BUTTON_PRESSED = False
pyautogui.FAILSAFE = False  # Allows move the cursor to the bottom of the scr.

# Hand detector
detector = HandDetector(maxHands=1)
moves = Moves()

while True:
    success, img = cap.read()
    if not success:
        pyautogui.alert("Esa camara no esta disponible", "ERROR")
        break

    if delay != 0:
        mode = 250
    else:
        mode = img.shape[1]

    # Image corrections
    cam_dim = scs.Dimensions(img.shape[0], img.shape[1])  # Cam dimensions
    img = cv2.flip(img, 1)  # 1: x flip ; 0: y flip
    cv2.line(img, (0, DIV_LINE), (cam_dim.width, DIV_LINE), (0, 255, 0), 4)  # Line to divide the img
    hands, img = detector.find_hands(img, flipType=False)

    # Auxiliary image area
    area = scs.Dimensions(1, cam_dim.width - XY_INI * 2)
    area = scs.Dimensions(int(area.width / aspect_ratio_scr), area.width)

    image_rect = np.zeros(img.shape, np.uint8)  # new cap with black background
    image_rect = cv2.rectangle(image_rect, (XY_INI, XY_INI), (XY_INI + area.width, XY_INI + area.height),
                               (255, 0, 0), -1)
    output = cv2.addWeighted(img, 1, image_rect, 0.7, 0)

    if hands:
        # 1. Find hand Landmarks
        hand = hands[0]
        cx, cy = hand["center"]  # center point of the hand
        lmList = hand["lmList"]  # List of 21 Landmark points

        # Ratio between two similar dimensions by coordinates
        xInd = int(np.interp(lmList[8][0], (XY_INI, XY_INI + area.width), (screen_points.x0, screen_points.x)))
        yInd = int(np.interp(lmList[8][1], (XY_INI, XY_INI + area.height), (screen_points.y0, screen_points.y)))

        fingers = detector.fingers_up(hand)  # List of which fingers are up
        moves.move_cursor(fingers, xInd, yInd, acc_opt, moves_dic)
        if BUTTON_PRESSED is False:
            moves.finger_acc(cy, fingers, acc_opt, mode, moves_dic)
            BUTTON_PRESSED = True

    # Button Pressed iterations
    if BUTTON_PRESSED:
        DELAY_COUNT += 1
        if DELAY_COUNT > delay:
            DELAY_COUNT = 0
            BUTTON_PRESSED = False

    # Getting the fps
    fps = time_v.calc_fps()

    cv2.putText(output, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)

    cv2.imshow("Virtual Mouse", output)

    key = cv2.waitKey(1)
    if key == 27:  # Press ESC to close te program
        break
cv2.destroyAllWindows()

