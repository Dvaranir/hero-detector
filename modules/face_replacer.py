import cv2

import math
import dlib
import numpy as np

from math import hypot

class FaceReplacer:
    
    def __init__(self, photo, mask):
        self.photo = photo
        self.photo_gray = cv2.cvtColor(self.photo.image, cv2.COLOR_BGR2GRAY)
        self.mask = cv2.imread(mask, cv2.IMREAD_UNCHANGED)
        self.predictor = dlib.shape_predictor('./models/shape_predictor_68_face_landmarks.dat')
        self.face_detector = dlib.get_frontal_face_detector()
    
    @staticmethod
    def round_up(n, decimals = 0):
        # if (decimals == 100): return n
        print(n)
        multiplier = 10 ** decimals
        return math.ceil(n * multiplier) / multiplier

    def detect_faces(self):
        self.faces = self.face_detector(self.photo_gray)

        for face in self.faces:
            landmarks = self.predictor(self.photo_gray, face)

            face_left_part = 0
            face_left = (landmarks.part(face_left_part).x, landmarks.part(face_left_part).y)

            face_right_part = 16
            face_right = (landmarks.part(face_right_part).x, landmarks.part(face_right_part).y)

            face_bottom_part = 9
            face_bottom = (landmarks.part(face_bottom_part).x, landmarks.part(face_bottom_part).y)

            face_center = [landmarks.part(8).x, landmarks.part(30).y]

            face_top = [landmarks.part(27).x, landmarks.part(20).y]

            length_from_right = face_right[0] - face_center[0]
            length_from_left = face_center[0] - face_left[0]

            deflection_percent = 100

            print("From top", length_from_right)
            print("From left", length_from_left + length_from_left / 100 * deflection_percent)

            if length_from_left > length_from_right:
                deflection_percent -= length_from_right / (length_from_left / 100)
                face_center[0] -= length_from_right / 100 * deflection_percent

            elif length_from_right > length_from_left:
                deflection_percent -= length_from_left / (length_from_right / 100)
                face_center[0] += length_from_left / 100 * deflection_percent
            deflection_percent = self.round_up(deflection_percent)

            mask_height = self.mask.shape[0]
            mask_width = self.mask.shape[1]
            
            mask_height_ratio = self.round_up(mask_height / mask_width)

            face_width = int(hypot(face_left[0] - face_right[0],
                                face_left[1] - face_right[1]))

            face_height = int(face_width * mask_height_ratio)
            face_height = int(face_height + (face_height / 100) * 30)

            face_width = int(face_width + (face_width / 100) * 30)

            face_top_left = (int(face_center[0] - face_width / 2),
                            int(face_center[1] - face_height / 2))

            face_bottom_right = (int(face_center[0] + face_width / 2),
                                int(face_center[1] + face_height / 2))

            face_area = self.photo.image[face_top_left[1]: face_top_left[1] + face_height,
                                    face_top_left[0]: face_top_left[0] + face_width]

            mask_resized = cv2.resize(self.mask, (face_width, face_height))
            mask_image_gray = cv2.cvtColor(mask_resized, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(mask_image_gray, 0, 255, cv2.THRESH_BINARY_INV)

            face_area_no_face = cv2.bitwise_and(face_area, face_area, mask=mask)
            
            if mask_resized.shape[2] < 4:
                alpha = np.ones(mask_resized.shape[:2], dtype=mask_resized.dtype) * 255
                mask_resized = cv2.merge((mask_resized, alpha))
                
            if face_area_no_face.shape[2] < 4:
                alpha = np.ones(face_area_no_face.shape[:2], dtype=face_area_no_face.dtype) * 255
                face_area_no_face = cv2.merge((face_area_no_face, alpha))
            
            final_mask = cv2.add(face_area_no_face, mask_resized)

            writable_photo = self.photo.image.copy()
            writable_photo.flags.writeable = True
            
            if writable_photo.shape[2] < 4:
                alpha = np.ones(writable_photo.shape[:2], dtype=writable_photo.dtype) * 255
                writable_photo = cv2.merge((writable_photo, alpha))
            
            writable_photo[face_top_left[1]: face_top_left[1] + face_height,
                        face_top_left[0]: face_top_left[0] + face_width] = final_mask

            # cv2.rectangle(input_image, face_top_left, face_bottom_right, (0, 255, 0), 2)
            # cv2.circle(input_image, face_center, 3, (0, 255, 0), -1)

            # cv2.circle(input_image, face_left, 3, (255, 0, 0), -1)
            # cv2.circle(input_image, face_right, 3, (255, 0, 0), -1)
            # cv2.circle(input_image, face_bottom, 3, (255, 0, 0), -1)

            cv2.imshow('Input Image Replaced BG', writable_photo)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            # cv2.imshow('Target mask', mask_resized)


    


