import json
import os
from csvoperations import readFromCsv
from jsonoperations import readFromJson
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
images_path_json = '/Users/okt/Desktop/my_project/data/images_json'
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

def writeRowToDatabase(tag_dict, type):

    tag_dict = { k:v for k,v in tag_dict.items() if not (isinstance(v,bytes))}
    event_id = tag_dict['eventid']
    data_json = getJson(tag_dict)
    cur = None
    conn = None
    returnvalue = 'Success' 
    try:
        conn = connect()
        cur = conn.cursor()
        
        
            
        if(type == 'image'):
            print("now running the flex unit")
            cur.execute ("select * from event_index_main_indexed where event_id = %s and image IS NULL", [event_id])
            rows = cur.fetchall()
            if not rows:
                print("executing first time")
                cur.execute("insert into event_index_main_indexed(event_id,image) values (%s,%s) ", [event_id,data_json] )
                conn.commit()
            else:
                primary_id = rows[0][0]
                cur.execute("update event_index_main_indexed set image = %s where primary_id = %s", [data_json, primary_id])



        if(type == 'text'):
            print("now running the flex unit")
            cur.execute ("select * from event_index_main_indexed where event_id = %s and textdoc IS NULL", [event_id])
            rows = cur.fetchall()
            if not rows:
                print("executing first time")
                cur.execute("insert into event_index_main_indexed(event_id,textdoc) values (%s,%s) ", [event_id,data_json] )
                conn.commit()
            else:
                primary_id = rows[0][0]
                cur.execute("update event_index_main_indexed set textdoc = %s where primary_id = %s", [data_json, primary_id])

        
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        returnvalue = "error thrown by database"
        print(error)

    finally:

        if conn is not None:
            conn.close()
        if cur is not None:
            cur.close()
        return returnvalue

def deleteFromDatabase(path, type):

    cur = None
    conn = None
    returnvalue = 'Success' 
    try:
        conn = connect()
        cur = conn.cursor()
        if type == 'image':
            print("executing query....")
            cur.execute("""
                update event_index_main_indexed set image = (case when image->>'path' = %s then NULL else image end)
                """, [path])

        elif type == 'text':
            print("executing query....")
            cur.execute("""
                update event_index_main_indexed set textdoc = (case when textdoc->>'path' = %s then NULL else textdoc end)
                """, [path])

        else:
            returnvalue = 'wrong type supplied'

        conn.commit() 

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:

        if conn is not None:
            conn.close()
        if cur is not None:
            cur.close()
        return returnvalue








 
 





