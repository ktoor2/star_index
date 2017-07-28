import os
import json
from PIL import Image
import exifread
import csv
from PIL.ExifTags import TAGS, GPSTAGS
from csvoperations import writeToCsv
from histograms import getCorrelation
import random
import sys
from jsonoperations import writeToJson
from random import randint
import re
import pickle

'''
Author: Kunwar Singh
saves image metadata to a filesystem, including GPS data
'''

path_to_save_meta_json = '/Users/okt/Desktop/my_project/data/images_json'


gps_info = False #initially it is false
arg_list = sys.argv
data_format = arg_list[0]
counter = 0
eventid = 1


'''
    Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags
'''
def getMetadata(image):

    print("getmetadata called")
    info = image._getexif()
    global gps_info

    exif_data = {}
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_info = True
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t,t)
                    gps_data[sub_decoded] = value[t]
                    
                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

        '''Remove unwanted fields here'''
    if "JPEGThumbnail" in exif_data: del exif_data['JPEGThumbnail']
    if "MakerNote" in exif_data: del exif_data['MakerNote']
    return exif_data


def _get_if_exist(data, key):
    if key in data:
        return data[key]

    return None


'''
Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
'''
def _convert_to_degress(value):
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)



'''
    Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)
'''
def getLatLon(exif_data):

    lat = None
    lon = None
    global gps_info
    if gps_info == True:      
        gps_info = exif_data["GPSInfo"]
        gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
        gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')
        gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":                     
                lat = 0 - lat

            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon

        exif_data['lat'] = lat
        exif_data['lon'] = lon
        del exif_data['GPSInfo']
    
    exif_data['topic'] = random.choice(["nuclear", "plant", "heatgradient", "pipeburst"])
    print(exif_data['topic'])
    return exif_data


'''
Get dictionary of a single image. Called through DogWatch
'''
def getImageMetaData(path):
    if '.jpg' not in path:
        return 0
    tag_dict = getDict(path)

    #as we do not have event in our metadata we generate an arbitary event
    myfile = open('mynumber.txt', 'r')
    eventid = int(myfile.read())
    myfile.close()
    tag_dict['eventid'] = eventid
    basename = re.search(r'[^\\/]+(?=[\\/]?$)', path)
    if basename:
        basename =  basename.group(0)
        meta_filename =  basename + '_meta.json'
        writeToJson(path_to_save_meta_json,meta_filename, tag_dict)
        return tag_dict

    return None

'''
Get the complete metadata dictionary of an Image(path)
'''
def getDict(path, calltype = 'default'):
    flag = 0
    global counter
    global eventid
    image = Image.open(path)
    tag_dict = getMetadata(image)
    tag_dict = getLatLon(tag_dict)
    tag_dict = getCorrelation(path, tag_dict)
    tag_dict['path'] = path
    tag_dict['XResolution'] = [randint(0,255),randint(0,255)]

    if calltype == 'create':
        if (counter == 0 or counter == 1):
            flag = 1
            tag_dict['eventid'] = 1
        if(counter%2 == 0 and counter!=0):
            eventid = eventid+1

        counter = counter + 1
        
        if(flag!=1):
            tag_dict['eventid'] = eventid

        return tag_dict

    return tag_dict

def loadEventId(filename):

    with open(filename, 'rb') as fobj:
        return pickle.load(fobj)



                


'''
iterate over all files in images and produce JSON/CSV
'''
if __name__== "__main__":
    
    source = '/Users/okt/Desktop/my_project/data/images'
    path_to_save_meta = '/Users/okt/Desktop/my_project/data/images_meta'
    for root, dirs, filenames in os.walk(source):
        for f in filenames:
            if f.endswith('.jpg'):
                dirpath = os.path.join(source,root)
                fullpath = os.path.join(dirpath, f)
                tag_dict = getDict(fullpath, 'create')
                print(tag_dict['eventid'])
                
                if(data_format == 'csv'):
                    meta_filename = f + '_meta.csv'
                    writeToCsv(path_to_save_meta,meta_filename,tag_dict)
                else:
                    meta_filename = f + '_meta.json'
                    writeToJson(path_to_save_meta_json,meta_filename, tag_dict)

    with open('eventid.pickle', 'wb')as fobj:
        pickle.dump(eventid, fobj)





    


