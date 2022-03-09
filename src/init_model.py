import tensorflow as tf
from config import *
from keras import backend as K


def init_model(variant: str = "sequential") -> tf.keras.models.Sequential:
    """initlialize and return a keras sequential model according to the configuration created in the config.py

    Args:
        variant (str, optional): architecture of the model, can be either "sequential", "hybrid", "conv" or "squeeze_net". Defaults to "sequential".

    Returns:
        tf.keras.models.Sequential: model created from the hyperparameter set in the config file
    """

    if variant == "sequential":
        # default sequential model

        model = tf.keras.models.Sequential()
        model.add(
            tf.keras.layers.Flatten(input_shape=(THERMAL_FRAME_DIM, THERMAL_FRAME_DIM))
        )

        # Adding hidden layers
        for _ in range(DEFAULT_PARAMETERS["N_HIDDEN_LAYERS"]):
            model.add(
                tf.keras.layers.Dense(
                    DEFAULT_PARAMETERS["N_HIDDEN_LAYERS_NEURONS"],
                    activation=DEFAULT_PARAMETERS["ACTIVATION_FUNCTION"],
                    kernel_regularizer=tf.keras.regularizers.l2(
                        l2=DEFAULT_PARAMETERS["L2_REGULARIZATION"]
                    ),
                )
            )

        # Adding final dropout and output layer
        model.add(tf.keras.layers.Dropout(DEFAULT_PARAMETERS["DROPOUT_PERCENTAGE"]))
        model.add(tf.keras.layers.Dense(OUTPUT_SIZE))

    elif variant == "hybrid":

        # model with convolutionnal layers on top of the default sequential model
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Conv2D(N_FILTER_CONV_LAYER_1, (CONV_FILTER_SIZE,CONV_FILTER_SIZE), activation="relu",input_shape=(THERMAL_FRAME_DIM,THERMAL_FRAME_DIM,1) ,strides=(2,2),padding='valid'))
        model.add(tf.keras.layers.Conv2D(N_FILTER_CONV_LAYER_2, (CONV_FILTER_SIZE,CONV_FILTER_SIZE), activation="relu",input_shape=(THERMAL_FRAME_DIM,THERMAL_FRAME_DIM,1) ,strides=(2,2),padding='valid'))
        model.add(tf.keras.layers.Flatten(input_shape=(28, 28)))
        for _ in range(DEFAULT_PARAMETERS["N_HIDDEN_LAYERS"]):
            model.add(
                tf.keras.layers.Dense(
                    DEFAULT_PARAMETERS["N_HIDDEN_LAYERS_NEURONS"],
                    activation=DEFAULT_PARAMETERS["ACTIVATION_FUNCTION"],
                    kernel_regularizer=tf.keras.regularizers.l2(
                        l2=DEFAULT_PARAMETERS["L2_REGULARIZATION"]
                    ),
                )
            )
        model.add(tf.keras.layers.Dropout(DEFAULT_PARAMETERS["DROPOUT_PERCENTAGE"]))
        model.add(tf.keras.layers.Dense(OUTPUT_SIZE))

    elif variant == "conv":

        model = tf.keras.models.Sequential()
        model.add(
            tf.keras.layers.Conv2D(
                32,
                kernel_size=(3, 3),
                activation=DEFAULT_PARAMETERS["ACTIVATION_FUNCTION"],
                input_shape=(THERMAL_FRAME_DIM, THERMAL_FRAME_DIM, 1),
            )
        )
        model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
        model.add(
            tf.keras.layers.Conv2D(
                64,
                kernel_size=(3, 3),
                activation=DEFAULT_PARAMETERS["ACTIVATION_FUNCTION"],
            )
        )
        model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
        model.add(tf.keras.layers.Flatten(input_shape=(THERMAL_FRAME_DIM, THERMAL_FRAME_DIM)))
        model.add(
            tf.keras.layers.Dense(
                256, activation=DEFAULT_PARAMETERS["ACTIVATION_FUNCTION"]
            )
        )
        model.add(
            tf.keras.layers.Dense(
                128, activation=DEFAULT_PARAMETERS["ACTIVATION_FUNCTION"]
            )
        )
        model.add(tf.keras.layers.Dense(OUTPUT_SIZE, activation="softmax"))

    elif variant == "squeeze_net":

        def fire_module(x, s1, e1, e3):
            s1x = tf.keras.layers.Conv2D(s1, kernel_size=1, padding="same")(x)
            s1x = tf.keras.layers.ReLU()(s1x)
            e1x = tf.keras.layers.Conv2D(e1, kernel_size=1, padding="same")(s1x)
            e3x = tf.keras.layers.Conv2D(e3, kernel_size=3, padding="same")(s1x)
            x = tf.keras.layers.concatenate([e1x, e3x])
            x = tf.keras.layers.ReLU()(x)
            return x

        def SqueezeNet(nclasses, input_shape=(224, 224, 3)):
            input = tf.keras.Input(input_shape)
            x = tf.keras.layers.Conv2D(
                96, kernel_size=(7, 7), strides=(2, 2), padding="same"
            )(input)
            x = tf.keras.layers.MaxPool2D(pool_size=(3, 3), strides=(2, 2))(x)
            x = fire_module(x, s1=16, e1=64, e3=64)  # 2
            x = fire_module(x, s1=16, e1=64, e3=64)  # 3
            x = fire_module(x, s1=32, e1=128, e3=128)  # 4
            x = tf.keras.layers.MaxPool2D(pool_size=(3, 3), strides=(2, 2))(x)
            x = fire_module(x, s1=32, e1=128, e3=128)  # 5
            x = fire_module(x, s1=48, e1=192, e3=192)  # 6
            x = fire_module(x, s1=48, e1=192, e3=192)  # 7
            x = fire_module(x, s1=64, e1=256, e3=256)  # 8
            x = tf.keras.layers.MaxPool2D(pool_size=(3, 3), strides=(2, 2))(x)
            x = fire_module(x, s1=64, e1=256, e3=256)  # 9
            x = tf.keras.layers.Dropout(0.5)(x)
            x = tf.keras.layers.Conv2D(nclasses, kernel_size=1)(x)
            output = tf.keras.layers.AvgPool2D(pool_size=(13, 13))(x)
            model = tf.keras.Model(input, output)

            return model

        return SqueezeNet(10)

    # Compiling the model with the loss function associated
    loss_fn = tf.keras.losses.BinaryCrossentropy(
        from_logits=True if MODEL_TYPE == "sequential" else False
    )
    model.compile(
        optimizer=DEFAULT_PARAMETERS["OPTIMIZER"],
        loss=loss_fn,
        metrics=["accuracy"],
    )
    K.set_value(model.optimizer.learning_rate, DEFAULT_PARAMETERS["INIT_LEARNING_RATE"])

    if DEBUG:
        model.summary()

    return model


if __name__ == "__main__":

    model = init_model()
