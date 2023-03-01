import argparse
import cv2
import glob
import numpy as np
import os
import torch
from basicsr.utils import imwrite
import base64
from PIL import Image
from gfpgan import GFPGANer



def doer(file_path):


    print("Starting Doer")
    # ------------------------ set up background upsampler ------------------------

    bg_upsampler = None

    # ------------------------ set up GFPGAN restorer ------------------------

    arch = 'clean'
    channel_multiplier = 2
    model_name = 'GFPGANv1.3'
    print("Loading Path for gan")
    model_path = '/mysite/experiments/pretrained_models/GFPGANv1.3.pth'
    url = 'https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth'

    # model_path = os.path.join('experiments/pretrained_models', model_name + '.pth')
    # # if not os.path.isfile(model_path):
    # #     model_path = os.path.join('gfpgan/weights', model_name + '.pth')
    # if not os.path.isfile(model_path):
    #     # download pre-trained models from url
    #     model_path = url
    #     pass

    print(model_path)
    print(f"model path type: {type(model_path)}")

    restorer = GFPGANer(
        model_path=url,
        upscale=2,
        arch=arch,
        channel_multiplier=channel_multiplier,
        bg_upsampler=bg_upsampler)
    print(model_path)
    print(f"model path type: {type(model_path)}")
    if restorer:
        print("Something happened")
    else:
        print("Nothing happened")

    # ------------------------ restore ------------------------

        # read image
    # img_name = os.path.basename(file_path)
    # print(f'Processing {img_name} ...')
    # basename, ext = os.path.splitext(img_name)
    # input_img = cv2.imread(file_path, cv2.IMREAD_COLOR)
    input_img = file_path
    #print(input_img)
    # restore faces and background if necessary
    cropped_faces, restored_faces, restored_img = restorer.enhance(
        input_img,
        has_aligned=False,
        only_center_face=False,
        paste_back=True,
        weight=0.1)

    img_str = cv2.imencode('.png', restored_img)[1].tostring()
    img_b64 = base64.b64encode(img_str).decode('utf-8')
    #imwrite(restored_img,os.path.join('./', 'resty', f'{basename}_resty.png'))
    return img_b64




