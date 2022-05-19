from HandTrackingModule import HandDetector
import cv2
import numpy as np
import pyautogui
import time


class Camara:
    def __init__(self, img, screen_x_fin, screen_y_fin, delay, cam_height, cam_width):
        self.img = img
        self.screen_x_ini = 0
        self.screen_y_ini = 0
        self.screen_x_fin = screen_x_fin
        self.screen_y_fin = screen_y_fin
        self.xy_ini = 100
        self.delay = delay
        self.aspect_ratio_scr = (self.screen_x_fin - self.screen_x_ini) / (self.screen_y_fin - self.screen_y_ini)
        self.cam_width = cam_width
        self.cam_height = cam_height

    def line(self, div_line):
        cv2.line(self.img, (0, div_line), (self.cam_width, div_line), (0, 255, 0), 4)

    def dimensions(self):
        area_width = cam_width - self.xy_ini * 2
        area_height = int(area_width / self.aspect_ratio_scr)

        image_rect = np.zeros(img.shape, np.uint8)  # new cap with black background
        image_rect = cv2.rectangle(image_rect, (self.xy_ini, self.xy_ini), (self.xy_ini + area_width, self.xy_ini + area_height),
                                   (255, 0, 0), -1)
        output = cv2.addWeighted(img, 1, image_rect, 0.7, 0)



if __name__ == '__main__':
    screen_x_fin, screen_y_fin = pyautogui.size()

    # Time Var
    counter = 0
    prev_time = 0
    current_time = 0

    div_line = 250  # y position of the line

    # Video on
    cap = cv2.VideoCapture(1)  # 0: main camera; 1: external camera

    # Hand Detector
    detector = HandDetector(maxHands=1)

    while True:
        success, img = cap.read()

        if not success:
            print("Esa camara no esta disponible")
            break

        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

        delay = int(fps / 2)

        # Image corrections
        cam_height, cam_width, channel = img.shape  # Cam dimensions
        img = cv2.flip(img, 1)  # 1: x flip ; 0: y flip
        hands, img = detector.findHands(img, flipType=False)

        camara = Camara(img, screen_x_fin, screen_y_fin, delay, cam_height, cam_width)
        camara.line(div_line)
        camara.dimensions()

        cv2.putText(output, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("Virtual Mouse", output)

        key = cv2.waitKey(1)
        if key == 27:  # Press ESC to close te program
            break
    cv2.destroyAllWindows()
