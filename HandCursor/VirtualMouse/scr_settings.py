import time
from tkinter import messagebox

import cv2
import pyautogui
import tkinter as tk


# Global auxiliary variable containing the default values
# of the possible actions that can be executed by the user.
global aux
aux = {
    "move": [0, 1, 0, 0, 0],
    "left click": [0, 0, 0, 0, 1],
    "right click": [0, 0, 0, 1, 1],
    "left arrow": [1, 0, 0, 0, 0],
    "right arrow": [1, 1, 0, 0, 0],
    "up arrow": [1, 1, 1, 0, 0],
    "down arrow": [0, 1, 1, 0, 0]
}


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


class WindowOpt:
    def __init__(self):
        # Editable dictionary
        self.configuration = {
            "move": [0, 1, 0, 0, 0],
            "left click": [0, 0, 0, 0, 1],
            "right click": [0, 0, 0, 1, 1],
            "left arrow": [1, 0, 0, 0, 0],
            "right arrow": [1, 1, 0, 0, 0],
            "up arrow": [1, 1, 1, 0, 0],
            "down arrow": [0, 1, 1, 0, 0]
        }
        # Actions the user wants to execute
        self.selected_options = {}

        # Create window
        self.window = tk.Tk()
        self.window.title("Seleccionar acciones")

        # Align the window in the center of the screen.
        self.window_width = 350
        self.window_height = 300

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

        # Create checkboxes
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

        # The text box opens allowing the user to configure the action command.
        opt1_cbox.configure(command=lambda: self.activate_settings(0))
        opt2_cbox.configure(command=lambda: self.activate_settings(1))
        opt3_cbox.configure(command=lambda: self.activate_settings(2))
        opt4_cbox.configure(command=lambda: self.activate_settings(3))
        opt5_cbox.configure(command=lambda: self.activate_settings(4))
        opt6_cbox.configure(command=lambda: self.activate_settings(5))
        opt7_cbox.configure(command=lambda: self.activate_settings(6))

        # Button for processing selection
        process_button = tk.Button(self.window, text="Aceptar", command=self.process_selection)
        process_button.pack()

    def activate_settings(self, index):
        if index == 0 and self.opt1.get() == 1:
            # Create an instance of the class HandSettings
            HandSettings("move", self.configuration, self.selected_options)
        elif index == 1 and self.opt2.get() == 1:
            HandSettings("left click", self.configuration, self.selected_options)
        elif index == 2 and self.opt3.get() == 1:
            HandSettings("right click", self.configuration, self.selected_options)
        elif index == 3 and self.opt4.get() == 1:
            HandSettings("left arrow", self.configuration, self.selected_options)
        elif index == 4 and self.opt5.get() == 1:
            HandSettings("right arrow", self.configuration, self.selected_options)
        elif index == 5 and self.opt6.get() == 1:
            HandSettings("up arrow", self.configuration, self.selected_options)
        elif index == 6 and self.opt7.get() == 1:
            HandSettings("down arrow", self.configuration, self.selected_options)

    def process_selection(self):
        # Dictionary with actions activated or not
        self.selected_options = {"move": self.opt1.get(), "left click": self.opt2.get(), "right click": self.opt3.get(),
                                 "left arrow": self.opt4.get(), "right arrow": self.opt5.get(),
                                 "up arrow": self.opt6.get(), "down arrow": self.opt7.get()}

        # Close the window after processing the selection
        self.window.destroy()


class HandSettings:
    """
    :param action: String of the action to which the command is to be modified
    :param configuration: Dictionary with the command of each action
    :param selected_options: Dictionary that tells whether the action is activated or not
    """
    def __init__(self, action, configuration, selected_options):

        self.selected_options = selected_options
        self.action = action
        self.configuration = configuration

        # Initial command list
        self.command = [0, 0, 0, 0, 0]
        self.finger_names = ["Pulgar", "Indice", "Medio", "Anular", "Meñique"]

        # List for storing the text variables of the buttons
        self.button_texts = []
        # List to store the buttons
        self.buttons = []

        # Create window
        self.window = tk.Tk()
        self.window.title("Configuración de comandos")

        # Align the window in the center of the screen.
        self.window_width = 400
        self.window_height = 200

        screen_width = self.window.winfo_screenwidth()
        screen_height =self. window.winfo_screenheight()

        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2

        self.window.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

        # Create buttons and labels and add them to the window
        for i in range(len(self.command)):
            # Variable de texto para el botón
            text = tk.StringVar()
            text.set("OFF")

            # Create button with the value of the gesture list as text
            button = tk.Button(self.window, textvariable=text, width=5, height=2,
                               command=lambda index=i: self.toggle_value(index))
            button.grid(row=1, column=i, padx=2, pady=2)

            # The background color of the button is set according to the initial value of the gesture list.
            if self.command[i] == 0: # OFF
                button.config(bg="red")
            else: # ON
                button.config(bg="green")

            # Text variable is added to the list
            self.button_texts.append(text)

            # The button is added to the list
            self.buttons.append(button)

            # The name of each finger is placed under the respective button.
            label = tk.Label(self.window, text=self.finger_names[i])
            label.grid(row=0, column=i, padx=5)

        accept_button = tk.Button(self.window, text="Aceptar", command=self.accept_selection)
        accept_button.grid(row=2, column=0, padx=5, pady=10)

        default_button = tk.Button(self.window, text="Predeterminado", command=self.set_default)
        default_button.grid(row=2, column=1, padx=5, pady=10)

        self.window.mainloop()

    # Function to change the value in the gesture list when a button is pressed
    def toggle_value(self, index):
        if self.command[index] == 0:
            self.command[index] = 1
            self.button_texts[index].set("ON")
            self.buttons[index].config(bg="green")
        else:
            self.command[index] = 0
            self.button_texts[index].set("OFF")
            self.buttons[index].config(bg="red")

    # Button "Aceptar"
    def accept_selection(self):
        # The key is updated with a new command value
        self.configuration[self.action] = self.command
        self.window.destroy()

    # button "Prederterminado"
    def set_default(self):
        # The selected action returns to the initial command
        self.configuration[self.action] = aux[self.action]
        self.window.destroy()











