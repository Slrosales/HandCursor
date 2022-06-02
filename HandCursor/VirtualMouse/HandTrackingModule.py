"""
Hand Tracking Module
By: Computer Vision Zone
Website: https://www.computervision.zone/

Edited and adapted by: Jason Estrada and Laura Gómez

The modification of the module focused on reading the commands
that the hands can perform, obtaining coordinates and drawing
on the camera frame.
"""

import math
import time
import cv2
import mediapipe as mp
import pyautogui


class HandDetector:
    """
    Finds Hands using the mediapipe library. Exports the landmarks
    in pixel format. Adds extra functionalities like finding how
    many fingers are up or the distance between two fingers. Also
    provides bounding box info of the hand found.
    """

    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, minTrackCon=0.5):
        """
        :param mode: In static mode, detection is done on each image: slower
        :param maxHands: Maximum number of hands to detect
        :param detectionCon: Minimum Detection Confidence Threshold
        :param minTrackCon: Minimum Tracking Confidence Threshold
        """
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.minTrackCon = minTrackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode, max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.minTrackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        self.fingers = []
        self.lmList = []

    def find_hands(self, img, draw=True, flipType=True):
        """
        Finds hands in a BGR image.
        :param img: Image to find the hands in.
        :param draw: Flag to draw the output on the image.
        :return: Image with or without drawings
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        allHands = []
        h, w, c = img.shape
        if self.results.multi_hand_landmarks:
            for handType, handLms in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                myHand = {}
                # lmList
                mylmList = []
                xList = []
                yList = []
                for id, lm in enumerate(handLms.landmark):
                    px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                    mylmList.append([px, py, pz])
                    xList.append(px)
                    yList.append(py)

                # bbox
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                boxW, boxH = xmax - xmin, ymax - ymin
                bbox = xmin, ymin, boxW, boxH
                cx, cy = bbox[0] + (bbox[2] // 2), \
                         bbox[1] + (bbox[3] // 2)

                myHand["lmList"] = mylmList
                myHand["bbox"] = bbox
                myHand["center"] = (cx, cy)

                if flipType:
                    if handType.classification[0].label == "Right":
                        myHand["type"] = "Right"
                    else:
                        myHand["type"] = "Left"
                else:
                    myHand["type"] = handType.classification[0].label
                allHands.append(myHand)

                # draw
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        if draw:
            return allHands, img
        else:
            return allHands

    def fingers_up(self, my_hand):
        """
        Finds how many fingers are open and returns in a list.
        Considers left and right hands separately
        :return: List of which fingers are up
        """
        my_hand_type = my_hand["type"]
        my_lm_list = my_hand["lmList"]
        if self.results.multi_hand_landmarks:
            fingers = []
            # Thumb
            if my_hand_type == "Right":
                if my_lm_list[self.tipIds[0]][0] > my_lm_list[self.tipIds[0] - 1][0]:
                    fingers.append(0)
                else:
                    fingers.append(1)
            else:
                if my_lm_list[self.tipIds[0]][0] < my_lm_list[self.tipIds[0] - 1][0]:
                    fingers.append(0)
                else:
                    fingers.append(1)

            # 4 Fingers
            for id in range(1, 5):
                if my_lm_list[self.tipIds[id]][1] < my_lm_list[self.tipIds[id] - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers

    def find_distance(self, p1, p2, img=None):
        """
        Find the distance between two landmarks based on their
        index numbers.
        :param p1: Point1
        :param p2: Point2
        :param img: Image to draw on.
        :param draw: Flag to draw the output on the image.
        :return: Distance between the points
                 Image with output drawn
                 Line information
        """

        x1, y1 = p1
        x2, y2 = p2
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length = math.hypot(x2 - x1, y2 - y1)
        info = (x1, y1, x2, y2, cx, cy)
        if img is not None:
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
            return length, info, img
        else:
            return length, info


class Moves:
    def __init__(self):
        pass

    def move_cursor(self, fingers, x_ind, y_ind):
        """
            If index finger is up, the cursor will move
            :param fingers: List of which fingers are up
            :param x_ind: x-coordinate of linear interpolation
            :param y_ind: y-coordinate of linear interpolation
        """
        if fingers == [0, 1, 0, 0, 0]:
            # print("move")
            pyautogui.moveTo(x_ind, y_ind)

    def finger_acc(self, cy, fingers):
        """
            Depending on the fingers that are raised,
            a mouse or keyboard action will be executed.
            :param cy: y-coordinate of the center point of the hand
            :param fingers: List of which fingers are up
        """
        if cy <= 250:  # if hand is at the height of the face
            # left clic is pressed
            if fingers == [0, 0, 0, 0, 1]:
                # print("Left click")
                pyautogui.click()

            # right clic is pressed
            if fingers == [0, 0, 0, 1, 1]:
                # print("Right click")
                pyautogui.click(button='right')

            # key left pressed
            if fingers == [1, 0, 0, 0, 0]:
                # print("Left")
                pyautogui.press('left')

            # key right pressed
            if fingers == [0, 0, 1, 1, 1]:
                # print("Right")
                pyautogui.press('right')

            # key up pressed
            if fingers == [1, 1, 1, 0, 0]:
                # print("Up")
                pyautogui.press('up')

                # key down pressed
            if fingers == [0, 1, 1, 0, 0]:
                # print("Down")
                pyautogui.press('down')

            # Stop the commands
            if fingers == [1, 1, 1, 1, 1]:
                time.sleep(0.00001)


def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector(detectionCon=0.8, maxHands=2)
    while True:
        # Get image frame
        success, img = cap.read()
        # Find the hand and its landmarks
        hands, img = detector.find_hands(img)  # with draw
        # hands = detector.findHands(img, draw=False)  # without draw

        if hands:
            # Hand 1
            hand1 = hands[0]
            lmList1 = hand1["lmList"]  # List of 21 Landmark points
            bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
            centerPoint1 = hand1['center']  # center of the hand cx,cy
            handType1 = hand1["type"]  # Handtype Left or Right

            fingers1 = detector.fingers_up(hand1)

            if len(hands) == 2:
                # Hand 2
                hand2 = hands[1]
                lmList2 = hand2["lmList"]  # List of 21 Landmark points
                bbox2 = hand2["bbox"]  # Bounding box info x,y,w,h
                centerPoint2 = hand2['center']  # center of the hand cx,cy
                handType2 = hand2["type"]  # Hand Type "Left" or "Right"

                fingers2 = detector.fingers_up(hand2)

                # Find Distance between two Landmarks. Could be same hand or different hands
                length, info, img = detector.find_distance(lmList1[8][0:2], lmList2[8][0:2], img)  # with draw
                # length, info = detector.findDistance(lmList1[8], lmList2[8])  # with draw
        # Display
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
