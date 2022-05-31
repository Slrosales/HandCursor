import time
import cv2
import pyautogui


class Dimensions:
    def __init__(self, height, width):
        self.height = height
        self.width = width


class TimeV:
    def __init__(self, prev_time=0, current_time=0):
        self.prev_time = prev_time
        self.current_time = current_time
        self.fps_ = 0

    def calc_fps(self):
        self.current_time = time.time()
        self.fps_ = 1 / (self.current_time - self.prev_time)
        self.prev_time = self.current_time

        return self.fps_


class ScreenPoints:
    def __init__(self, x0=0, y0=0, x=1920, y=1080):
        self.x0 = x0
        self.y0 = y0
        self.x = x
        self.y = y


class Start:
    def turn_video_on(self):
        OPT_1 = "Camara 1"
        OPT_2 = "Camara 2"
        OPT_3 = "Otra"

        opt = pyautogui.confirm(
            "Bienvenidx, a continuacón escoge que cámara usarás", "Elegir cámara",
            [OPT_1, OPT_2, OPT_3]
        )

        if opt == OPT_1:
            cam = 0
        elif opt == OPT_2:
            cam = 1
        elif opt == OPT_3:
            cam = int(pyautogui.prompt("Ingresa el número de la cámara", "Elegir otra cámara"))

        return cv2.VideoCapture(cam)

    def define_fps(self, fps):
        OPT_1 = "Juego"
        OPT_2 = "Diapositiva"

        opt = pyautogui.confirm(
            "A continuacón escoge que modo usarás", "Elegir modo",
            [OPT_1, OPT_2]
        )

        if opt == OPT_1:
            delay = 0
        elif opt == OPT_2:
            if fps < 35:
                delay = 20
            else:
                delay = 30

        return delay
