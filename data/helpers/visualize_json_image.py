# small script to visualize a random heat map from raw json data in .txt files

import json, sys, matplotlib.pyplot as plt

if len(sys.argv) != 5:
    exit(
        "[visualize_json_image] Error - missing arguments\n-> input file's path\n-> min index of image to save to output dir\n-> max index of image to save to output dir\n -> output dir"
    )
else:
    INPUT_FILE_PATH: str = sys.argv[1]
    PICTURE_RANGE_MIN: int = int(sys.argv[2])
    PICTURE_RANGE_MAX: int = int(sys.argv[3])
    OUTPUT_DIR: str = sys.argv[4]

with open(INPUT_FILE_PATH, "r") as f:

    for _ in range(PICTURE_RANGE_MIN):
        raw_line = f.readline()

    for i in range(PICTURE_RANGE_MAX - PICTURE_RANGE_MIN + 1):
        raw_line = f.readline()

        # fetching data into the raw input file
        parsed_json: dict = json.loads(raw_line)
        thermal_data_matrix: list = parsed_json["data"]
        theral_meta_data: dict = {k: v for k, v in parsed_json.items() if k != "data"}

        # creating the heatmap plot
        fig, ax = plt.subplots()
        im = ax.imshow(thermal_data_matrix)

        # adding legend
        title: str = f"Random thermal sensor frame heatmap from file {INPUT_FILE_PATH}\nMetadata : {json.dumps(theral_meta_data, indent=4)}"
        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.ax.set_ylabel("Room temperature", rotation=-90, va="bottom")
        ax.set_title(title)

        # final plotting
        fig.tight_layout()
        print(
            f"\r[+] Saving heatmap n°{i + PICTURE_RANGE_MIN} ... [{i + 1}/{PICTURE_RANGE_MAX - PICTURE_RANGE_MIN + 1}]"
        )
        plt.savefig(f"{OUTPUT_DIR}/heatmap_{i+ PICTURE_RANGE_MIN}.png")
