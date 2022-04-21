"""
    In the UML there are classes like "Draw" and "Movement",
    however it is not in the code because the backend structure is being re-planned.
    
    Also, "Manual" is commented because we haven't yet made the interface to play
    the video guide, so we avoid running the "error" code.
"""


from HandTrackingModule import HandDetector
import cv2
import numpy as np
import pyautogui
import time

"""
class Manual(Camara):
    def __init__(self, wCam, hCam)  # Reusing dimensions
        super().__init__(wCam, hCam)
        
    def show(self, url):
        video = pafy.new(url)
        best = video.getbest()
        media = vlc.MedipLyer(best.url)
        media.play()
"""

class Camara:
    def __init__(self, wCam, hCam, bDelay, img):
        self.wCam = wCam
        self.hCam = hCam
        self.bDelay = bDelay
        self.img = img

    def Line(self, divLine):
        cv2.line(self.img, (0, divLine), (self.wCam, divLine), (0, 255, 0), 4)


class Video:
    def __int__(self):
        pass

    def run(self):
        wScr, hScr = pyautogui.size()
        wCam, hCam = int(wScr / 2), int(hScr / 2)
        # print(wCam, hCam)
        divLine = int(hCam / 2)  # y position of the line

        cap = cv2.VideoCapture(0)
        cap.set(3, wCam)
        cap.set(4, hCam)

        buttonPressed = False
        bCounter = 0
        bDelay = 15  # Limit on consecutive presses of a single button based of fps
        pTime = 0  # Previews time
        cTime = 0  # Current time

        # Hand Detector
        detector = HandDetector(maxHands=1)
        while True:
            success, img = cap.read()
            img = cv2.flip(img, 1)
            hands, img = detector.findHands(img, flipType=False)

            if hands and buttonPressed is False:
                # 1. Find hand Landmarks
                hand = hands[0]
                cx, cy = hand["center"]  # center point of the hand
                lmList = hand["lmList"]  # List of 21 Landmark points

                fingers = detector.fingersUp(hand)  # List of which fingers are up
                # print(fingers)
                c = 0
                if cy <= divLine:  # if hand is at the height of the face
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

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                        (255, 0, 255), 3)

            bDelay = int(fps / 2)

            camara = Camara(wCam, hCam, bDelay, img)
            camara.Line(divLine)

            cv2.imshow("Virtual Mouse", img)
            key = cv2.waitKey(1)
            if key == 27:  # Press ESC to close te program
                break


if __name__ == '__main__':
    video = Video()
    video.run()
