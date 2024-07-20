import sqlite3,os,logging


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'logs.db')
LOG_FILE_PATH = os.path.join(BASE_DIR, 'error_log.txt')

logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.ERROR,
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def row_counter_json():
    conn = None
    cursor = None
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        cursor = conn.cursor()

        table_name = 'json_logs'
        query = f"SELECT COUNT(*) FROM {table_name}"
        cursor.execute(query)
        result = cursor.fetchone()
        row_count = result[0]

    except sqlite3.Error as e:
        logging.error(f"An error occurred while counting rows in json_logs: {e}")
        raise

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return row_count

def row_counter_clf():
    conn = None
    cursor = None
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        cursor = conn.cursor()

        table_name = 'clf_combined_logs'
        query = f"SELECT COUNT(*) FROM {table_name}"
        cursor.execute(query)
        result = cursor.fetchone()
        row_count = result[0]

    except sqlite3.Error as e:
        logging.error(f"An error occurred while counting rows in clf_combined_logs: {e}")
        raise

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return row_count
