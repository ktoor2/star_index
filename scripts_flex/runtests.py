import os 
from dbconnect import connect
import psycopg2
import sys
import re



"""
Reads queries from a text document and runs them 
Author: Kunwar Singh
"""
'''
arg_list = sys.argv
cli_query = arg_list[1]
print('running' + cli_query)
'''

def getQueries(path):
    with os.open(path, 'r') as fw:
        queries = fw.readLines()
        queries = [line.rstrip('\n') for line in queries]

    return queries




def runQueries(query, command = 1):
    
    exec_time = 0
    try:
        conn = connect()
        cur = conn.cursor()
        if(command == 0):
            exex_list=[]
           # path = '/Users/okt/Desktop/my_project/scripts/queries.txt'
            queries = getQueries(path)
            for query in queries:
                cur.execute(query)
                rows = cur.fetchall()
                egex = "\d+\.\d+"
                exec_time_string = re.findall(regex, rows[4][0])
                exec_time = float(exec_time_string[0])
                exec_list.append(exec_time)
                
        else:
            print("in business")
            cur.execute(query)
            rows = cur.fetchall()
            print(rows)
            regex = "\d+\.\d+"
            '''
            search the execution tuple in the output. In this case it is at position 7. change the position accordingly with your query
            '''
            exec_time_string = re.findall(regex, rows[4][0])
            exec_time = float(exec_time_string[0])
            


    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
        if cur is not None:
            cur.close()

    return exec_time


time_list = []
for x in range(1,20):
    time_list.append(runQueries("Explain analyze Select textdoc from columnar_index where textdoc->>'primary' like '%ati%' or textdoc->>'secondary' like '%ati%' or textdoc->>'tertiary' like '%ati%';"))

print(sum(time_list)/len(time_list))

'''
time = runQueries("explain analyze select * from event_index_3 where text1->>'primary'= 'edu' or text1->>'secondary'= 'edu' or text1->>'tertiary' = 'edu' order by case when text1 @>'{\"primary\":\"edu\"}' then 1 when text1 @>'{\"secondary\":\"edu\"}' then 2 else 3 end ")
print(time)
'''     



