import csv
import numpy as np
import pandas as pd
import sys

# TODO
# Able to change delimter
# Throw error if the dimensions don't match
# Throw error if numerical data in label file
# Throw error if alpha space data in run data
# Make sure label info num of lines == 1

label_file = sys.argv[1]
data_file = sys.argv[2]

# Get label information
def read_label():
    column = []

    with open(label_file) as file:
        reader = csv.reader(file)
        for row in reader:
            column = row
        if len(column) == 0:
            return print("Invalid label file!")

        return column

def read_data():
    df = pd.read_csv(data_file)
    return df
        
def main(): 
    label = read_label()
    df = read_data()
    df.columns = [label]

    df.to_json(os.path.abspath('temp/data.json'))
    # print(df)
    sys.stdout.flush()

if __name__ == "__main__":
    main()
