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

data_files= json.loads(sys.argv[2]) #[ r"C:\Users\kuhnb\Desktop\Large Dataset\output.csv.csv"]
if sys.argv[1] is not None:
    label_file = sys.argv[1]
else:
    label_file = ""
form_data = json.loads(sys.argv[3])

# print(type(sys.argv[3]))

# for testing
# label_file =  r"sample_data\Data_Label.csv"
# data_files = [r"sample_data\Measurement1.csv", r"sample_data\Measurement2.csv", r"sample_data\Measurement3.csv", r"sample_data\Measurement4.csv"]
# form_data = 'columns'

# Get label information
csv_ext = data_files[0].find("csv", len(data_files[0]) - 3, len(data_files[0]))
txt_ext= data_files[0].find("txt", len(data_files[0]) - 3, len(data_files[0]))
excel_ext = data_files[0].find("xlsx", len(data_files[0]) - 4, len(data_files[0]))

def clear_json():
    f = open("temp/data.json", "r+")
    f.seek(0)
    f.truncate()

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
#, names = read_excel_label()
def read_excel_file():

    if form_data["dataFormat"] == 'rows':
        df = pd.read_excel(data_files[0], names = range(len(read_excel_label())))
    else:
        df = pd.read_excel(data_files[0], names = range(len(read_excel_label()))).transpose()
        
    return df

def read_csv_file():
    if form_data["dataFormat"] == 'rows':
        df = pd.read_csv(data_files[0], names = range(len(read_label())))
    else:
        df = pd.read_csv(data_files[0], names = range(len(read_label()))).transpose()
    return df


def read_data():
     #find csv, excel, txt extension returns -1 if not found or the first index if found
     #if excel extension and not csv, use read_excel to import data
     if excel_ext > 1 and csv_ext == -1:
        if form_data["dataFormat"] == 'rows':
            df_from_each_file = (pd.read_excel(f, names = read_label()) for f in data_files)
        else:
            df_from_each_file = (pd.read_excel(f, names = read_label()).transpose() for f in data_files)
     #if csv or text files use read_csv to import data
     elif excel_ext == -1:
        if form_data["dataFormat"] == 'rows':
            df_from_each_file = (pd.read_csv(f, names = read_label())for f in data_files)
        else:
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
         df = pd.read_excel(data_files[0])
     elif (csv_ext > 1 or txt_ext > 1) and excel_ext == -1:
         df = pd.read_csv(data_files[0])
     return df


def getFileNames():
    file_names= []
    for f in data_files:
        file_names.append(os.path.basename(f))
        
    for i in range(len(data_files)):    
       file_names[i] = file_names[i][: (len(file_names[i]) - 4)]
       file_names[i] = file_names[i].replace(" ", "")
    return file_names

def main():
     clear_json()
     if(len(data_files) > 1 and label_file != ""):
         df = read_data()
     elif label_file == "":
         df = read_all_encompassing_file()
     elif excel_ext > 1 and label_file != "" and len(data_files) == 1:
         df = read_excel_file()
     elif csv_ext > 1 and label_file != "" and len(data_files) == 1:
         df = read_csv_file()


         
     if(len(label_file)> 1):
        if (csv_ext > 1):
            names = read_label()
        else: 
            names = read_excel_label()
        for f in range(len(names)):
            names[f] = names[f].strip()
        file_names = getFileNames()
        file_name_list = []
        for j in range(len(file_names)):
            for i in range(len(names)):
                file_name_list.append(file_names[j])
        names = names * len(data_files)
        df["Samples"] = names
        df["run"] = file_name_list
        # print(df)
    #  df_t = format_dataframe(df)
    #  print(df_t)
        df.to_json(os.path.abspath('temp/data.json')) #TODO: just for testing
        sys.stdout.flush()
     else: 

        df.to_json(os.path.abspath('temp/data.json')) #TODO: just for testing
        # print(sys.argv[3])
        sys.stdout.flush()

    # #  df_t = format_dataframe(df)


if __name__ == "__main__":
    main()
