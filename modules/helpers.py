import cv2
import uuid
import inspect
import numpy as np
    
def check_channels(photo): return photo.shape[2] < 4

def fix_channels(photo):
    if (not check_channels(photo)): return photo
    
    alpha = np.ones(photo.shape[:2], dtype=photo.dtype) * 255
    return cv2.merge((photo, alpha))

def cut_height(cut_size, image):
    start = int(cut_size / 2)
    end = 1920 - start
    return image[start:end, :]

def cut_width(cut_size, image):
    start = int(cut_size / 2)
    end = int(start + 1920 - cut_size)
    return image[:, start:end]

def save_image(image):
    image_name = f'photo-{str(uuid.uuid4())[:10]}.png'
    cv2.imwrite(image_name, image)
    
def show_image(image, frame=inspect.currentframe()):
    cv2.imshow(f'{inspect.getframeinfo(frame).function}', image)
    cv2.waitKey(0)
