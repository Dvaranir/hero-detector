import cv2
import inspect
import numpy as np

from PIL import Image
from rembg import remove, new_session

class Photo:
    
    def __init__(self, photo_path):
        self.image = cv2.imread(photo_path, cv2.IMREAD_UNCHANGED)
        self.update_data()
        
    def get_layout_format(self):
        if self.height > self.width: return 'vertical' 
        else: return 'horizontal' 
        
    def resize_with_aspect_ratio(self, new_size):
        new_height = int(new_size / self.ratio)
        self.image = cv2.resize(self.image, (new_size, new_height), interpolation=cv2.INTER_LINEAR)
        self.update_data()

    def resize_to_fullhd(self):
        if (self.layout_format == 'horizontal'):
            new_height = 1080
            new_width = int(new_height * self.ratio)
            if new_width > 1920:
                new_width = 1920
                new_height = int(new_width / self.ratio)
                image_pil = Image.fromarray(self.image)
                image_pil = image_pil.resize((new_width, new_height), resample=Image.BICUBIC)
                self.image = np.array(image_pil)
        else:
            new_width = 1080
            new_height = int(new_width / self.ratio)
            if new_height > 1920:
                new_height = 1920
                new_width = int(new_height * self.ratio)
                image_pil = Image.fromarray(self.image)
                image_pil = image_pil.resize((new_width, new_height), resample=Image.BICUBIC)
                self.image = np.array(image_pil)
        self.update_data()
        
    def remove_background(self):
        session = new_session('bisenetv2_human_seg')
        self.image = remove(self.image, session=session)
        
    def update_data(self):
        self.height = self.image.shape[0]
        self.width = self.image.shape[1]
        self.channels = self.image.shape[2]
        self.ratio = self.width / self.height
        self.layout_format = self.get_layout_format()
        
    def log_data(self, frame=inspect.currentframe()):
        print(f"Method: {inspect.getframeinfo(frame).function}")
        print(f"Width: {self.width}")
        print(f"Height: {self.height}")
        print(f"Channels: {self.channels}")
        print(f"Ratio: {self.ratio}")
        print(f"Layout: {self.layout_format}")
        


        
        
    