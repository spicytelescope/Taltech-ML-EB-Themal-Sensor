import json
import sys

import numpy as np

if len(sys.argv) not in [2, 3]:
    exit(
        f"[label_by_hand] Error - missing arguments\n-> input file's path\n-> [optional] output file path"
    )
else:
    INPUT_FILE_PATH: str = sys.argv[1]
    if len(sys.argv) == 3:
        OUTPUT_FILE_PATH = sys.argv[2]
    else:
        OUTPUT_FILE_PATH = ""

mirrored_content = []

with open(INPUT_FILE_PATH, "r+") as f:

    for l in f.readlines():

        # fetching data into the raw input file
        parsed_json: dict = json.loads(l)
        thermal_data_matrix: list = parsed_json["data"]

        # performing mirror transformation
        parsed_json["data"] = np.fliplr(thermal_data_matrix).tolist()
        mirrored_content.append(json.dumps(parsed_json) + "\n")

with open(OUTPUT_FILE_PATH if OUTPUT_FILE_PATH != "" else INPUT_FILE_PATH, "w") as f:
    f.writelines(mirrored_content)
