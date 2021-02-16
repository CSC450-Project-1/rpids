import csv, json, os, sys
import numpy as np
import pandas as pd

# glob and os

# TODO
# Able to change delimter
# Throw error if the dimensions don't match
# Throw error if numerical data in label file
# Throw error if alpha space data in run data
# Make sure label info num of lines == 1
label_file = sys.argv[1] #"sample_data\Data_Label.csv" #for testing
data_files =  json.loads(sys.argv[2]) #["sample_data\Measurement1.csv", "sample_data\Measurement2.csv", "sample_data\Measurement3.csv", "sample_data\Measurement4.csv"] #for testing

# Get label information
def read_label():
    column = []

    with open(label_file) as label_csv:
        csvReader = csv.reader(label_csv)
        for row in csvReader:
            column = row
        if len(column) == 0:
            return print("Invalid label file!")

        return column

        
def read_data():
    df_from_each_file = (pd.read_csv(f, names = read_label()) for f in data_files)
    concatenated_df = pd.concat(df_from_each_file, ignore_index=False, sort = False)
    return concatenated_df

def main(): 
    df = read_data()
    #print(data)
    df.to_json(os.path.abspath('temp/data.json')) #TODO: just for testing
    sys.stdout.flush()

if __name__ == "__main__":
    main()
