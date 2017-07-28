from dbconnect import connect
import psycopg2.extras

try:
    conn = connect()
    cur = conn.cursor()
    event_id = 1001
    cur.execute("select * from event_index_3 where event_id = %s", [event_id])
    rows = cur.fetchall()
    print(rows[0][3])

except (Exception, psycopg2.DatabaseError) as error:
    print(error)

finally:
    if conn is not None:
        conn.close()
    if cur is not None:
        cur.close()