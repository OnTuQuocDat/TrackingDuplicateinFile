import pandas as pd
import shutil
import os

def copy_txt_file():
    startfile = r'debug.txt'
    endfile = r'debug_copy.txt'
    if os.stat(startfile).st_size != 0:
        shutil.copyfile(startfile,endfile)

def convert_csv():
    read_file = pd.read_csv(r'debug_copy.txt',sep='\s+',header=None)
    read_file.to_csv(r'debug.csv',index=None)
