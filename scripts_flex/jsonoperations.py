import os
import json
import io

"""
Read and write csv operations vaccillating between csv and python dictionary
Author: Kunwar Singh
"""



def writeToJson(path_to_save_meta,meta_filename,tag_dict):
    """Writes the data dictionary to csv file. returns nothing"""

    '''
    clean data for json

    
    for k,v in tag_dict.items():
        """
        if (isinstance(v, bytes)):
            
            decoding can be used if the encoding is correct which might not always be the case
            it is better removing the encoded characters unless you are sure what encoding is used
            then one can use the following
            
            tag_dict[k] = v.decode('utf-8')
        """ 
    """
    this can be used to delete the encoded values altogether if the encoding is not known
    """
    '''
    mydict = { k:v for k,v in tag_dict.items() if not (isinstance(v,bytes))}
    
    print("writetojson called")
    if not os.path.exists(path_to_save_meta):
        os.makedirs(path_to_save_meta)
    with open(os.path.join(path_to_save_meta, meta_filename), 'w') as f:
        json.dump(mydict, f)
    

def readFromJson(path):
    """Reads a json file and convert the results to a dictionary"""
    data_list = []
    for root, dirs, filenames in os.walk(path):
        for f in filenames:
            if(f.endswith('.json')):
                fullpath = os.path.join(path,f)
                with open(fullpath) as f:
                    tag_dict = json.load(f)

                data_list.append(tag_dict)

    return data_list

'''
test
path = '/Users/okt/Desktop/my_project/data/images_json/mountain.jpg_meta.json'
with open(path) as f:
    dict = json.load(f)
    print(dict)

readFromJson('/Users/okt/Desktop/my_project/data/images_json')    
'''            

def readOneJson(path):
    with open(path) as f:
        tag_dict = json.load(f)

    return tag_dict
    

    
