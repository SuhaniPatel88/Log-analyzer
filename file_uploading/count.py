import sqlite3,os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'logs.db')

def row_counter_json():
 conn = sqlite3.connect(DB_PATH)
 cursor = conn.cursor()

 table_name = 'json_logs'
 query = f"SELECT COUNT(*) FROM {table_name}"
 cursor.execute(query)
 result = cursor.fetchone()
 row_count = result[0]

 cursor.close()
 conn.close()

 #print(f"The {table_name} table has {row_count} rows.")
 return row_count



def row_counter_clf():
 conn = sqlite3.connect(DB_PATH)
 cursor = conn.cursor()

 table_name = 'clf_combined_logs'
 query = f"SELECT COUNT(*) FROM {table_name}"
 cursor.execute(query)
 result = cursor.fetchone()
 row_count = result[0]

 cursor.close()
 conn.close()

 #print(f"The {table_name} table has {row_count} rows.")
 return row_count