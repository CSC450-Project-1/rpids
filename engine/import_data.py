import csv, json, os, sys, glob, xlrd
import numpy as np
import pandas as pd

# TODO
# Able to change delimter
# Throw error if the dimensions don't match
# Throw error if numerical data in label file
# Throw error if alpha space data in run data
# Make sure label info num of lines == 1

data_files= json.loads(sys.argv[2])
if sys.argv[1] is not None:
    label_file = sys.argv[1]
else:
    label_file = ""
form_data = json.loads(sys.argv[3])

# Get label information
csv_ext = data_files[0].find("csv", len(data_files[0]) - 3, len(data_files[0]))
txt_ext= data_files[0].find("txt", len(data_files[0]) - 3, len(data_files[0]))
excel_ext = data_files[0].find("xlsx", len(data_files[0]) - 4, len(data_files[0]))

#_____________________________________________________
#Clear JSON function:
#This function opens and clears the json file
#which holds the data. If there is no file it will
#create one.
#
#No return value.
#
#
#
#______________________________________________________
def clear_json():
    if (os.path.isfile("./temp/data.json")):
        f = open("temp/data.json", "r+")
        f.seek(0)
        f.truncate()
        f.close()
    else:
        f = open("./temp/data.json", "w")
        f.close()


#___________________________________________________________
#Read Label Function
#
#This function reads the first row of a CSV file to an array
#this holds our column names.
#
#Return Value:
#String array
#
#No parameters.
#
#local varaiables:
#column     array       column names for the run data files
#csvReader  Reader object   iterates through csv formatted  files to read data                           
#row        string      string variable to hold column names 
#                           during each iteration
#___________________________________________________________
def read_label():
     column = []

     with open(label_file) as label_csv:
         csvReader = csv.reader(label_csv)
         for row in csvReader:
             column = row
         if len(column) == 0:
             return print("Invalid label file!")

         return column

#___________________________________________________________________
#Read Excel Label function:
#reads the column names from an excel file and stores
#them in an array.
#
#return values:
#String array
#
#no parameters.
#
#local variables:
#wb     Instance of the Workbook class      opens an Excel file for reading the column names
#sheet     instance of the Sheet class      opens a sheet of the workbook to use
#column                   string array      holds column names as an array of strings                      
#__________________________________________________________________
def read_excel_label():
     wb = xlrd.open_workbook(label_file)
     sheet = wb.sheet_by_index(0)
 
     sheet.cell_value(0, 0)
     column = sheet.row_values(0)

     return column

#_______________________________________________________________
#Read Excel file:
#Reads data from an excel file. If the data is in column format 
#the data set is transposed to be in row format, if it is in row format
#it is not transposed.
#
#return values:
#df     dataframe        data from the run data file stored in an organized table format
#
#no parameters.
#
#local variables: 
#df     Dataframe object        Holds data from the read Excel file
#_________________________________________________________________
def read_excel_file():

    if form_data["dataFormat"] == 'rows':
        df = pd.read_excel(data_files[0], names = range(len(read_excel_label())))
    else:
        df = pd.read_excel(data_files[0], names = range(len(read_excel_label()))).transpose()
        
    return df


#_______________________________________________________________
#Read CSV file:
#Reads data from an csv file (can be .csv or .txt, but must be in CSV format).
#If the data is in column format the data set is transposed to be in row format, 
#if it is in row format it is not transposed.
#
#return values:
#df     dataframe        data from the run data file stored in an organized table format
#
#no parameters.
#
#local variables: 
#df     Dataframe object        Holds data from the read CSV file
#_________________________________________________________________
def read_csv_file():
    if form_data["dataFormat"] == 'rows':
        df = pd.read_csv(data_files[0], names = range(len(read_label())))
    else:
        df = pd.read_csv(data_files[0], names = range(len(read_label()))).transpose()
    return df


#_______________________________________________________________
#Read CSV file:
#Reads data from multiple run data files and returns the concatenated data set.
#Supports .csv, .txt, .xlsx files.
#
#return value:
#concatenated_df    dataframe    data from each run file in an organized table format
#
#no parameters.
#
#local variables: 
#df_from_each_file    Generator object       holds a list of references to eacvh of the data files
#concatenated_df      Dataframe object       hold
#_________________________________________________________________
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

#______________________________________________________________
#Read All Encompassing File function:
#This function reads datasets in which the file is already formatted like
#a dataframe. Primarily used for importing exported data sets.
#
#retrun values:
#df     DataFrame object        a dataframe of the imported data
#
#no parameters
#
#local variables:
#df     Pandas Dataframe Object       holds imported data to be written to a json file
#______________________________________________________________
def read_all_encompassing_file():
     if excel_ext > 1 and csv_ext == -1:
         df = pd.read_excel(data_files[0])
     elif (csv_ext > 1 or txt_ext > 1) and excel_ext == -1:
         df = pd.read_csv(data_files[0])
     return df


#______________________________________________________________
#get file names function:
#reads the file names and grabs the base name without the extension.
#This wil be used to add file names to the graph and outported data.
#
#return value:
#file_names     string array        holds the file names
#
#no parameters
#
#
#local variables:
#file_names     string array        string that holds file names
#_______________________________________________________________
def getFileNames():
    file_names= []
    for f in data_files:
        file_names.append(os.path.basename(f))
        
    for i in range(len(data_files)):    
       file_names[i] = file_names[i][: (len(file_names[i]) - 4)]
       file_names[i] = file_names[i].replace(" ", "")
    return file_names

def main():
    try:
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
       
        df.to_json(os.path.abspath('temp/data.json')) #TODO: just for testing
        sys.stdout.flush()
     else: 

        df.to_json(os.path.abspath('temp/data.json')) #TODO: just for testing
       
        sys.stdout.flush()
    except Exception as e:
        print("Oops!", e.__class__, e, "occurred.")




if __name__ == "__main__":
    clear_json()
    main()
