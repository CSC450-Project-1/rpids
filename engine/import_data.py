# _______________________________________________________________________________________________________________________________

#  Project Name:      Response Pattern-Based Identification System (RPIDS)
#  Purpose:           A Graphical User Interface (GUI) based software to assist chemists in performing principal component
#                     analysis (PCA) and hierarchical clustering analysis (HCA). 
#  Project Members:   Zeth Copher
#                     Josh Kuhn
#                     Ryan Luer
#                     Austin Pearce
#                     Rich Russell
#  Course:         Missouri State University CSC450 - Intro to Software Engineering Spring 2021
#  Instructor:     Dr. Razib Iqbal, Associate Professor of Computer Science 
#  Contact:        RIqbal@MissouriState.edu

#  License:
#  Copyright 2021 Missouri State University

#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
#  documentation files (the "Software"), to deal in the Software without restriction, including without limitation the 
#  rights to use, copy, modify, merge, publish, distribute, sub-license, and/or sell copies of the Software, and to
#  permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING 
#  BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
#  NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# _______________________________________________________________________________________________________________________________________

import csv, json, os, sys, glob, xlrd
import numpy as np
import pandas as pd

#run data file paths
data_files= json.loads(sys.argv[2])

#check if sys.argv is defined and assign label_file the appropriate value
if sys.argv[1] is not None:
    label_file = sys.argv[1]
else:
    label_file = ""

#User selected options on the import form
form_data = json.loads(sys.argv[3])

#path to the temp library
temp_path = sys.argv[4]

# Get label extensions
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
    if (os.path.isfile(getDataPath())):
        f = open(getDataPath(), "r+")
        f.seek(0)
        f.truncate()
        f.close()
    else:
        f = open(getDataPath(), "w")
        f.close()


#_________________________________________________________________
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
#___________________________________________________________________
#___________________________________________________________________
#
# The code block below fulfills the requirements of:
#
# Software Requirement Specification (SRS):    ( functional 1.1.1) - Page x
# Software Design Document (SDD) :                (component 5) - Page x
#___________________________________________________________________
def read_label():
     column = []
     if (form_data["delimiter"] == 'comma'):
        with open(label_file) as label_csv:
            csvReader = csv.reader(label_csv)
            for row in csvReader:
                column = row
            if len(column) == 0:
                return print("Invalid label file!")
     else:
        label_csv  = open(label_file)
        file_contents = label_csv.read()
        contents_split = file_contents.splitlines()

        if len(contents_split) == 0:
            return print("Invalid label file!")
        column = contents_split
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
#___________________________________________________________________
#
# The code block below fulfills the requirements of:
#
# Software Requirement Specification (SRS):    ( functional 1.1.2) - Page x
# Software Design Document (SDD) :                (component 5) - Page x
#___________________________________________________________________
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
#___________________________________________________________________
#
# The code block below fulfills the requirements of:
#
# Software Requirement Specification (SRS):    ( functional 1.1.2) - Page x
# Software Design Document (SDD) :                (component 5) - Page x
#___________________________________________________________________
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
#___________________________________________________________________
#
# The code block below fulfills the requirements of:
#
# Software Requirement Specification (SRS):    ( functional 1.1.2) - Page x
# Software Design Document (SDD) :                (component 5) - Page x
#___________________________________________________________________
def read_csv_file():
    if form_data["delimiter"] == 'comma':
        if form_data["dataFormat"] == 'rows':
            df = pd.read_csv(data_files[0], names = range(len(read_label())))
        else:
            df = pd.read_csv(data_files[0], names = range(len(read_label()))).transpose()
    else:
        if form_data["dataFormat"] == 'rows':
            df = pd.read_csv(data_files[0], names = range(len(read_label())), sep = r"\s+")
        else:
            df = pd.read_csv(data_files[0], names = range(len(read_label())), sep = r"\s+").transpose()

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
#___________________________________________________________________
#
# The code block below fulfills the requirements of:
#
# Software Requirement Specification (SRS):    (FR 1.1.2, NFR 1) - Page x
# Software Design Document (SDD) :                (component 5) - Page x
#___________________________________________________________________
def read_data():
     #find csv, excel, txt extension returns -1 if not found or the first index if found
     #if excel extension and not csv, use read_excel to import data
    if excel_ext > 1 and csv_ext == -1 and form_data["delimiter"] == 'comma':
        if form_data["dataFormat"] == 'rows':
            df_from_each_file = (pd.read_excel(f, names = read_label()) for f in data_files)
        else:
            df_from_each_file = (pd.read_excel(f, names = read_label()).transpose() for f in data_files)
        #if csv or text files use read_csv to import data
    elif excel_ext == -1 and form_data["delimiter"] == 'comma':
        if form_data["dataFormat"] == 'rows':
            df_from_each_file = (pd.read_csv(f, names = read_label())for f in data_files)
        else:
            df_from_each_file = (pd.read_csv(f, names = read_label()).transpose() for f in data_files)

    elif excel_ext == -1 and form_data["delimiter"] == 'space':
        if form_data["dataFormat"] == 'rows':
            df_from_each_file = (pd.read_csv(f, names = read_label(), sep = r'\s+') for f in data_files)
        else:
            df_from_each_file = (pd.read_csv(f, names = read_label(), sep = r'\s+').transpose() for f in data_files)
       
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
#___________________________________________________________________
#
# The code block below fulfills the requirements of:
#
# Software Requirement Specification (SRS):    (FR 8) - Page x
# Software Design Document (SDD) :                (component 5) - Page x
#___________________________________________________________________
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

def getDataPath():
    return os.path.join(temp_path,"data.json")

#______________________________________________________________
#add Sample and Run function:
#this function accepts a Dataframe as a parameter and adds the 
#correct amount of sample names and file names to match each data
#point.
#return value:
#df     pandas dataframe        modified dataframe to hold samples
#                                           and file names as a column
#reference parameters:
#df     pandas dataframe        imported run data held in a dataframe
#
#local variables:
#names     string array             holds file label names without any spaces
#file_names     string array        holds the run data file names
#file_names_list    string array    holds the file_names that will be fitted
#                                        to match each point on the graph
#_______________________________________________________________
def addSampleAndRun(df):
    if(len(label_file)> 1):
        if (csv_ext > 1 or txt_ext > 1):
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
    return df
#______________________________________________________________
#create df function:
#This function checks the file extension and the length of the run
#  file list to determine which function to call to read the datasets. 
#
#return value:
#df     pandas dataframe        holds the run and label data imported by the user        
#                                           
#no parameters.
#
#local variables:
#df     pandas dataframe        holds the incoming data from the function being called, 
#                                               eventually will be returned
#_______________________________________________________________
def createDf():
    if(len(data_files) > 1 and label_file != ""):
        df = read_data()
    elif label_file == "":
        df = read_all_encompassing_file()
    elif excel_ext > 1 and label_file != "" and len(data_files) == 1:
        df = read_excel_file()
    elif csv_ext > 1 or txt_ext > 1 and label_file != "" and len(data_files) == 1:
        df = read_csv_file()
    return df

def main():
    clear_json()
    try:
        df = createDf()
        newDf = addSampleAndRun(df)
        newDf.to_json(getDataPath())
        sys.stdout.flush()
    #  else: 

        # df.to_json(os.path.abspath('temp/data.json')) #TODO: just for testing
       
        # sys.stdout.flush()
    except Exception as e:
        print("Oops!", e.__class__, e, "occurred.")
        print(names)




if __name__ == "__main__":
    clear_json()
    main()
