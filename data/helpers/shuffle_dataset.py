import random, sys

if len(sys.argv) != 2:
    exit("[shuffle_dataset] Error - missing arguments\n-> input file's path")
else:
    INPUT_FILE_PATH: str = sys.argv[1]

with open(INPUT_FILE_PATH, "r") as f:
    lines = f.readlines()

with open(INPUT_FILE_PATH, "w") as f:
    random.shuffle(lines)
    f.writelines(lines)
