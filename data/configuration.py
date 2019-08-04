# from keras import layers
# from keras.layers import Input, Dense, Activation,BatchNormalization
# from keras.layers import Dropout
# from keras.models import Model, load_model
# from keras.utils import layer_utils
# from keras.utils.data_utils import get_file
# from keras.utils.vis_utils import model_to_dot
# from keras.utils import plot_model
# import keras.backend as K
# import matplotlib.pyplot as plt
# from keras.callbacks import TensorBoard

# netModel = load_model("diseasespreadmodel.h5")
# Map Parameters:
SCALE_FACTOR = 1
MAP_MIN_X = 0
MAP_MIN_Y = 0
MAP_MAX_X = 1000
MAP_MAX_Y = 1000

MAP_BUILDINGS_COUNT = round(1000 * SCALE_FACTOR) 
MAP_ROADS_COUNT     = max(2, round(20   * SCALE_FACTOR)) * 5

INFECTED_AT_START = 0.002 
INFECTION_SPREAD  = 0.001
INFECTION_PERIOD  =  24 * 5

FAMILIES    = round(2000 * SCALE_FACTOR) 
VEHICLES    = round(175 * SCALE_FACTOR) 

# particlesimulationfile = 'out.log'
