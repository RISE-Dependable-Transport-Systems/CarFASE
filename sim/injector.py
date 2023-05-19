import glob
import os
import cv2
import numpy as np
from datetime import datetime, date, time
import carla
import argparse
import xml.etree.ElementTree as ET
from PIL import Image, ImageEnhance, ImageOps
import re
from auto_run import Ex_data

# print('Numpy version is= ', np.__version__)
root = ET.parse('experiment_data.xml').getroot()
X = root.find('data')
noise_type = str(root.find("noise_type").text)
start_time = float(root.find("start_time").text)
end_time = float(root.find("end_time").text)
brightness_factor = float(root.find("b_factor").text)
experiment_nr = int(root.find("ex_nr").text)
print('timeeeeeeeeeeeeeeee=', noise_type, start_time, end_time)
# importing module
from datetime import datetime
import logging
# Create and configure logger
logging.basicConfig(filename="campaign_data/Ex_{}_Sensor_data_{}.log".format(experiment_nr, datetime.now()),
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
def log_sensor_data(data):
  logger.info(str(data))

def current_time():
  # Current Time
  now = datetime.now()
  Current_time = now.strftime("%Y-%m-%d %H.%M.%S")
  return Current_time
# *********************************************************
##                RGB Camera Fault models                ##
# *********************************************************
noise_typ = noise_type
from numba import jit, cuda
@jit(target_backend ="cuda")
def rgb_fa(time, image):
  if time >= start_time and time <= end_time:
    if noise_typ == "s_p":
      row, col, ch = image.shape
      s_vs_p = 0.5
      amount = 0.004
      out = np.copy(image)
      # Salt mode
      num_salt = np.ceil(amount * image.size * s_vs_p)
      coords = [np.random.randint(0, i - 1, int(num_salt))
                for i in image.shape]
      out[coords] = 1
      # Pepper mode
      num_pepper = np.ceil(amount * image.size * (1. - s_vs_p))
      coords = [np.random.randint(0, i - 1, int(num_pepper))
                for i in image.shape]
      out[coords] = 0
      # cv2.imwrite('noisy_img/sp_noise_out.jpg', out)
      return out.astype('uint8')
    elif noise_typ == "brightness":
      image= Image.fromarray(image)  # RGB image
      # print('-----------------------------------------------', image.mode, image.size)
      enhancer = ImageEnhance.Brightness(image)
      # An enhancement factor of 0.0 gives a black image. A factor of 1.0 gives the original image.
      factor = brightness_factor #3.5
      noisy = enhancer.enhance(factor)
      return noisy #.astype('uint8')

    else:
      return image
  else:
    return image
