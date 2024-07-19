from flask import Flask, render_template, request, session, jsonify
import parsing, json_parsing, count, sqlite3,os


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'logs.db')


# Define a mapping for criteria to column names in the database
criteria_mapping = {
    'client_ip': {'clf_combined_logs': 'IP', 'json_logs': 'Client_IP'},
    'status': {'clf_combined_logs': 'Status_code', 'json_logs': 'Status'},
    'response_size': {'clf_combined_logs': 'Bytes', 'json_logs': 'Bytes_out'},
    'url': {'clf_combined_logs': 'Requested_URL', 'json_logs': 'Uri'}
}

@app.route('/', methods=['GET', 'POST'])
def upload_file():
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

            elif file_format == 'combined' or file_format == 'clf':
                initial_count = count.row_counter_clf()
                parsing.parse_log_file(file, text)
                final_count = count.row_counter_clf()
                if initial_count == final_count:
                    return "There is some issue with the file format mentioned and file type uploaded, try again!"
                else:
                    return render_template('uploaded_successfully.html')

            else:
                return "Enter valid file type"
    return render_template('upload.html')

@app.route('/view_logs', methods=['GET','POST'])
def view_logs():
    log_type = session.get('log_type')
    if log_type == 'json':
        logs = fetch_json_logs()
        return render_template('logs_display_json.html', data=logs)
    elif log_type in ['combined', 'clf']:
        logs = fetch_combined_logs()
        return render_template('view_combined_logs.html', data=logs)
    else:
        return "Invalid log type"

@app.route('/filter_logs', methods=['GET','POST'])
def filter_logs():
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
    '''print(table_name)
    print(log_type)
    print(column_name)
    print(comparison)
    print(value)
    print(filename_userip)'''

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        if comparison=='contains':
            c.execute(query_1,('%'+value+'%',filename_userip))
        else:
            c.execute(query_2,(value,filename_userip))
        data = c.fetchall()
        conn.close()
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return "Error fetching data"
    

    if log_type == 'json':
        return data
    elif log_type in ['combined', 'clf']:
        return data
    else:
        return "Invalid log type"
    

def fetch_json_logs():
    filename_userip = session.get('filename_userip')
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM json_logs WHERE File_name=?",(filename_userip,))
    data = c.fetchall()
    conn.close()
    return data

def fetch_combined_logs():
    filename_userip = session.get('filename_userip')
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM clf_combined_logs WHERE File_name=?",(filename_userip,))
    data = c.fetchall()
    conn.close()
    return data

if __name__ == '__main__':
    app.run(debug=True)
