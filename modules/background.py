import cv2
import numpy as np

class Background:
    
    def __init__(self, background_path):
        self.image = cv2.imread(background_path, cv2.IMREAD_UNCHANGED)
        self.add_alpha()
        
    def add_alpha(self):
        if self.image.shape[2] < 4:
            alpha = np.ones(self.image.shape[:2], dtype=self.image.dtype) * 255
            self.image = cv2.merge((self.image, alpha))
        
    




