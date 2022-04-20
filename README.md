# Introduction

Technology advances and innovates with the intention of making our daily lives easier. For example, one day you have an important presentation and you already have the slides projected on the board, but you forgot the control that allows you to control the presentation remotely. Instead of approaching the PC every now and then to change the slide, you can open the virtual mouse software, which has the purpose of speeding up certain behaviors when using the computer, replacing the physical mouse and integrating some of the keyboard's own functionalities to: move the slide forward or backward, move the cursor on the screen, click on the buttons, make annotations, etc. From a distance, since its usefulness consists in detecting human hand gestures through the camera in real time, to perform certain tasks thanks to libraries and trained modules such as OpenCV, CVzone, MediaPipe and PyAutoGUI.

# Commands

In the following table, some gestures and the function they perform are shown. It should be noted that in the code, the fingers of a hand are stored in a list of 5 spaces, where:
- 1: finger up
- 0: finger down
- List positions are for:
  - 1st: Thumb
  - 2nd: Index finger
  - 3rd: Middle/heart
  - 4th: Ring finger
  - 5th: Little finger

List of Fingers|Max. Hands|Function|
|:----:|:----:|:----:|
[0,1,0,0,0]|1|Move the cursor|
[0,0,0,0,1]|1|Left click|
[0,0,0,1,1]|1|Right click|
[0,0,0,0,0]|1| |
[0,0,0,0,0]|1| |
[0,0,0,0,0]|1| |

