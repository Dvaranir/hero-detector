import os
import random
import cv2
import numpy as np

from PIL import Image

from .photo import Photo
from .background import Background
from .face_replacer import FaceReplacer
from .pattern_detector import PatternDetector
from .helpers import *

class Controller:
    
    def __init__(self, photo_path, pattern_path):
        self.photo = Photo(photo_path)
        self.background = Background(self.choose_random_background())
        self.face_replacer = FaceReplacer(self.photo, self.choose_random_mask())
        self.pattern_detector = PatternDetector(self.photo, pattern_path)
                
        self._BIGGEST_RESOLUTION = 1920
        self._SMALLEST_RESOLUTION = 1080
    
    def make_background_fit_image(self):
        if self.photo.layout_format == 'vertical':
            cut_size = self._BIGGEST_RESOLUTION - self.photo.height
            self.background.image = cut_height(cut_size, self.background.image)
        else:
            cut_size = self._BIGGEST_RESOLUTION - self.photo.width
            self.background.image = cut_width(cut_size, self.background.image)
            
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
    
    
    # def crop_background(self):
    #     background_height = self.background.image.shape[0]
    #     background_width = self.background.image.shape[1]
        
    #     if (self.photo.layout_format == 'vertical'):
    #         crop_size = 1920 - self.photo.height
    #         new_height = 1920 - crop_size
    #         y = int(crop_size / 2)
    #         x = 0
    #         self.background.image = self.background.image[y:new_height, x:x+background_width]
    #     else:
    #         crop_size = 1920 - self.photo.width
    #         new_width = 1920 - crop_size
    #         x = int(crop_size / 2)
    #         y = 0
    #         self.background.image = self.background.image[y:background_height, x:x+new_width]
            
            
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
        # self.photo.remove_background()
        # self.photo.resize_to_fullhd()
        # # self.crop_background()
        # self.make_background_fit_image()
        # self.place_photo_on_background()
        # self.face_replacer.replace_faces()
        # save_image(self.photo.image)
        self.pattern_detector.marker_found()
        