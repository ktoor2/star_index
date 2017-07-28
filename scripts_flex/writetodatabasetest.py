import json
import os
from csvoperations import readFromCsv
from dbconnect import connect
import psycopg2.extras


def getJson(dict):
	"""
	Converts dictionary to a json string and retruns
	"""
	dict_text = json.dumps(dict)
	return dict_text


images_path = '/Users/okt/Desktop/my_project/data/images_meta'
text_path = '/Users/okt/Desktop/my_project/data/text_meta'

images_dict_list = readFromCsv(images_path)
text_dict_list = readFromCsv(text_path)
list_length = len(images_dict_list)


i = 0
j = 0
cur = None
conn = None
try:

	conn = connect()
	cur = conn.cursor()
	while True:

		if(i >= list_length):
			break;

		image1  = images_dict_list[i]
		text1 = text_dict_list[i]
		print(image1)

		i = i + 1

		if(i >= list_length):
			break;

		image2 = images_dict_list[i]
		text2 = text_dict_list[i]


		j = j + 1
		cur.execute( "insert into event_index(event_id,image1,image2,text1,text2) values (%s,%s, %s, %s, %s)",[j,psycopg2.extras.Json(image1), psycopg2.extras.Json(image2)
																							, psycopg2.extras.Json(text1), psycopg2.extras.Json(text2)])
		conn.commit()
		i = i + 1



except (Exception, psycopg2.DatabaseError) as error:
	print(error)

finally:
    if conn is not None:
    	conn.close()
    if cur is not None:
    	cur.close()
    print('Database connection closed.')





