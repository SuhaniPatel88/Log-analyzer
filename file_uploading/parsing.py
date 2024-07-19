import re,sqlite3,io,os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'logs.db')

def parse_log_file(file,text):
    pattern = r'^([^ ]+) (?:([\S]+))? (?:([^\s]+))? \[([^"]+)\] "(?:([^ ]+))? (?:(\/[^ ]+|\/))? (?:([^"]+))?" (\d+) (?:(-|\d+))? "(.*?)" "(.*?)"$'
    s = sqlite3.connect(DB_PATH)
    file_contents_str = file.read().decode('utf-8')
    for line in file_contents_str.splitlines():
        match = re.match(pattern, line)
        if match:
            file_name = text
            ip_address = match.group(1)
            user_identifier = match.group(2)
            user_id = match.group(3)
            date_time = match.group(4)
            request_method = match.group(5)
            requested_url = match.group(6)
            request_protocol = match.group(7)
            status_code = match.group(8)
            bytes = match.group(9)
            referrer = match.group(10)
            user_agent = match.group(11)
            s.execute("INSERT INTO clf_combined_logs (File_name,IP,User_identifier,User_ID,Date_Time_Timezone,Request_method,Requested_URL,Request_protocol,Status_code,Bytes,Referrer,User_agent) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",(file_name,ip_address,user_identifier,user_id,date_time,request_method,requested_url,request_protocol,status_code,bytes,referrer,user_agent))
        else:
            pattern_exception1 = r'^([^ ]+) (?:([^\s]+))? (?:([^\s]+))? \[([^"]+)\] "([^ ]+) (\/[^ ]+) ([^"]+)" (\d+) (?:(-|\d+))?$'
            match1 = re.match(pattern_exception1, line)
            if match1:
                file_name = text
                ip_address = match1.group(1)
                user_identifier = match1.group(2)
                user_id = match1.group(3)
                date_time = match1.group(4)
                request_method = match1.group(5)
                requested_url = match1.group(6)
                request_protocol = match1.group(7)
                status_code = match1.group(8)
                bytes = match1.group(9)
                s.execute("INSERT INTO clf_combined_logs (File_name,IP,User_identifier,User_ID,Date_Time_Timezone,Request_method,Requested_URL,Request_protocol,Status_code,Bytes) VALUES (?,?,?,?,?,?,?,?,?,?)",(file_name,ip_address,user_identifier,user_id,date_time,request_method,requested_url,request_protocol,status_code,bytes))
            else:
                print("Skipped line:", line.strip())
                continue
    s.commit()
    s.close()

