import cv2
import numpy as np
from .helpers import *

class Background:
    
    def __init__(self, background_path):
        self.image = fix_channels(cv2.imread(background_path, cv2.IMREAD_UNCHANGED))

