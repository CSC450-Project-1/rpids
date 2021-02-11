import csv
import numpy as np
import pandas as pd
import glob
import os

# TODO
# Able to change delimter
# Throw error if the dimensions don't match
# Throw error if numerical data in label file
# Throw error if alpha space data in run data
# Make sure label info num of lines == 1

# Get label information
def read_label():
    column = []
    label_file = "Metal Detection Sensor Array/Data_Label.csv" # TODO: for testing

    with open(label_file) as label_csv:
        csvReader = csv.reader(label_csv)
        for row in csvReader:
            column = row
        if len(column) == 0:
            return print("Invalid label file!")

        return column
def read_data():
        # path = input("enter path to folder: ")
        path = r'C:\Users\kuhnb\Desktop\ImportFilesFunc\Metal Detection Sensor Array'
        all_files = ["Measurement1.csv", "Measurement2.csv"]     # advisable to use os.path.join as this makes concatenation OS independen4
        df_from_each_file = (pd.read_csv(f) for f in all_files)
        concatenated_df   = pd.concat(df_from_each_file, ignore_index=True, sort = False)
        return concatenated_df 
        
def main(): 
    label = read_label()
    data = read_data()
    # data.columns  = [label]
    # df = pd.DataFrame(data, columns = label)
    print(data)
   
   # df = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), columns=['a', 'b', 'c'])


    # print(df)
    # print(df.get('a'))

if __name__ == "__main__":
    main()
