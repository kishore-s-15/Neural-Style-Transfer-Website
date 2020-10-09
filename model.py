# Importing the required libraries
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import PIL
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

def load_image(path_to_image):
    """
    Function which loads an image and limits its maximum dimension to 512 pixels
    """

    max_dim = 512

    image = tf.io.read_file(path_to_image)
    image = tf.image.decode_image(image, channels=3)
    image = tf.image.convert_image_dtype(image, tf.float32)

    shape = tf.cast(tf.shape(image)[:-1], tf.float32)
    long_dim = max(shape)
    scale = max_dim / long_dim

    new_shape = tf.cast(shape * scale, tf.int32)

    image = tf.image.resize(image, new_shape)
    image = image[tf.newaxis, :]

    return image

def tensor_to_image(tensor):
    """
    Function which converts tensor to image
    """

    tensor = tensor * 255
    tensor = np.array(tensor, dtype=np.uint8)

    if np.ndim(tensor) > 3:
        assert tensor.shape[0] == 1, "There are more than one image is present in the given input"
        tensor = tensor[0]

    return PIL.Image.fromarray(tensor)

def NST(content_img_path, style_img_path):
    """
    Function which transfers the style from style image to content image
    """

    content_image = load_image(content_img_path)
    style_image = load_image(style_img_path)

    # Neural Style Transfer using Tensorflow Hub Model
    hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

    stylized_image = hub_model(tf.constant(content_image), tf.constant(style_image))[0]

    stylized_image = tensor_to_image(stylized_image)

    return stylized_image