
import csv, json, os, sys
import numpy as np
import pandas as pd

#load data frame that is passed in
local_path = sys.argv[1]
temp_path = sys.argv[2]
eig_path = local_path[:len(local_path) - 4] + "_eigen" + local_path[len(local_path):]

def getDataPath(filename):
    return os.path.join(temp_path, filename)

def main():
    data_file = pd.read_json(getDataPath("computed_data.json"))
    data_file.to_csv(local_path, index = False)
    eig_data_file = pd.read_json(getDataPath("eig_data.json"))
    eig_data_file.to_csv(eig_path + ".csv", index = False)
    f = open(getDataPath("computed_data.json"), "r+")
    f.seek(0)
    f.truncate()
    f = open(getDataPath("eig_data.json"), "r+")
    f.seek(0)
    f.truncate()
    
if __name__ == "__main__":
    main()