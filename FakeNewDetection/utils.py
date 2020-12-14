import os
import numpy as np 
import random

import seaborn as sns
import matplotlib.pyplot as plt

import tensorflow as tf

def seed_all(seed=1512):
    np.random.seed(seed)
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    tf.random.set_seed(seed)