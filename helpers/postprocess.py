#
# Stephen Vondenstein, Matthew Buckley
# 10/09/2018
#
import tensorflow as tf
import cv2
import os
import numpy as np

def process(image, name, config):
    for i in range(image[0].shape[0]):
        img = np.reshape(np.argmax(image[0], axis=3), (image[0].shape[0],128,128))
        print(img.shape)
        cv2.imwrite(os.path.join(config.prediction_path, name[i].decode('utf-8')), 255 * img[i, :, :])