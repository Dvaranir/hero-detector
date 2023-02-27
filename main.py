from modules.background import Background
from modules.controller import Controller
import cv2
import os

def_input = './tests/6.jpg' # Load the image
def_background = './backgrounds/01.png'

controller = Controller(def_input)

# controller.photo.remove_background()

# cv2.imshow('bordered_image.png', bcs.photo.image)
# cv2.waitKey(0)
controller.process_image()

