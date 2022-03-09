# taltech-ML-EB-final-project

## Content

This project implement a neural network trained using `tensorflow` library with python `3.8.10`. It is adapted to thermal sensor, with the aim to detect when a human being is in front of the captor.

This neural network should be able to run on a STM32F4 board.

## Installation

Run the `setup` script to install the dependencies for this project :

    ./setup

## Testing the project

The project can be tested by running the demo script from the root directory :

    ./demo

It will get all the raw data from the `data/demo_dataset.txt` input file and make a prediction wether there is a human shape
in them or not and print the result in the terminal. For validation purpose, all the specified thermal frames will be displayed as pictures (heatmap) into the `data/demo_heatmaps` dir.
## Usage

### Training a model

You can train a model to detect human shapes from thermal sensor data if the data is formatted as the files presents in the `data` directory.

Just `cd` into the `src` directory and run the `train_model` using `python > 3.8`.

### Changing the settings (input dataset, hyper-parameters)

The model is fully customizable by changing the lines in the `config.py` file !
Suit yourself.

Also, you can automatically tune the hyper-parameters by running the `tune_parameters.py` file.# Taltech-ML-EB-Themal-Sensor
