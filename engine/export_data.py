
import csv
import json
import os
import sys
import numpy as np
import pandas as pd

# load data frame that is passed in
local_path = sys.argv[1]


def main():
    data_file = pd.read_json(os.path.abspath('temp/data.json'))
    data_file.drop
    data_file.to_csv(local_path, header=False, index=False)

    eig_data_file = pd.read_json(os.path.abspath('temp/eig_data.json'))
    eig_data_file.drop
    eig_data_file.to_csv(local_path, header=False, index=False)

    f = open("temp/data.json", "r+")
    f.seek(0)
    f.truncate()
    print(data_file)
    sys.stdout.flush()

    f = open("temp/eig_data.json", "r+")
    f.seek(0)
    f.truncate()
    print(eig_data_file)
    sys.stdout.flush()


if __name__ == "__main__":
    main()
