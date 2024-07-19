import sqlite3,os

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'logs.db')

def combined_log_format():
    try:
        with sqlite3.connect(db_path) as s:
            s.execute('''CREATE TABLE IF NOT EXISTS clf_combined_logs
                        (  
                        File_name TEXT,
                        IP TEXT,
                        User_identifier VARCHAR(15),
                        User_ID VARCHAR(20),
                        Date_Time_Timezone TEXT,
                        Request_method TEXT,
                        Requested_URL TEXT,
                        Request_protocol VARCHAR(15),
                        Status_code INT(3),
                        Bytes INT(9),
                        Referrer VARCHAR(150),
                        User_agent TEXT);''')
    except sqlite3.Error as e:
        print("Error creating table 'clf_combined_logs':", e)

def json_log_format():
    try:
        with sqlite3.connect(db_path) as s:
            s.execute('''CREATE TABLE IF NOT EXISTS json_logs
                        (
                        Endtime TEXT,
                        Timestamp TEXT,
                        Accept TEXT,
                        Accept_language TEXT,
                        Ack_packets_in INT(9),
                        Ack_packets_out INT(9),
                        Bytes INT(15),
                        Bytes_in INT(7),
                        Bytes_out INT(7),
                        Client_IP TEXT,
                        Cached INT(7),
                        Capture_Hostname TEXT,
                        Client_rtt INT,
                        Client_rtt_packets INT,
                        Client_rtt_sum INT,
                        Connection_type TEXT,
                        Cs_pragma TEXT,
                        Cs_version TEXT,
                        Data_center_time INT(6),
                        Data_packets_in INT(6),
                        Data_packets_out INT(6),
                        Dest_content TEXT,
                        Dest_headers TEXT,
                        Dest_IP TEXT,
                        Dest_MAC TEXT,
                        Dest_port INT(7),
                        Duplicate_packets_in INT(5),
                        Duplicate_packets_out INT(5),
                        Etag TEXT,
                        Http_comment TEXT,
                        Http_content_length INT(8),
                        Http_content_type TEXT,
                        Http_method TEXT,
                        Http_user_agent TEXT,
                        Missing_packets_in INT(6),
                        Missing_packets_out INT(6),
                        Network_interface TEXT,
                        Packets_in INT(8),
                        Packets_out INT(8),
                        Reply_time INT(8),
                        Request TEXT,
                        Request_ack_time INT(6),
                        Request_time INT(6),
                        Response_ack_time INT(6),
                        Response_time INT(6),
                        Sc_date TEXT,
                        Server TEXT,
                        Server_rtt INT(5),
                        Server_rtt_packets INT(5),
                        Server_rtt_sum INT(5),
                        Site TEXT,
                        Src_headers TEXT,
                        Src_IP TEXT,
                        Src_MAC TEXT,
                        Src_port INT(6),
                        Status INT(5),
                        Time_taken INT(7),
                        Transport TEXT,
                        Uri TEXT,
                        Uri_path TEXT)''')
    except sqlite3.Error as e:
        print("Error creating table 'json_logs':", e)

combined_log_format()
json_log_format()
