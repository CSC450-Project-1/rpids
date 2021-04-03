
import csv, json, os, sys
import numpy as np
import pandas as pd

#load data frame that is passed in
local_path = sys.argv[1]

def main():
    data_file = pd.read_csv(os.path.abspath('temp/data.json'))
    data_file.to_csv(local_path + '.csv')
    print(data_file)
    sys.stdout.flush()

if __name__ == "__main__":
    main()