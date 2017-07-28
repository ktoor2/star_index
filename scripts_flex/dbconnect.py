import psycopg2
from readconfig import config
 




def connect():
    """ 
    Connect to the PostgreSQL database server

     """
    conn = None

    # read connection parameters
    params = config()
    print(params)
 
        # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params)

    return conn    

    