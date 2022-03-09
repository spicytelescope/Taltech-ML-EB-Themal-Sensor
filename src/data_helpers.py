"""
@file data.py
@author BEZIAUD Jordan LEBARON Maëlie ROSSIGNOL Vincent
@brief functions to convert & preprocess a dataset to data structures, in order to manage the data for training the neural network
@version 0.1
@date 2021-12-07

@copyright Copyright (c) 2021
"""


import json
from typing import List, Union

import numpy as np

from config import *


# --------------------------- DATA LOADING --------------------------- #


def load_data(
    dataset_path: str,
    dataset_size: int,
    dataset_matrix: Union[List[List[List[float]]], List[int]],
    field: str,
) -> None:
    """read an input file from the dataset dir and write all its data to an output matrix

    Args:
        dataset_path (str): path to the input file
        dataset_size (int): number of lines read, if set to -1 then read the entier input file
        dataset_matrix (List[List[List[float]]] | List[int]): matrix containing the values that will be read from the input file
        field (str): field of the json data that needs to be stored in the raw output matrix
    """

    if dataset_size == -1:
        with open(dataset_path, "r") as f:
            dataset_size = len(f.readlines())

    # Loading the dataset
    with open(dataset_path, "r") as f:

        if DEBUG:
            print(
                f"[ LOADING DATA ] Creating dataset ... [size={dataset_size}, src={dataset_path}]"
            )

        for line_ind in range(dataset_size):
            raw_line: str = f.readline()

            # Fetching data from the raw input file
            parsed_json: dict = json.loads(raw_line)
            thermal_data: List[List[float]] or str = np.array(parsed_json[field])

            if field == "data":

                # Parsing the matrix of temperature and creating the dataset
                dataset_matrix[line_ind] = thermal_data

            elif field == "label":

                # Storing each label in the matrix
                dataset_matrix[line_ind] = int(parsed_json[field])


def create_datasets(
    dataset: Union[List[List[List[float]]], List[int]],
    train_dataset: Union[List[List[List[float]]], List[int]],
    test_dataset: Union[List[List[List[float]]], List[int]],
) -> None:
    """split the dataset according to macros to 2 output matrix (train & test dataset)

    Args:
        dataset (List[List[List[float]]] | List[int]): input matrix representing the dataset
        COL (int): number of columns in all the matrices concerned
        train_dataset (List[List[List[float]]] | List[int]): output matrix that will contain the train dataset
        test_dataset (List[List[List[float]]] | List[int]): output matrix that will contain the test dataset
    """

    if DEBUG:
        print(
            "[ LOADING DATA ] Creating train & test subsets by splitting the main dataset ..."
        )

    for i in range(DATASET_SIZE):

        if i < DATASET_TRAIN_SIZE:
            if len(dataset.shape) > 1:
                for j in range(dataset.shape[1]):
                    train_dataset[i][j] = dataset[i][j]
            else:
                train_dataset[i] = dataset[i]
        else:
            if len(dataset.shape) > 1:
                for j in range(dataset.shape[1]):
                    test_dataset[i - DATASET_TRAIN_SIZE][j] = dataset[i][j]
            else:
                test_dataset[i - DATASET_TRAIN_SIZE] = dataset[i]


# --------------------------- DATA PREPROCESSING --------------------------- #


def normalize_dataset(
    input_dataset: List[List[List[float]]],
    normalized_dataset: List[List[List[float]]],
) -> None:
    """normalize a dataset with mean centering

    Args:
        input_dataset (List[List[List[float]]]): the raw dataset
        normalized_dataset (List[List[List[float]]]): the output e.g. normalized dataset
    """

    if DEBUG:
        print("[ PREPROCESSING DATA ] Normalizing dataset ...")

    feature_extremums: List[float] = [
        (np.min(input_dataset[:, i]), np.max(input_dataset[:, i]))
        for i in range(input_dataset.shape[1])
    ]

    for i in range(input_dataset.shape[0]):
        for j in range(input_dataset.shape[1]):
            normalized_dataset[i][j] = (
                input_dataset[i][j] - feature_extremums[j][0]
            ) / (feature_extremums[j][1] - feature_extremums[j][0])


# Tests

if __name__ == "__main__":

    raw_dataset: List[List[List[float]]] = np.zeros(
        shape=(DATASET_SIZE, THERMAL_FRAME_DIM, THERMAL_FRAME_DIM)
    )
    raw_train_x: List[List[List[float]]] = np.zeros(
        shape=(DATASET_TRAIN_SIZE, THERMAL_FRAME_DIM, THERMAL_FRAME_DIM)
    )
    raw_test_x: List[List[List[float]]] = np.zeros(
        shape=(DATASET_TEST_SIZE, THERMAL_FRAME_DIM, THERMAL_FRAME_DIM)
    )
    train_x: List[List[List[float]]] = np.zeros(
        shape=(DATASET_TRAIN_SIZE, THERMAL_FRAME_DIM, THERMAL_FRAME_DIM)
    )

    load_data(DATASET_PATH, DATASET_SIZE, raw_dataset, "data")
    create_datasets(raw_dataset, raw_train_x, raw_test_x)
    normalize_dataset(raw_train_x, train_x)

    raw_labels: List[int] = np.zeros(shape=(DATASET_SIZE,), dtype=np.int32)
    load_data(DATASET_PATH, DATASET_SIZE, raw_labels, "label")
    print(raw_labels)
