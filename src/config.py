"""
  @file config.py
  @authors BEZIAUD Jordan LEBARON Maëlie ROSSIGNOL Vincent
  @brief declaration of variables and data structures as global configuration for the neural network
  @version 0.1
  @date 2021-12-08

  @copyright Copyright (c) 2021
"""

import numpy as np

DEBUG = True
MODEL_TYPE = "sequential"  # "sequential", "hybrid", "conv", "squeeze_net"

# --------------------- SAVING ----------------- #

SAVE_FLAG = False
OUTPUT_DIR = "./models"
OUTPUT_NAME = "model_extended"

# --------------------- DATASETS ----------------- #

DATASET_PATH = "./data/dataset_extended.txt"
DATASET_TRAIN_SIZE = 1200
DATASET_TEST_SIZE = 300
DATASET_SIZE = DATASET_TRAIN_SIZE + DATASET_TEST_SIZE
THERMAL_FRAME_DIM = 32

# --------------------- HYPER-PARAMETERS ----------------- #

DEFAULT_PARAMETERS = {
    "INIT_LEARNING_RATE": 0.012,
    "OPTIMIZER": "adam",
    "EPOCHS": 200,
    "BATCH_SIZE": 100,
    "ACTIVATION_FUNCTION": "relu",
    "N_HIDDEN_LAYERS_NEURONS": 80,
    "N_HIDDEN_LAYERS": 2,
    "DROPOUT_PERCENTAGE": 0.1,
    "L2_REGULARIZATION": 1e-4,
}

PREDICTION_THRESHOLD = 0.5
NUM_OF_BATCH = DATASET_TRAIN_SIZE / DEFAULT_PARAMETERS["BATCH_SIZE"]

# CNN PARAMETERS

N_FILTER_CONV_LAYER_1 = 64
N_FILTER_CONV_LAYER_2 = 80
CONV_FILTER_SIZE = 3

# RANGE FOR PARAMETERS TUNING

VALIDATION_RANGES_PARAMETERS = {
    "INIT_LEARNING_RATE": np.linspace(0.01, 0.5, 20),
    "OPTIMIZER": ["adam", "adagrad"],
    "EPOCHS": range(10, 50),
    "BATCH_SIZE": range(40, 120, 10),
    "ACTIVATION_FUNCTION": ["sigmoid", "elu", "relu", "selu", "tanh"],
    "N_HIDDEN_LAYERS_NEURONS": range(60, 90, 5),
    "N_HIDDEN_LAYERS": range(2, 6),
    "DROPOUT_PERCENTAGE": np.linspace(0.2, 0.8, 20),
}

MAX_TRIAL_TUNER = 10

# --------------------- FEATURES ----------------- #

NUM_OF_FEATURES = THERMAL_FRAME_DIM * THERMAL_FRAME_DIM  # input values (nb input)
OUTPUT_SIZE = 1  # output classes

# --------------------- FEATURES ----------------- #

DEFAULT_PARAMETERS_SMALL = {
    "INIT_LEARNING_RATE": 0.012,
    "OPTIMIZER": "adam",
    "EPOCHS": 200,
    "BATCH_SIZE": 10,
    "ACTIVATION_FUNCTION": "relu",
    "N_HIDDEN_LAYERS_NEURONS": 80,
    "N_HIDDEN_LAYERS": 2,
    "DROPOUT_PERCENTAGE": 0.2,
    "L2_REGULARIZATION": 1e-3,
}
# train_size = 600 and test_size = 154

DEFAULT_PARAMETERS_EXTENDED = {
    "INIT_LEARNING_RATE": 0.012,
    "OPTIMIZER": "adam",
    "EPOCHS": 200,
    "BATCH_SIZE": 100,
    "ACTIVATION_FUNCTION": "relu",
    "N_HIDDEN_LAYERS_NEURONS": 80,
    "N_HIDDEN_LAYERS": 2,
    "DROPOUT_PERCENTAGE": 0.1,
    "L2_REGULARIZATION": 1e-4,
}

# train_size = 1200 and test_size = 300
