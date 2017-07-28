import os
import csv
import ast

"""
Read and write csv operations vaccillating between csv and python dictionary
Author: Kunwar Singh
"""



def writeToCsv(path_to_save_meta,meta_filename,tag_dict):
    """Writes the data dictionary to csv file. returns nothing"""
    print("writetocsv called")
    if not os.path.exists(path_to_save_meta):
        os.makedirs(path_to_save_meta)
    with open(os.path.join(path_to_save_meta, meta_filename), 'w') as f:
        w = csv.DictWriter(f, tag_dict.keys(), quoting = csv.QUOTE_NONNUMERIC)
        w.writeheader()
        w.writerow(tag_dict)


def readFromCsv(path):
    """Reads a csv file and convert the results to a dictionary"""
    data_list = []
    for root, dirs, filenames in os.walk(path):
        for f in filenames:
            if f.endswith('.csv'):
                fullpath = os.path.join(path,f)
                input_file = csv.DictReader(open(fullpath), quoting = csv.QUOTE_NONNUMERIC )
                for row in input_file:
                    data_dict = row
                data_list.append(data_dict)

    return data_list


#readFromCsv('/Users/okt/Desktop/my_project/data/images_meta')

def readOneCsv(path):
    input_file = csv.DictReader(open(path), quoting = csv.QUOTE_NONNUMERIC )
    for row in input_file:
        data_dic = row

    return data_dict

                

    
