import os
import random
import cv2
import uuid
import inspect
import numpy as np

from PIL import Image

from .photo import Photo
from .background import Background
from .face_replacer import FaceReplacer

class Controller:
    
    def __init__(self, photo_path):
        self.photo = Photo(photo_path)
        self.background = Background(self.choose_random_background())
        self.face_replacer = FaceReplacer(self.photo, self.choose_random_mask())
                
        self._BIGGEST_RESOLUTION = 1920
        self._SMALLEST_RESOLUTION = 1080
        
    @staticmethod
    def cut_height(cut_size, image):
        start = int(cut_size / 2)
        end = 1920 - start
        return image[start:end, :]

    @staticmethod
    def cut_width(cut_size, image):
        start = int(cut_size / 2)
        end = int(start + 1920 - cut_size)
        return image[:, start:end]
    
    @staticmethod
    def save_image(image):
        image_name = f'photo-{uuid.getnode()}.png'
        cv2.imwrite(image_name, image)
        
    @staticmethod
    def show_image(image, frame=inspect.currentframe()):
        cv2.imshow(f'{inspect.getframeinfo(frame).function}', image)
        cv2.waitKey(0)
    
    def make_background_fit_image(self):
        if self.photo.layout_format == 'vertical':
            self.background.cut_height(self.photo.height)
        else:
            self.background.cut_width(self.photo.width)
            
    def choose_random_mask(self):
        masks_dir = './masks/'
        all_files = os.listdir(masks_dir)
        all_masks = [x for x in all_files if x.endswith('.png')]
        return masks_dir + random.choice(all_masks)
    
    def choose_random_background(self):
        backgrounds_dir = './backgrounds/vertical/'
        if (self.photo.layout_format == 'horizontal'): backgrounds_dir = './backgrounds/horizontal/'
        all_files = os.listdir(backgrounds_dir)
        all_backgrounds = [x for x in all_files if x.endswith('.png')]
        return backgrounds_dir + random.choice(all_backgrounds)
    
    
    def crop_background(self):
        background_height = self.background.image.shape[0]
        background_width = self.background.image.shape[1]
        
        if (self.photo.layout_format == 'vertical'):
            crop_size = 1920 - self.photo.height
            new_height = 1920 - crop_size
            y = int(crop_size / 2)
            x = 0
            self.background.image = self.background.image[y:new_height, x:x+background_width]
        else:
            crop_size = 1920 - self.photo.width
            new_width = 1920 - crop_size
            x = int(crop_size / 2)
            y = 0
            self.background.image = self.background.image[y:background_height, x:x+new_width]
            
            
    def place_photo_on_background(self):
        foreground_pil = Image.fromarray(cv2.cvtColor(self.photo.image, cv2.COLOR_BGR2RGBA))
        background_pil = Image.fromarray(cv2.cvtColor(self.background.image, cv2.COLOR_BGR2RGB))
        
        background_pil = background_pil.resize((foreground_pil.size[0], foreground_pil.size[1]))
        background_pil.paste(foreground_pil, (0, 0), mask=foreground_pil)

        self.photo.image = cv2.cvtColor(np.array(background_pil), cv2.COLOR_RGB2BGR)

    # def get_border_size(self):
    #     if self.photo.layout_format == 'vertical': self.photo.border_size = self._BIGGEST_RESOLUTION - self.height
    #     else: self.photo.border_size = self._BIGGEST_RESOLUTION - self.photo.width
    
    # def add_border(self):
    #     self.get_border_size()
    #     self.photo.image = cv2.cvtColor(self.photo.image, cv2.COLOR_BGR2BGRA)
    #     half_border_size = int(self.photo.border_size / 2)
    #     print(self.photo.border_size)
    #     print(half_border_size)
    #     if self.photo.layout_format == 'vertical':
    #         b_top = half_border_size
    #         b_bottom = half_border_size
    #         b_left = 0
    #         b_right = 0
    #     else:
    #         b_top = 0
    #         b_bottom = 0
    #         b_left = half_border_size
    #         b_right = half_border_size
            
    #     self.photo.image = cv2.copyMakeBorder(self.photo.image, b_top, b_bottom, b_left, b_right, cv2.BORDER_CONSTANT, value=(0, 0, 0, 0))
    
    def process_image(self):
        self.photo.remove_background()
        self.photo.resize_to_fullhd()
        self.crop_background()
        self.place_photo_on_background()
        self.face_replacer.detect_faces()
        # self.save_image(self.photo_replaced_background)
        