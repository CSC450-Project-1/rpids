import csv, json, os, sys, glob, xlrd
import numpy as np
import pandas as pd

# glob and os

# TODO
# Able to change delimter
# Throw error if the dimensions don't match
# Throw error if numerical data in label file
# Throw error if alpha space data in run data
# Make sure label info num of lines == 1
data_files = [r"C:\Users\kuhnb\Desktop\Large Dataset\Measurement1.csv", r"C:\Users\kuhnb\Desktop\Large Dataset\Measurement2.csv", r"C:\Users\kuhnb\Desktop\Large Dataset\Measurement3.csv"]  #for testing json.loads(sys.argv[2])
path = r"engine\sample_data"
#for testing label_file =  sys.argv[1]
label_file = r"C:\Users\kuhnb\Desktop\Large Dataset\Data_Label.csv"
# Get label information
csv_ext = data_files[0].find("csv", len(data_files[0]) - 3, len(data_files[0]))
txt_ext= data_files[0].find("txt", len(data_files[0]) - 3, len(data_files[0]))
excel_ext = data_files[0].find("xlsx", len(data_files[0]) - 4, len(data_files[0]))
def read_label():
    column = []

    with open(label_file) as label_csv:
        csvReader = csv.reader(label_csv)
        for row in csvReader:
            column = row
        if len(column) == 0:
            return print("Invalid label file!")

        return column
def read_excel_label():
    wb = xlrd.open_workbook(label_file)
    sheet = wb.sheet_by_index(0)
 
    sheet.cell_value(0, 0)
    column = sheet.row_values(0)

    return column

def read_excel_file():
    df = pd.read_excel(data_files[0], names = read_excel_label())
    return df

def read_csv_file():
    df = pd.read_csv(data_files[0], names = read_label())
    return df


def read_data():
    #find csv, excel, txt extension returns -1 if not found or the first index if found
    #if excel extension and not csv, use read_excel to import data
    if excel_ext > 1 and csv_ext == -1:
         df_from_each_file = (pd.read_excel(f, names = read_label()) for f in data_files)
    #if csv or text files use read_csv to import data
    elif excel_ext == -1:
        df_from_each_file = (pd.read_csv(f, names = read_label()) for f in data_files)
    #concatenate each dataframe
    concatenated_df = pd.concat(df_from_each_file, ignore_index=True, sort = False)
    return concatenated_df

def read_all_files():
    df_from_each_file = []
    for filename in glob.glob(os.path.join(path, '*.csv')):
        with open(os.path.join(os.getcwd(), filename), 'r') as f:
            df_from_each_file.append((pd.read_csv(f, names = read_label())))
    df_from_each_file.pop(0)   
    concatenated_df = pd.concat(df_from_each_file, ignore_index=True, sort = False)
    return concatenated_df

def read_all_encompassing_file():
    if excel_ext > 1 and csv_ext == -1:
        df_from_each_file = (pd.read_excel(f) for f in data_files)
    elif (csv_ext > 1 or txt_ext > 1) and excel_ext == -1:
        df_from_each_file = (pd.read_csv(f)for f in data_files)
    concatenated_df = pd.concat(df_from_each_file, ignore_index=True, sort = False)
    return concatenated_df

def main():
    if(len(data_files) > 1 and label_file != ""):
        df = read_data()
    elif label_file == "":
        df = read_all_encompassing_file()
    elif excel_ext > 1 and label_file != "" and len(data_files) == 1:
        df = read_excel_file()
    elif csv_ext > 1 and label_file != "" and len(data_files) == 1:
        df = read_csv_file()
    print(df)
    #df.to_json(os.path.abspath('temp/data.json')) #TODO: just for testing
    #sys.stdout.flush()

if __name__ == "__main__":
    main()
