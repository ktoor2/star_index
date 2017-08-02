from dbconnect import connect
import psycopg2

"""
sample queries to check db connection
"""

def create_table():
	conn = None
	try:
		conn = connect()
		cursor = conn.cursor()

		command=(
			"""
			CREATE TABLE event_index_main_test(
			primary_id serial PRIMARY KEY,
			event_id int NOT NULL,
			event_time timestamp NOT NULL DEFAULT current_timestamp,
			image jsonb, textdoc jsonb 
			)
		"""	
		)
		result = cursor.execute(command)		
		print(result)
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)

	finally:
		if conn is not None:
			conn.commit()
			conn.close()
			print("database connection closed")


if __name__ == '__main__':
    create_table()


