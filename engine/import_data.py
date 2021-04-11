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
data_files = [r"C:\Users\kuhnb\Desktop\Large Dataset\allencompassingfile.xlsx"] #json.loads(sys.argv[2])
label_file = "" #for testing sys.argv[1]
#json.loads(sys.argv[2]) # for testing data_files = [r"sample_data\Measurement1.csv", r"sample_data\Measurement2.csv", r"sample_data\Measurement3.csv", r"sample_data\Measurement4.csv"]
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
     wb = xlrd.open_workbook(data_files[0])
     sheet = wb.sheet_by_index(0)
 
     sheet.cell_value(0, 0)
     column = sheet.row_values(0)

     return column

def read_excel_file():
     df = pd.read_excel(data_files[0], names = range(len(read_label()))).transpose()
     return df

def read_csv_file():
     df = pd.read_csv(data_files[0], names = range(len(read_label()))).transpose()
     return df


def read_data():
     #find csv, excel, txt extension returns -1 if not found or the first index if found
     #if excel extension and not csv, use read_excel to import data
     if excel_ext > 1 and csv_ext == -1:
        df_from_each_file = (pd.read_excel(f, names = read_label()).transpose() for f in data_files)
     #if csv or text files use read_csv to import data
     elif excel_ext == -1:
        df_from_each_file = (pd.read_csv(f, names = read_label()).transpose() for f in data_files)
    #concatenate each dataframe
     concatenated_df = pd.concat(df_from_each_file, ignore_index=True, sort = False)
     return concatenated_df
# def read_col_to_row():
    #  rows = []
    #  names = read_label()
    #  for i > len(data_files):
    #     with open(data_files[i]) as df:
    #         csvReader = csv.reader(df)
    #         for column in csvReader:
    #             row = column
                


# def read_all_files():
#      df_from_each_file = []
#      for filename in glob.glob(os.path.join(path, '*.csv')):
#          with open(os.path.join(os.getcwd(), filename), 'r') as f:
#              df_from_each_file.append((pd.read_csv(f, names = read_label())))
#      df_from_each_file.pop(0)   
#      concatenated_df = pd.concat(df_from_each_file, ignore_index=True, sort = False)
#      return concatenated_df

def read_all_encompassing_file():
     if excel_ext > 1 and csv_ext == -1:
         df_from_each_file = (pd.read_excel(f, names =read_excel_label()).transpose() for f in data_files)
     elif (csv_ext > 1 or txt_ext > 1) and excel_ext == -1:
         df_from_each_file = (pd.read_csv(f).transpose() for f in data_files)
     concatenated_df = pd.concat(df_from_each_file, ignore_index=True, sort = False)
     
     return concatenated_df

def format_dataframe(df):
     df_t = df.transpose()
     return df_t

def main():
     if(len(data_files) > 1 and label_file != ""):
         df = read_data()
     elif label_file == "":
         df = read_all_encompassing_file()
     elif excel_ext > 1 and label_file != "" and len(data_files) == 1:
         df = read_excel_file()
     elif csv_ext > 1 and label_file != "" and len(data_files) == 1:
         df = read_csv_file()
     if(len(label_file) > 0):
        names = read_label()
        names = names * len(data_files)
        df["Samples"] = names
        dfs = df.sort_values(by=['Samples'])
        print(dfs)
    #  df_t = format_dataframe(df)
    #  print(df_t)
        dfs.to_json(os.path.abspath('temp/data.json')) #TODO: just for testing
        sys.stdout.flush()
     else: 
         names = read_excel_label()
         df["Samples"] = names
         dfs = df.sort_values(by=['Samples'])
         print(dfs)
    #  df_t = format_dataframe(df)
    #  print(df_t)
         dfs.to_json(os.path.abspath('temp/data.json')) #TODO: just for testing
         sys.stdout.flush()

if __name__ == "__main__":
    main()
