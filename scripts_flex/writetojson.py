import os
import json

"""
Read and write csv operations vaccillating between csv and python dictionary
Author: Kunwar Singh
"""



def writeToJson(path_to_save_meta,meta_filename,tag_dict):
    """Writes the data dictionary to csv file. returns nothing"""
    print("writetojson called")
    if not os.path.exists(path_to_save_meta):
        os.makedirs(path_to_save_meta)
    with open(os.path.join(path_to_save_meta, meta_filename), 'w') as f:
        json.dump(tag_dict, f)


def readFromJson(path):
    """Reads a json file and convert the results to a dictionary"""
    data_list = []
    for root, dirs, filenames in os.walk(path):
        for f in filenames:
            fullpath = os.path.join(path,f)
            with open(fullpath) as f:
                tag_dict = json.load(f)

            data_list.append(tag_dict)


readFromJson('/Users/okt/Desktop/my_project/data/images_meta')
                

    
