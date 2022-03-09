import keras_tuner as kt
from config import *
from init_model import *
from data_helpers import *


def tune_parameters(
    train_x: List[List[List[float]]],
    train_y: List[int],
    test_x: List[List[List[float]]],
    test_y: List[int],
) -> None:
    """use the keras_tuner package to find the best hyper-parameters for a model created from the init_model function

    Args:
        train_x (List[List[List[float]]]): matrix containing the training data
        train_y (List[int]): matrix containing the training labels
        test_x (List[List[List[float]]]): matrix containing the validation data
        test_y (List[int]): matrix containing the validation label
    """

    tuner: kt.RandomSearch = kt.RandomSearch(
        lambda _: init_model(variant=MODEL_TYPE),
        objective="val_loss",
        max_trials=MAX_TRIAL_TUNER,
        project_name="parameter_search_results",
    )

    tuner.search(
        train_x,
        train_y,
        epochs=DEFAULT_PARAMETERS["EPOCHS"],
        validation_data=(test_x, test_y),
    )

    if DEBUG:
        tuner.results_summary()
        print("\n\nBest model from tuner search : \n\n")
        tuner.get_best_models()[0].summary()

    return tuner.get_best_models()[0]


if __name__ == "__main__":

    raw_dataset_x: List[List[List[float]]] = np.zeros(
        shape=(DATASET_SIZE, THERMAL_FRAME_DIM, THERMAL_FRAME_DIM)
    )
    raw_dataset_y: List[int] = np.zeros(shape=(DATASET_SIZE,), dtype=np.int32)

    # train set
    raw_train_x: List[List[List[float]]] = np.zeros(
        shape=(DATASET_TRAIN_SIZE, THERMAL_FRAME_DIM, THERMAL_FRAME_DIM)
    )
    train_x: List[List[List[float]]] = np.zeros(
        shape=(DATASET_TRAIN_SIZE, THERMAL_FRAME_DIM, THERMAL_FRAME_DIM)
    )
    train_y: List[int] = np.zeros(shape=(DATASET_TRAIN_SIZE,), dtype=np.int32)

    # test set
    raw_test_x: List[List[List[float]]] = np.zeros(
        shape=(DATASET_TEST_SIZE, THERMAL_FRAME_DIM, THERMAL_FRAME_DIM)
    )
    test_x: List[List[List[float]]] = np.zeros(
        shape=(DATASET_TEST_SIZE, THERMAL_FRAME_DIM, THERMAL_FRAME_DIM)
    )
    test_y: List[int] = np.zeros(shape=(DATASET_TEST_SIZE,), dtype=np.int32)

    # fetching data from input file

    load_data(DATASET_PATH, DATASET_SIZE, raw_dataset_x, "data")
    load_data(DATASET_PATH, DATASET_SIZE, raw_dataset_y, "label")
    create_datasets(raw_dataset_x, raw_train_x, raw_test_x)
    create_datasets(raw_dataset_y, train_y, test_y)

    # preprocessing data
    normalize_dataset(raw_train_x, train_x)
    normalize_dataset(raw_test_x, test_x)

    best_model = tune_parameters(train_x, train_y, test_x, test_y)
