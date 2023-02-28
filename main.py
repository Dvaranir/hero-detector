from modules.background import Background
from modules.controller import Controller

def_input = './tests/from_client2.jpg' # Load the image
def_background = './backgrounds/01.png'
def_pattern = './pattern/marker.png'

controller = Controller(def_input, def_pattern)

# controller.photo.remove_background()

# cv2.imshow('bordered_image.png', bcs.photo.image)
# cv2.waitKey(0)
controller.process_image()

