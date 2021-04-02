
import csv, json, os, sys
import numpy as np
import pandas as pd

#load data frame that is passed in
local_path = sys.argv[1]
data_file = json.load(sys.argv[2])

def main():
    data_file[0].to_csv(local_path)