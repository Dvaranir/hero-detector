import cv2
import inspect
from math import gcd
from rembg import remove, new_session

class Image:
    
    def __init__(self, image_path, background_path):
        self.image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        self.background_image = cv2.imread(background_path, cv2.IMREAD_UNCHANGED)
        self.background_longest_side = 1920
        self.width = self.image.shape[1]
        self.height = self.image.shape[0]
        self.channels = self.image.shape[2]
        self.ratio = gcd(self.width, self.height)
        self.layout_format = self.get_layout_format()
        
        self.log_data(inspect.currentframe())
        # self.process_image()
        
    def get_layout_format(self):
        if self.height > self.width: return 'vertical' 
        else: return 'horizontal' 
        
    def resize_with_aspect_ratio(self, new_size):
        new_height = int(self.height * self.ratio)
        self.image = cv2.resize(self.image, (new_size, new_height), interpolation=cv2.INTER_LINEAR)
        
    def resize_to_fullhd(self):
        if self.layout_format == 'vertical':
            self.resize_with_aspect_ratio(1080)
        else: self.resize_with_aspect_ratio(1920)
        
    def remove_background(self):
        # session = new_session('u2net_human_seg.onnx')
        session = new_session('bisenetv2_human_seg')
        # session = new_session('u2net_portrait')
        self.image = remove(self.image, session=session)
        
    def add_border(self, half_border_size):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2BGRA)
        self.log_data(inspect.currentframe())
        
        if self.layout_format == 'vertical':
            b_top = half_border_size
            b_bottom = half_border_size
            b_left = 0
            b_right = 0
        else:
            b_top = 0
            b_bottom = 0
            b_left = half_border_size
            b_right = half_border_size
        
        self.image = cv2.copyMakeBorder(self.image, b_top, b_bottom, b_left, b_right, cv2.BORDER_CONSTANT, value=(0, 0, 0, 0))

    def cut_background_height(self, cut_size):
        start = int(cut_size / 2)
        end = self.background_longest_side - start
        self.background_image = self.background_image[start:end, :]
    
    def cut_background_width(self, cut_size):
        start = int(cut_size / 2)
        end = int(start + self.background_longest_side - cut_size)
        self.background_image = self.background_image[:, start:end]

    def rotate_background(self):
        self.background_image = cv2.rotate(self.background_image, cv2.ROTATE_90_CLOCKWISE)
        
    def make_background_fit_image(self):
        if self.layout_format == 'vertical':
            self.cut_background_height(self.height)
        else:
            self.rotate_background() 
            self.cut_background_width(self.width)
        
    def process_image(self):
        self.add_border()
        
    def log_data(self, frame=inspect.currentframe()):
        print(f"Method: {inspect.getframeinfo(frame).function}")
        print(f"Width: {self.width}")
        print(f"Height: {self.height}")
        print(f"Channels: {self.channels}")
        print(f"Ratio: {self.ratio}")
        print(f"Layout: {self.layout_format}")
        
    def show_image(self, image):
        cv2.imshow('bordered_image.png', image)
        cv2.waitKey(0)
        
    def save_image(self, image):
        cv2.imwrite('bordered_image.png', image)

        
        
    