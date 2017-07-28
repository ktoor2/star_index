"""
Test to find the time taken to find image with a metadata from /images_json &csv folders
"""

from jsonoperations import readOneJson
from csvoperations import readOneCsv
import os
import time


def searchInJson(options):
    result_list = []
    path_to_images = '/Users/okt/Desktop/my_project/data/text_json'
    start_time = time.time()
    for root, dirs, filenames in os.walk(path_to_images):
        for f in filenames:
            fullpath = os.path.join(path_to_images, f)
            meta_dict = readOneJson(fullpath)
            if options == 1:
                substring = "ati"
                if substring in meta_dict['primary'] or substring in meta_dict['secondary'] or substring in meta_dict['tertiary']:
                    result_list.append(meta_dict)

    return((time.time() - start_time)*1000)
    



                    


                    

'''
def searchInCsv(options):
    path_to_images = '/Users/okt/Desktop/my_project/data/text_csv'
    for root, dirs, filenames in os.walk(path_to_images):
        for f in filenames:
            fullpath = os.path.join(path_to_images, f)
            meta_dict = readOneCsv(fullpath)
            if options = 1:
                if 'correlation' in meta_dict.keys():
                    if meta_dict['correlation'] > 0.4:
                    

            if options = 2:
                if 'lat' in meta_dict.keys():
''' 
time_list = []                   
for x in range(1,100):                   
    time_list.append(searchInJson(1))

print(sum(time_list)/len(time_list))

            





    





