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
label_file =  r"sample_data\Data_Label.csv" #for testing sys.argv[1]
json.loads(sys.argv[2]) # for testing data_files = [r"sample_data\Measurement1.csv", r"sample_data\Measurement2.csv", r"sample_data\Measurement3.csv", r"sample_data\Measurement4.csv"]
#for testing data_files =  [r"sample_data\Book2.xlsx"]
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
    #find csv, excel, txt extension returns -1 if not found or the first index if found
    csv_ext = data_files[0].find("csv", len(data_files[0]) - 3, len(data_files[0]))
    txt_ext= data_files[0].find("txt", len(data_files[0]) - 3, len(data_files[0]))
    excel_ext = data_files[0].find("xlsx", len(data_files[0]) - 4, len(data_files[0]))
    #if excel extension and not csv, use read_excel to import data
    if excel_ext and csv_ext == -1:
         df_from_each_file = (pd.read_excel(f, names = read_label()) for f in data_files)
    #if csv or text files use read_csv to import data
    elif csv_ext or txt_ext and excel_ext == -1:
        df_from_each_file = (pd.read_csv(f, names = read_label()) for f in data_files)
    
    #concatenate each dataframe
    concatenated_df = pd.concat(df_from_each_file, ignore_index=True, sort = False)
    return concatenated_df

def main(): 
    df = read_data()
    # csv_ext = data_files[0].find("csv", len(data_files[0]) - 3, len(data_files[0]))
    # txt_ext= data_files[0].find("txt", len(data_files[0]) - 3, len(data_files[0]))
    # print("csv: ", csv_ext)
    # print("csv: ", txt_ext)
    print(df)
    df.to_json(os.path.abspath('temp/data.json')) #TODO: just for testing
    sys.stdout.flush()

if __name__ == "__main__":
    main()
