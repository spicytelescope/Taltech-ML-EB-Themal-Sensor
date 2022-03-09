# Demo purposes

import os
import sys
from typing import List

import numpy as np

from data_helpers import *

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import tensorflow as tf

# Printing formatting
OKGREEN: str = "\033[92m"
FAIL: str = "\033[91m"
ENDC: str = "\033[0m"

if len(sys.argv) != 3:
    exit(
        "Error : missing argument, arg list :\n-> demo dataset input path\n-> saved model location"
    )
else:
    DATASET_INPUT_PATH: str = sys.argv[1]
    SAVED_MODEL_PATH: str = sys.argv[2]

THERMAL_FRAME_DIM: int = 32
DEMO_DATASET_SIZE: int = 8

# Loading the dataset

print("[*] Loading demo dataset ...")

raw_thermal_data: List[List[List[float]]] = np.zeros(
    shape=(DEMO_DATASET_SIZE, THERMAL_FRAME_DIM, THERMAL_FRAME_DIM)
)
thermal_data_x: List[List[List[float]]] = np.zeros(
    shape=(DEMO_DATASET_SIZE, THERMAL_FRAME_DIM, THERMAL_FRAME_DIM)
)
load_data(DATASET_INPUT_PATH, DEMO_DATASET_SIZE, raw_thermal_data, "data")
normalize_dataset(raw_thermal_data, thermal_data_x)

print("[+] Successfully loaded demo dataset! ")

# Loading model

print("[*] Loading demo dataset ...")

model = tf.keras.models.load_model(SAVED_MODEL_PATH)

print("[+] Successfully loaded model !")

# Predictions

predictions = model.predict(thermal_data_x)
for i, pred in enumerate([p[0] for p in predictions]):
    if pred < 0:
        print(
            f"{FAIL}Prediction {i+1} - There is no human form in the thermal frame ! [pred_value = {pred}]{ENDC}"
        )
    else:
        print(
            f"{OKGREEN}Prediction {i+1} - Human form detected ! [pred_value = {pred}]{ENDC}"
        )
