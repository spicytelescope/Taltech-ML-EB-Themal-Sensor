import matplotlib.pyplot as plt, sys, json, os

if len(sys.argv) not in [4, 5]:
    exit(
        f"[label_by_hand] Error - missing arguments\n-> input file's path\n-> min index of image to labelise\n-> min index of image to labelise\n-> [optional] output file path"
    )
else:
    INPUT_FILE_PATH: str = sys.argv[1]
    PICTURE_RANGE_MIN: int = int(sys.argv[2])
    PICTURE_RANGE_MAX: int = int(sys.argv[3])

if len(sys.argv) == 5:
    OUTPUT_FILE_PATH = sys.argv[4]
else:
    OUTPUT_FILE_PATH = ""

with open(INPUT_FILE_PATH, "r") as f:

    content = f.readlines()

with open(INPUT_FILE_PATH, "r+") as f:

    for _ in range(PICTURE_RANGE_MIN):
        raw_line = f.readline()

    AMPLITUDE: int = PICTURE_RANGE_MAX - PICTURE_RANGE_MIN + 1

    for i in range(PICTURE_RANGE_MIN, PICTURE_RANGE_MIN + AMPLITUDE):
        raw_line = f.readline()

        # fetching data into the raw input file
        parsed_json: dict = json.loads(raw_line)
        thermal_data_matrix: list = parsed_json["data"]

        # creating the heatmap plot
        fig, ax = plt.subplots()
        im = ax.imshow(thermal_data_matrix)

        # adding legend
        title: str = (
            f"Random thermal sensor frame n°{i} heatmap from file {INPUT_FILE_PATH}"
        )
        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.ax.set_ylabel("Room temperature", rotation=-90, va="bottom")
        ax.set_title(title)

        # final plotting
        fig.tight_layout()
        plt.ion()
        plt.show()

        label: int = int(input("[?] Enter the label (0: NOT human, 1: human) : "))
        parsed_json["label"] = label
        plt.close()

        content[i] = json.dumps(parsed_json) + "\n"

        os.system("cls")

    print(
        f"\r[+] Writing label to lines n°{PICTURE_RANGE_MIN} to {PICTURE_RANGE_MIN+AMPLITUDE-1} ..."
    )

with open(OUTPUT_FILE_PATH if OUTPUT_FILE_PATH != "" else INPUT_FILE_PATH, "w") as f:
    f.writelines(content[PICTURE_RANGE_MIN : PICTURE_RANGE_MIN + AMPLITUDE])
