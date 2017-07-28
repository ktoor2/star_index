import json
import os
from csvoperations import readFromCsv
from jsonoperations import readFromJson, readOneJson
from dbconnect import connect
import psycopg2.extras
import sys

arg_list = sys.argv
data_format = arg_list[0]


def getJson(dict):
    """
    Converts dictionary to a json string and retruns
    """
    dict_text = json.dumps(dict)
    return dict_text


images_path_csv = '/Users/okt/Desktop/my_project/data/images_meta'
text_path_csv = '/Users/okt/Desktop/my_project/data/text_meta'

text_path_json = '/Users/okt/Desktop/my_project/data/text_json'


def readAllFiles(data_format = 'json'):

    if(data_format == 'csv'):
        images_dict_list_csv = readFromCsv(images_path_csv)
        text_dict_list_csv = readFromCsv(text_path_csv)
        list_length = len(images_dict_list_csv)
        return text_dict_list_csv, images_dict_list_csv

        
    else:
        images_dict_list_json = readFromJson(images_path_json)
        print(images_dict_list_json[0])
        text_dict_list_json= readFromJson(text_path_json)
        list_length = len(images_dict_list_json)
        return text_dict_list_json, images_dict_list_json


'''
I have made these two functions seperate so that multiprocessing can be possible .
They can be built into the same function
'''

def readFromImage():
    dict_of_dict = {}
    images_path_json = '/Users/okt/Desktop/my_project/data/images_json'
    for root, dirs, filenames in os.walk():
        for f in filenames:
            if f.endswith('.json'):
                path = os.path.join(path,f)
                tag_dict = readOneJson(path)
                if tag_dict['eventid'] not in dict_of_dict.keys():
                    dict_of_dict[tag_dict['eventid']] = [tag_dict]'' 
                    max_event'
                else:
                    list_from_key = dict_of_dict[tag_dict['eventid']]
                    list_from_key.append(tag_dict)

def readFromText():
    dict_of_dict = {}
    images_path_json = '/Users/okt/Desktop/my_project/data/text_json'
    for root, dirs, filenames in os.walk():
        for f in filenames:
            if f.endswith('.json'):
                path = os.path.join(path,f)
                tag_dict = readOneJson(path)
                if tag_dict['eventid'] not in dict_of_dict.keys():
                    dict_of_dict[tag_dict['eventid']] = [tag_dict]
                else:
                    list_from_key = dict_of_dict[tag_dict['eventid']]
                    list_from_key.append(tag_dict)


def writeDatatoDatabase():


    global number_of_rows

    dict_of_images = readFromImage()
    dict_of_texts = readFromText()

    


    
    while true:
        global flag
        if (flag == 2):
            merge_list = [dict_of_dict_of_texts, dict_of_dict_of_images]
            merge_dict = {}
            for k in dict_of_dict_of_texts.iterkeys():
                merge_dict[k] = list(merge_dict[k] for merge_dict in merge_list)












if __name__ == '__main__':

    i = 0
    j = 0
    cur = None
    conn = None

    list_length = 5000 #restricting list length for smaller database and equal no of rows and columns
    try:

        conn = connect()
        cur = conn.cursor()
        text_dict_list_json, images_dict_list_json = readAllFiles()
        while True:

            if(i >= list_length):
                break;


            if(data_format == 'csv'):
                image1  = getJson(images_dict_list_csv[i])
                text1 = getJson(text_dict_list_csv[i])

                i = i + 1

                if(i >= list_length):
                    break;

                image2 = getJson(images_dict_list_csv[i])
                text2 = getJson(text_dict_list_csv[i])


                j = j + 1
                #cur.execute( "insert into event_index(event_id,image1,image2,text1,text2) values (%s,%s, %s, %s, %s)",[j,image1, image2
                #                                                                                   , text1, text2])
                #conn.commit()
                i = i + 1

            else:
                image1 = getJson(images_dict_list_json[i])
                text1 = getJson(text_dict_list_json[i])


                i = i + 1

                if(i >= list_length):
                    break;

                image2 = getJson(images_dict_list_json[i])
                text2 = getJson(text_dict_list_json[i])

                '''
                cur.execute( "insert into event_index_main(image1,image2,text1,text2) values (%s, %s, %s, %s)",[image1, image2
                                                                                                    , text1, text2])
                conn.commit()
                i = i + 1
                '''


    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
        if cur is not None:
            cur.close()
        print('Database connection closed.')









 
 





