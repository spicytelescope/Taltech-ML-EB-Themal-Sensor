from config import *
from data_helpers import *
from init_model import *
from tune_parameters import *
import matplotlib.pyplot as plt

if __name__ == "__main__":

    # --------------------------- DATA LOADING & PREPROCESSING --------------------------- #

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

    if MODEL_TYPE in ["hybrid", "conv"]:
        train_x = train_x.reshape(
            train_x.shape[0], THERMAL_FRAME_DIM, THERMAL_FRAME_DIM, 1
        ).astype(np.float32)
        test_x = test_x.reshape(
            test_x.shape[0], THERMAL_FRAME_DIM, THERMAL_FRAME_DIM, 1
        ).astype(np.float32)

    if DEBUG:
        print("[DATA LOADING & PREPROCESSING] Done ! Proceeding to training phase ...")

    # --------------------------- MODEL (NN) BUILDING --------------------------- #

    model: tf.keras.models.Sequential = init_model(variant=MODEL_TYPE)

    print("=============== TRAINING PHASE ===============")

    history = model.fit(
        train_x,
        train_y,
        epochs=DEFAULT_PARAMETERS["EPOCHS"],
        batch_size=DEFAULT_PARAMETERS["BATCH_SIZE"],
    )

    # Ploting

    fig, ax = plt.subplots()
    ax.plot(history.history["accuracy"], color="blue")
    ax.set_xlabel("Epochs")
    ax.set_ylabel("accuracy", color="blue", fontsize=14)

    ax2 = ax.twinx()
    ax2.plot(history.history["loss"], color="red")
    ax2.set_ylabel("cost", color="red", fontsize=14)

    # plt.legend(["Accuracy","Cost"], loc=1)
    plt.title(
        f"Evolution of the cost and accuracy in regars to the epochs, \nDATASET_SIZE={DATASET_SIZE}, learning_rate={DEFAULT_PARAMETERS['INIT_LEARNING_RATE']}, EPOCH={DEFAULT_PARAMETERS['EPOCHS']}"
    )

    if DEBUG:
        print(
            "[+] You can find the cost evolution graph in ./src/cost_helpers/results\n"
        )

    plt.savefig("./src/cost_helpers/results/cost_plot.png")

    print("=============== TESTING PHASE ===============")

    model.evaluate(test_x, test_y, verbose=2)

    if SAVE_FLAG:
        model.save(f"{OUTPUT_DIR}/{OUTPUT_NAME}")

        print("[ MODEL SAVING ] Successfully saved the model to ./output_model !")

        # Convert the model.
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        tflite_model = converter.convert()

        # Save the model.
        with open(f"{OUTPUT_DIR}/{OUTPUT_NAME}.tflite", "wb") as f:
            f.write(tflite_model)

        print(
            "[ MODEL SAVING ] Successfully converted model to tensorflow lite format !"
        )
