from modules.background import Background
from modules.controller import Controller

def_input = './tests/5.jpg' # Load the image
# def_background = './backgrounds/01.png'
def_pattern = './pattern/marker.png'

controller = Controller(def_input, def_pattern)

controller.process_image()

