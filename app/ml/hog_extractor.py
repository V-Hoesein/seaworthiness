import cv2
from skimage.feature import hog
import numpy as np

class HOGFeatureExtractor:
    def __init__(self, target_size=(128, 128)):
        self.target_size = target_size

    def extract_features(self, image_path):
        """
        Membaca gambar, meresize, mengubah ke grayscale, dan mengekstrak fitur HOG.
        """
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Tidak dapat membaca gambar di path: {image_path}")

        # Resize image
        resized_image = cv2.resize(image, self.target_size)

        # Convert to grayscale
        gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

        # Extract HOG features
        features = hog(gray_image, orientations=9, pixels_per_cell=(8, 8),
                       cells_per_block=(2, 2), block_norm='L2-Hys', visualize=False)
        
        return features
