
import csv, json, os, sys
import numpy as np
import pandas as pd

#load data frame that is passed in
local_path = sys.argv[1]
eig_path = local_path[:len(local_path) - 4] + "_eigen" + local_path[len(local_path):]
def main():
    data_file = pd.read_json(os.path.abspath('temp/computed_data.json'))
    data_file.to_csv(local_path, index = False)
    eig_data_file = pd.read_json(os.path.abspath('temp/eig_data.json'))
    eig_data_file.to_csv(eig_path + ".csv", index = False)
    f = open("temp/computed_data.json", "r+")
    f.seek(0)
    f.truncate()
    f = open("temp/eig_data.json", "r+")
    f.seek(0)
    f.truncate()
    f = open("temp/data.json", "r+")
    f.seek(0)
    f.truncate()
    sys.stdout.flush()

if __name__ == "__main__":
    main()