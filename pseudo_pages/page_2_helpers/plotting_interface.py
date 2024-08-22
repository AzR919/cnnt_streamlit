

import streamlit as st

from utils.utils import *
from .plotting_options import *
from pseudo_pages.page_1_helpers import running_inference

from inputs.input_class import Input_Class
from model.model_class import Model_Class
from outputs.output_class import Output_Class

ic : Input_Class = st.session_state.input_class
mc : Model_Class = st.session_state.model_class
oc : Output_Class = st.session_state.output_class

sst = st.session_state

def plotting_st():

    st.write("Image Plots")

    plot_ind = index_slider(ic.get_num_images())

    plot_image(plot_ind)

def index_slider(num_images):

    max_value = num_images-1 if not num_images == 1 else 1
    return st.slider("Index of Image to plot", min_value=0, max_value=max_value, disabled=num_images==1)


def plot_image(idx):
    # Given index, plot the pair of noisy, pred, and clean images

    name = ic.noisy_im_names[idx]

    noisy_im = ic.noisy_im_list[idx]
    clean_im = ic.clean_im_list[idx] if ic.clean_im_list is not None else None
    
    predi_image = ic.predi_im_list[idx]
    
    if predi_image is None:
        predi_image = running_inference(mc.model, 
                                            [ic.noisy_im_list[idx]], 
                                            sst.args.cutout,
                                            sst.args.overlap,
                                            sst.args.device)[0]
        
        ic.set_predi_im_idx(predi_image, idx)

    plot_three(name, noisy_im, predi_image, clean_im)