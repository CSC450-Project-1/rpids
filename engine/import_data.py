import csv
import numpy as np
import pandas as pd

# TODO
# Able to change delimter
# Throw error if the dimensions don't match
# Throw error if numerical data in label file
# Throw error if alpha space data in run data
# Make sure label info num of lines == 1

# Get label information
def read_label():
    column = []
    label_file = "sample_data/Data_Label.csv" # TODO: for testing

    with open(label_file) as file:
        reader = csv.reader(file)
        for row in reader:
            column = row
        if len(column) == 0:
            return print("Invalid label file!")

        return column

def read_data():
        df = pd.read_csv("sample_data/Measurement1.csv") # TODO: for testing
        return df
        
def main(): 
    label = read_label()
    data = read_data()
    data.columns  = [label]
    print(data)

if __name__ == "__main__":
    main()
