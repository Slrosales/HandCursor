import time
import cv2
import pyautogui
import tkinter as tk


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


class window_opt:
    def __init__(self):
        self.selected_options = []

        # Create window
        self.window = tk.Tk()
        self.window.title("Seleccionar acciones")

        # Align the window in the center of the screen.
        self.window_width = 350
        self.window_height = 320

        screen_width = self.window.winfo_screenwidth()
        screen_height =self. window.winfo_screenheight()

        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2

        self.window.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

        # Create variables to store the values of the checkboxes
        self.opt1 = tk.IntVar()
        self.opt2 = tk.IntVar()
        self.opt3 = tk.IntVar()
        self.opt4 = tk.IntVar()
        self.opt5 = tk.IntVar()
        self.opt6 = tk.IntVar()
        self.opt7 = tk.IntVar()

        # Crear checkboxes
        opt1_cbox = tk.Checkbutton(self.window, text="Move the cursor", variable=self.opt1)
        opt2_cbox = tk.Checkbutton(self.window, text="Left click", variable=self.opt2)
        opt3_cbox = tk.Checkbutton(self.window, text="Right click", variable=self.opt3)
        opt4_cbox = tk.Checkbutton(self.window, text="Left arrow", variable=self.opt4)
        opt5_cbox = tk.Checkbutton(self.window, text="Right arrow", variable=self.opt5)
        opt6_cbox = tk.Checkbutton(self.window, text="Up arrow", variable=self.opt6)
        opt7_cbox = tk.Checkbutton(self.window, text="Down arrow", variable=self.opt7)

        # Place checkboxes in the window
        opt1_cbox.pack(anchor="w")
        opt2_cbox.pack(anchor="w")
        opt3_cbox.pack(anchor="w")
        opt4_cbox.pack(anchor="w")
        opt5_cbox.pack(anchor="w")
        opt6_cbox.pack(anchor="w")
        opt7_cbox.pack(anchor="w")

        # Button for processing selection
        process_button = tk.Button(self.window, text="Aceptar", command=self.process_selection)
        process_button.pack()

    def process_selection(self):
        self.selected_options = [self.opt1.get(), self.opt2.get(), self.opt3.get(), self.opt4.get(), self.opt5.get(),
                                 self.opt6.get(), self.opt7.get()]

        # Close the window after processing the selection
        self.window.destroy()










