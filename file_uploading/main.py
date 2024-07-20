from flask import Flask, render_template, request, session, jsonify
import parsing, json_parsing, count, sqlite3, os, logging
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'logs.db')
ERROR_LOG_PATH = os.path.join(BASE_DIR, 'error_log.txt')

# Set up logging configuration
logging.basicConfig(
    filename=ERROR_LOG_PATH,
    level=logging.ERROR,
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Define a mapping for criteria to column names in the database
criteria_mapping = {
    'client_ip': {'clf_combined_logs': 'IP', 'json_logs': 'Client_IP'},
    'status': {'clf_combined_logs': 'Status_code', 'json_logs': 'Status'},
    'response_size': {'clf_combined_logs': 'Bytes', 'json_logs': 'Bytes_out'},
    'url': {'clf_combined_logs': 'Requested_URL', 'json_logs': 'Uri'}
}

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    try:
        if request.method == 'POST':
            file = request.files['file']
            if file:
                text = request.form['text']
                file_format = request.form['file_format']
                session['log_type'] = file_format  # Store the log type in session
                session['filename_userip'] = text
                if file_format == 'json':
                    initial_count = count.row_counter_json()
                    json_parsing.parse_log_file(file, text)
                    final_count = count.row_counter_json()
                    if initial_count == final_count:
                        return "There is some issue with the file format mentioned and file type uploaded, try again!"
                    else:
                        return render_template('uploaded_successfully.html')

                elif file_format in ['combined', 'clf']:
                    initial_count = count.row_counter_clf()
                    parsing.parse_log_file(file, text)
                    final_count = count.row_counter_clf()
                    if initial_count == final_count:
                        return "There is some issue with the file format mentioned and file type uploaded, try again!"
                    else:
                        return render_template('uploaded_successfully.html')

                else:
                    return "Enter valid file type"
    except Exception as e:
        logging.error(f"Error in upload_file: {e}")
        return "An error occurred during file upload"
    return render_template('upload.html')

@app.route('/view_logs', methods=['GET','POST'])
def view_logs():
    try:
        log_type = session.get('log_type')
        if log_type == 'json':
            logs = fetch_json_logs()
            return render_template('logs_display_json.html', data=logs)
        elif log_type in ['combined', 'clf']:
            logs = fetch_combined_logs()
            return render_template('view_combined_logs.html', data=logs)
        else:
            return "Invalid log type"
    except Exception as e:
        logging.error(f"Error in view_logs: {e}")
        return "An error occurred while fetching logs"

@app.route('/filter_logs', methods=['GET','POST'])
def filter_logs():
    try:
        log_type = session.get('log_type')
        filename_userip = session.get('filename_userip')
        criteria = request.args.get('criteria')
        comparison = request.args.get('comparison')
        value = request.args.get('value')
        if criteria is None:
            return "Criteria not specified"
        table_name = 'clf_combined_logs' if log_type in ['combined', 'clf'] else 'json_logs'
        # Map the criteria to the correct column name for the current log_type
        column_name = criteria_mapping.get(criteria, {}).get(table_name)
        if column_name is None:
            return "Invalid criteria or log type"

        query_2 = f"SELECT * FROM {table_name} WHERE {column_name} {comparison} ? AND File_name = ?"
        query_1 = f"SELECT * FROM {table_name} WHERE {column_name} LIKE ? AND File_name = ?"

        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        c = conn.cursor()
        if comparison == 'contains':
            c.execute(query_1, ('%' + value + '%', filename_userip))
        else:
            c.execute(query_2, (value, filename_userip))
        data = c.fetchall()
        conn.close()
        return jsonify(data)  # Return data in JSON format for better handling
    except sqlite3.Error as e:
        logging.error(f"SQLite error in filter_logs: {e}")
        return "Error fetching data"
    except Exception as e:
        logging.error(f"Error in filter_logs: {e}")
        return "An error occurred during log filtering"

def fetch_json_logs():
    try:
        filename_userip = session.get('filename_userip')
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        c = conn.cursor()
        c.execute("SELECT * FROM json_logs WHERE File_name=?", (filename_userip,))
        data = c.fetchall()
        conn.close()
        return data
    except sqlite3.Error as e:
        logging.error(f"SQLite error in fetch_json_logs: {e}")
        return "Error fetching JSON logs"
    except Exception as e:
        logging.error(f"Error in fetch_json_logs: {e}")
        return "An error occurred while fetching JSON logs"

def fetch_combined_logs():
    try:
        filename_userip = session.get('filename_userip')
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        c = conn.cursor()
        c.execute("SELECT * FROM clf_combined_logs WHERE File_name=?", (filename_userip,))
        data = c.fetchall()
        conn.close()
        return data
    except sqlite3.Error as e:
        logging.error(f"SQLite error in fetch_combined/clf_logs: {e}")
        return "Error fetching combined/clf logs"
    except Exception as e:
        logging.error(f"Error in fetch_combined/clf_logs: {e}")
        return "An error occurred while fetching combined/clf logs"

if __name__ == '__main__':
    app.run(debug=True)
