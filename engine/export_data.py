
import csv, json, os, sys
import numpy as np
import pandas as pd

#load data frame that is passed in
local_path = sys.argv[1]

def main():
    data_file = pd.read_csv(local_path)
    data_file.to_csv(local_path)
    print(data_file[0])
    data_file.to_json(os.path.abspath('temp/data.json')) #TODO: just for testing
    sys.stdout.flush()

if __name__ == "__main__":
    main()