import cv2
import numpy as np
import torch
import torchvision.transforms.functional as F
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image

from .helpers import *

class PatternDetector:
    
    def __init__(self, photo, pattern_path):
        self.pattern = fix_channels(cv2.imread(pattern_path, cv2.IMREAD_UNCHANGED))
        self.photo = fix_channels(photo.image)

    def marker_found(self):
        # model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

        # pattern_img = self.pattern

        # pattern_tensor = torch.from_numpy(pattern_img).float().permute(2, 0, 1).unsqueeze(0) / 255

        # search_img = self.photo

        # results = model(search_img)

        # for obj in results.pred[0]:

        #     x1, y1, x2, y2 = obj[:4].int().tolist()

        #     obj_patch = search_img[y1:y2, x1:x2]

        #     obj_patch_resized = cv2.resize(obj_patch, (pattern_img.shape[1], pattern_img.shape[0]))

        #     obj_tensor = torch.from_numpy(obj_patch_resized).float().permute(2, 0, 1).unsqueeze(0) / 255

        #     similarity = torch.nn.functional.cosine_similarity(pattern_tensor, obj_tensor, dim=1)

        #     if similarity.item() > 0.9:
        #         print("True")
        #         break
        # else:
        #     print("False")
        
        
        img_gray = cv2.cvtColor(self.photo, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(self.pattern, cv2.COLOR_BGR2GRAY)

        sift = cv2.SIFT_create()

        kp1, des1 = sift.detectAndCompute(img_gray, None)
        kp2, des2 = sift.detectAndCompute(template_gray, None)

        bf = cv2.BFMatcher()

        matches = bf.knnMatch(des1, des2, k=2)

        good_matches = []
        for m, n in matches:
            if m.distance < 0.77 * n.distance:
                good_matches.append(m)

        img_matches = cv2.drawMatches(self.photo, kp1, self.pattern, kp2, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

        if len(good_matches) > 10:
            print("Template found")
        else:
            print("Template not found")
            
        cv2.imshow('Result', img_matches)
        cv2.waitKey(0)