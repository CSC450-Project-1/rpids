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
import csv
import json
import os
import sys
import numpy as np
import pandas as pd

# load data frame and paths/settings that is passed in
local_path = sys.argv[1]
temp_path = sys.argv[2]
settings = json.loads(sys.argv[3])
local_path_shorten = os.path.splitext(local_path)[0]
ext = ".csv"


def getDataPath(filename):
    return os.path.join(temp_path, filename)

# ______________________________________________________________
# export pca to csv function:
# This function saves the dataset by reading from the json file and saving it as a csv file
#
# return value:
# none.
#
# no parameters.
#
# local variables:
# data_file     pandas dataframe        holds the data read from computed_data.json
# eig_data_file     pandas dataframe        holds the data read from eig_data.json
# _______________________________________________________________
# ___________________________________________________________________
#
# The code block below fulfills the requirements of:
#
# Software Requirement Specification (SRS):    (FR. 10) - Page x
# Software Design Document (SDD) :                (component 7) - Page x
# ___________________________________________________________________


def export_pca_to_csv():
    if is_file_exportable(getDataPath("pca_2d.json")):
        pca_2d_file = pd.read_json(getDataPath("pca_2d.json"))
        if pca_2d_file.empty == False:
            pca_2d_file.to_csv(local_path_shorten +
                               "_pca_2d" + ext, index=False)

    if is_file_exportable(getDataPath("pca_3d.json")):
        pca_3d_file = pd.read_json(getDataPath("pca_3d.json"))
        if pca_3d_file.empty == False:
            pca_3d_file.to_csv(local_path_shorten +
                               "_pca_3d" + ext, index=False)

    if is_file_exportable(getDataPath("eig_data.json")):
        eig_data_file = pd.read_json(getDataPath("eig_data.json"))
        if eig_data_file.empty == False:
            eig_data_file.to_csv(local_path_shorten +
                                 "_eigen" + ext, index=False)


def is_file_exportable(path):
    return os.path.exists(path) and os.path.getsize(path) > 0

# ______________________________________________________________
# export hca to csv function:
# This function saves the dataset by reading from the json file and saving it as a csv file
#
# return value:
# none.
#
# no parameters.
#
# local variables:
# df     pandas dataframe        holds the incoming data from the function being called,
#                                               eventually will be returned
# _______________________________________________________________
# ___________________________________________________________________
#
# The code block below fulfills the requirements of:
#
# Software Requirement Specification (SRS):    (FR. 10) - Page x
# Software Design Document (SDD) :                (component 7) - Page x
# ___________________________________________________________________


def export_data_to_csv():
    if os.path.exists(getDataPath("data.json")):
        data_file = pd.read_json(getDataPath("data.json"))
        data_file.to_csv(local_path, index=False)


def clear_output_files():
    if os.path.exists(getDataPath("pca_2d.json")):
        f = open(getDataPath("pca_2d.json"), "r+")
        f.seek(0)
        f.truncate()
    if os.path.exists(getDataPath("pca_3d.json")):
        f = open(getDataPath("pca_3d.json"), "r+")
        f.seek(0)
        f.truncate()
    if os.path.exists(getDataPath("eig_data.json")):
        f = open(getDataPath("eig_data.json"), "r+")
        f.seek(0)
        f.truncate()


def main():
    export_data_to_csv()
    export_pca_to_csv()
    clear_output_files()


if __name__ == "__main__":
    main()
