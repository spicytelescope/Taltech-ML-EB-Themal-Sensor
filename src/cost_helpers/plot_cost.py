import matplotlib.pyplot as plt

data: list = []
learning_rate: float = 0.0
EPOCH: int = 0
DATASET_SIZE: int = 0

# fetching the data
with open("./src/cost_helpers/results/cost_data.txt", "r") as f:
    for index, line in enumerate(f):
        if index == 0:
            learning_rate = float(line)
        elif index == 1:
            EPOCH = int(line)
        elif index == 2:
            DATASET_SIZE = int(line)
        else:
            data.append(float(line))

# adding annotations
plt.xlabel("Epochs")
plt.ylabel("Cost")
plt.title(
    f"Cost evolution for the neural network, DATASET_SIZE={DATASET_SIZE}\nlearning_rate={learning_rate}, EPOCH={EPOCH}"
)

# creating and saving the plot
plt.plot(range(len(data)), data)
plt.savefig("./src/cost_helpers/results/cost_plot.png")
