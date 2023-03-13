import cv2
import os
import uuid
import inspect
import numpy as np
    
def check_channels(photo): return photo.shape[2] < 4

def fix_channels(photo):
    if (not check_channels(photo)): return photo
    
    alpha = np.ones(photo.shape[:2], dtype=photo.dtype) * 255
    return cv2.merge((photo, alpha))

def fix_channels_PIL(photo):
    if photo.mode != "RGBA": return photo.convert("RGBA")
    else: return photo

def cut_height(cut_size, image):
    start = int(cut_size / 2)
    end = 1920 - start
    return image[start:end, :]

def cut_height_from_top(cut_size, image):
    return image[cut_size:, :]

def cut_width(cut_size, image):
    start = int(cut_size / 2)
    end = int(start + 1920 - cut_size)
    return image[:, start:end]

def generate_image_name():
    return f'photo-{str(uuid.uuid4())[:10]}.png'

def save_image(image):
    current_directory = os.getcwd()
    image_name = generate_image_name()
    image_path = f'{current_directory}/output_images/{image_name}'
    cv2.imwrite(image_path, image)
    return image_path
    
def show_image(image, frame=inspect.currentframe()):
    cv2.imshow(f'{inspect.getframeinfo(frame).function}', image)
    cv2.waitKey(0)
