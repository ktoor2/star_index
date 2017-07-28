"""
Test to find the time taken to find image with a metadata from /images_json &csv folders
"""

from jsonoperations import readOneJson
from csvoperations import readOneCsv
import time
import os


def searchInJson(options):
    i = 0
    path_to_images = '/Users/okt/Desktop/my_project/data/images_json'
    start_time = time.time()
    result_list = []
    for root, dirs, filenames in os.walk(path_to_images):
        for f in filenames:
            i = i +1
            if(i >1000):
                break
            fullpath = os.path.join(path_to_images, f)
            meta_dict = readOneJson(fullpath)
            if options == 1:
                if 'correlation' in meta_dict.keys():
                    if meta_dict['correlation'] > 0.8:
                        result_list.append(meta_dict)
                    #store the path in the list

            elif options == 2:
                if 'lat' in meta_dict.keys():
                    result_list.append(meta_dict)
                    

            else:
                if 'XResolution' in meta_dict.keys():
                    array = meta_dict['XResolution']
                    if 1 in array:
                        result_list.append(meta_dict)


    #print(result_list)
    return((time.time() - start_time)*1000)


                    

'''
def searchInCsv(options):
    path_to_images = '/Users/okt/Desktop/my_project/data/images_csv'
    for root, dirs, filenames in os.walk(path_to_images):
        for f in filenames:
            fullpath = os.path.join(path_to_images, f)
            meta_dict = readOneCsv(fullpath)
            if options == 1:
                if 'correlation' in meta_dict.keys():
                    if meta_dict['correlation'] > 0.4:
                    

            if options == 2:
                if 'lat' in meta_dict.keys():
                    

            if options == 3:
                if 'XResolution' in meta_dict.keys():
                    if meta_dict[XResolution][1]  > 1:

'''
'''
Run your tests here
'''

time_list = []
for x in range(1, 100):
    time_list.append(searchInJson(3))

print(sum(time_list)/len(time_list))





    





