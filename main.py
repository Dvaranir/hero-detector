from modules.image_data import Image
import cv2

def_input = './tests/6.jpg' # Load the image
def_background = './backgrounds/01.png'
img = Image(def_input, def_background)

img.crop_background(513)

# cv2.imshow('bordered_image.png', img.image)
# cv2.waitKey(0)
# cv2.imwrite('bordered_image.png', add_border(img.image))

