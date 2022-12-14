"""
File for the input class

Holds the given image and attributes related to it:
- name
- scale
- cutouts

Supports only 3D input (for now)

TODO: Support nD images (n=3,4,5)
"""

import random

from inputs.inputs_variations import read_inputs
from inputs.inputs_variations import set_image


class Inputs_Class():
    """
    Class for holding the inputs given and provides access to them

    Hold the following variables:
        - noisy_im_names: the names of the noisy images given
        - noisy_im_list: the given noisy images. each noisy image is a 3D numpy array
        - cutouts: the cutout shape for each image
        - scale: that value to scale images with

    Allows access to indvidual images and names.
    Provides cut numpy list of inference as well.
    """

    def __init__(self):
        # Init with empties

        self.noisy_im_list = []
        self.noisy_im_names = []
        self.cutouts = []
        self.scale = 1

    def read_inputs_files(self, input_list_raw):
        # Read using the one function

        self.noisy_im_names, self.noisy_im_list = read_inputs(input_list_raw)

    def set_cutouts(self, cutout_shape):
        # set cutouts for each image

        def get_cut(type, ind):

            shape = self.get_noisy_im_shape(ind)

            if type == "complete":
                return "complete"

            if type == "random":

                t1 = random.randint(0, shape[0]//2)
                t2 = random.randint(t1+4, shape[0])
                
                h1 = random.randint(0, shape[1]//2)
                h2 = random.randint(h1+64, shape[1])
                
                w1 = random.randint(0, shape[2]//2)
                w2 = random.randint(w1+64, shape[2])

                return (t1, t2, h1, h2, w1, w2)

            # if given then use that cutout
            return cutout_shape

        self.cutouts = [get_cut(cutout_shape, i) for i in range(self.get_num_images())]

    def set_format(self, format_a, format_d):
        # Save formats for later use

        self.format_a = format_a # axis order (THW, HWT, etc)
        self.format_d = format_d # data type (8-bit, 16-bit, etc)

    def get_format(self):
        # Retrieve format

        return self.format_a, self.format_d

    def get_num_images(self):
        # Total number of images
        
        return len(self.noisy_im_list)
    
    def get_noisy_im(self, ind):
        # Retrieve specific noisy image

        return self.noisy_im_list[ind]

    def get_noisy_im_name(self, ind):
        # Retrieve specific noisy image name

        return self.noisy_im_names[ind]

    def get_noisy_im_names(self):
        # Retrieve all  noisy image names

        return self.noisy_im_names
    
    def get_noisy_im_shape(self, ind):
        # Retrieve specific noisy image shape

        return self.noisy_im_list[ind].shape

    def get_cutout(self, ind):
        # Retrieve specific image cutout

        return self.cutouts[ind]

    def get_cut_np_images(self):
        # Retrieve cut np images ready for inference
        # Scaled and with axis set as THW

        def make_cut(image, c):

            if c=="complete":
                return image

            return image[c[0]:c[1], c[2]:c[3], c[4]:c[5]]

        return [make_cut(set_image(x, self.format_a, self.format_d), y)
                 for x, y in zip(self.noisy_im_list, self.cutouts)]

