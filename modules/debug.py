import cv2

class Debug:
    
    @staticmethod
    def show_image(image):
        cv2.imshow('bordered_image.png', image)
        cv2.waitKey(0)
    
    @staticmethod
    def save_image(image):
        cv2.imwrite('bordered_image.png', image)