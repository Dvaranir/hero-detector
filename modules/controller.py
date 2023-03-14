import os
import random
import cv2
import numpy as np

from PIL import Image

from .photo import Photo
from .background import Background
from .face_replacer import FaceReplacer
# from .pattern_detector import PatternDetector
from .helpers import *

class Controller:
    
    def __init__(self, photo_path, pattern_path):
        self.photo = Photo(photo_path)
        self.background = Background(self.choose_random_background())
        self.face_replacer = FaceReplacer(self.photo, self.choose_random_mask())
        # self.pattern_detector = PatternDetector(self.photo, pattern_path)
                
        self._BIGGEST_RESOLUTION = 1920
        self._SMALLEST_RESOLUTION = 1080
    
    def make_background_fit_image(self):
        if self.photo.layout_format == 'vertical':
            cut_size = self._BIGGEST_RESOLUTION - self.photo.height
            self.background.image = cut_height(cut_size, self.background.image)
        else:
            cut_size = self._BIGGEST_RESOLUTION - self.photo.width
            self.background.image = cut_width(cut_size, self.background.image)
            
    def make_effect_fit_image(self):
        cut_size = self._SMALLEST_RESOLUTION - self.photo.height
        self.effect = cut_height_from_top(cut_size, self.effect)
        
        
    @staticmethod    
    def make_effect_fit_image_PILL(image):
        width, height = image.size
        
        x0 = 0
        y0 = 200
        x1 = width
        y1 = height
        
        return image.crop((x0, y0, x1, y1))
        
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
        self.random_background = random.choice(all_backgrounds)
        return backgrounds_dir + self.random_background
    
    def check_background_effect(self):
        effects_dir = './effects/'
        all_files = os.listdir(effects_dir)
        all_effects = [x for x in all_files if x.endswith('.png')]
         
        if (self.random_background in all_effects):
            self.effect_path = effects_dir + self.random_background
            self.effect = cv2.imread(self.effect_path, cv2.IMREAD_UNCHANGED)
            return True
        else: return False
            
    def place_photo_on_background(self):
        foreground_pil = Image.fromarray(cv2.cvtColor(self.photo.image, cv2.COLOR_BGR2RGBA))
        background_pil = Image.fromarray(cv2.cvtColor(self.background.image, cv2.COLOR_BGR2RGB))
        
        background_pil = background_pil.resize((foreground_pil.size[0], foreground_pil.size[1]))
        background_pil.paste(foreground_pil, (0, 0), mask=foreground_pil)

        self.photo.image = cv2.cvtColor(np.array(background_pil), cv2.COLOR_RGB2BGR)
            
    def place_effect_on_photo(self):
        if (self.check_background_effect()):
            
            effect_pil = self.make_effect_fit_image_PILL(fix_channels_PIL(Image.fromarray(cv2.cvtColor(self.effect, cv2.COLOR_BGR2RGBA))))
            
            # effect_pil = Image.open(self.effect)
            image_pil = fix_channels_PIL(Image.fromarray(cv2.cvtColor(self.photo.image, cv2.COLOR_BGR2RGB)))
            
            effect_pil = effect_pil.resize((image_pil.size[0], image_pil.size[1]))
            image_pil.paste(effect_pil, (0, 0), mask=effect_pil)

            self.photo.image = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)

    def process_image(self):
        self.photo.remove_background()
        self.photo.resize_to_fullhd()
        self.make_background_fit_image()
        self.place_photo_on_background()
        # self.face_replacer.replace_faces()
        
        self.place_effect_on_photo()
        return save_image(self.photo.image)
        