# -*- coding: utf-8 -*-

!pip install kornia kornia_moons

import numpy as np
import cv2
import kornia.feature as KF
import torch
from kornia_moons.viz import draw_LAF_matches
import kornia as K

"""For the task of feature matching (in satellite images) we will use pretrined LoFTR model with parameter "outdoor"
"""

class FeatureMatcher:
    def __init__(self):
        self.loftr = KF.LoFTR(pretrained='outdoor').eval() #creating model

    #normalize data to avoid mistakes
    def normalize_image(self, image):
        normalized_image = cv2.normalize(image, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        return normalized_image
    #LoFTR model works with tensors
    def match_features(self, image1, image2):
      image1 = torch.from_numpy(image1).float().unsqueeze(0).permute(0, 3, 1, 2) / 255.0
      image2 = torch.from_numpy(image2).float().unsqueeze(0).permute(0, 3, 1, 2) / 255.0
    #LoFTR model works with gray images only
      if image1.shape[1] == 3:
        image1 = K.color.rgb_to_grayscale(image1)
      if image2.shape[1] == 3:
        image2 = K.color.rgb_to_grayscale(image2)
    #looking for matches
      with torch.inference_mode():
        input_dict = {"image0": image1, "image1": image2}
        correspondences = self.loftr(input_dict)
      keypoints0 = correspondences["keypoints0"].numpy()
      keypoints1 = correspondences["keypoints1"].numpy()
      Fm, inliers = cv2.findFundamentalMat(keypoints0, keypoints1, cv2.USAC_MAGSAC, 0.5, 0.999, 100000) #classify inliers and outliers
      inliers = inliers > 0 #getting inliers only (inliers have value of 1 whereas outliers - 0)
      return keypoints0, keypoints1, inliers, image1, image2
    #function to draw mathes
    def draw_matches(self, image1, image2, max_matches=None): #max_matches is the parameter to regulate the number of matches drawn
        image1 = self.normalize_image(image1) #normalization
        image2 = self.normalize_image(image2) #normalization

        keypoints0, keypoints1, inliers, _, _ = self.match_features(image1, image2) #getting matches

        # Subset the matches if max_matches is specified
        if max_matches is not None:
            indices = np.arange(len(keypoints0))
            np.random.shuffle(indices)
            indices = indices[:max_matches]
            keypoints0 = keypoints0[indices]
            keypoints1 = keypoints1[indices]
            inliers = inliers[indices]

        # Ensure images are in RGB for consistent drawing
        if len(image1.shape) == 2:  # Grayscale to RGB
            image1 = cv2.cvtColor(image1, cv2.COLOR_GRAY2RGB)
            image2 = cv2.cvtColor(image2, cv2.COLOR_GRAY2RGB)
        #drawing
        matched_image = draw_LAF_matches(
            KF.laf_from_center_scale_ori(
                torch.from_numpy(keypoints0).view(1, -1, 2),
                torch.ones(keypoints0.shape[0]).view(1, -1, 1, 1),
                torch.ones(keypoints0.shape[0]).view(1, -1, 1),
            ),
            KF.laf_from_center_scale_ori(
                torch.from_numpy(keypoints1).view(1, -1, 2),
                torch.ones(keypoints1.shape[0]).view(1, -1, 1, 1),
                torch.ones(keypoints1.shape[0]).view(1, -1, 1),
            ),
            torch.arange(keypoints0.shape[0]).view(-1, 1).repeat(1, 2),
            image1,
            image2,
            inliers,
            draw_dict={
                'inlier_color': (0.2, 1, 0.2),
                'tentative_color': (1, 0.1, 0.1),
                'feature_color': (0.2, 0.5, 1),
                'vertical': False,
            },
        )
        return matched_image #returns an image with drawn matches
