from HandTrackingModule import HandDetector
import cv2
import numpy as np
import pyautogui
import time

"""
class Manual:
    def show(self, url):
        video = pafy.new(url)
        best = video.getbest()
        media = vlc.MedipLyer(best.url)
        media.play()
"""


class Movement:
    def __init__(self):
        pass


class Draw(Movement):
    pass


class Camara:
    def __init__(self, wCam, hCam, bDelay):
        self.wCam = wCam
        self.hCam = hCam
        self.bDelay = bDelay

    def Line(self, divLine):
        self.divLine = divLine
        cv2.line(img, (0, divLine), (wCam, divLine), (0, 255, 0), 4)


wScr, hScr = pyautogui.size()
wCam, hCam = int(wScr / 2), int(hScr / 2)
# print(wCam, hCam)
divLine = int(hCam / 2)  # y position of the line

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0
cTime = 0

# Hand Detector
detector = HandDetector(maxHands=1)
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        move = Movement()

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)

    bDelay = int(fps / 2)

    camara = Camara(wCam, hCam, bDelay)
    camara.Line(divLine)

    cv2.imshow("Virtual Mouse", img)
    key = cv2.waitKey(1)
    if key == 27:  # Press ESC to close te program
        break
