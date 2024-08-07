import json
import sqlite3
import os
import logging
from datetime import datetime

# Setup logging
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'logs.db')
LOG_FILE_PATH = os.path.join(BASE_DIR, 'error_log.txt')

logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.ERROR,
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def parse_log_file(file, text):
    conn = None
    cursor = None
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        cursor = conn.cursor()

        file_contents_str = file.read().decode('utf-8')
        for line in file_contents_str.splitlines():
            try:
                file_name = text
                data = json.loads(line)
                endtime = data.get("endtime", "-")
                timestamp = data.get("timestamp", "-")
                accept = data.get("accept", "-")
                accept_language = data.get("accept_language", "default_value")
                ack_packets_in = data.get("ack_packets_in", "-")
                ack_packets_out = data.get("ack_packets_out", "-")
                bytes = data.get("bytes", "-")
                bytes_in = data.get("bytes_in", "-")
                bytes_out = data.get("bytes_out", "-")
                c_ip = data.get("c_ip", "-")
                cached = data.get("cached", "-")
                capture_hostname = data.get("capture_hostname", "-")
                client_rtt = data.get("client_rtt", "-")
                client_rtt_packets = data.get("client_rtt_packets", "-")
                client_rtt_sum = data.get("client_rtt_sum", "-")
                connection_type = data.get("connection_type", "-")
                cs_pragma = data.get("cs_pragma", "-")
                cs_version = ",".join(data.get("cs_version", [])) if isinstance(data.get("cs_version", []), list) else data.get("cs_version", "-")
                data_center_time = data.get("data_center_time", "-")
                data_packets_in = data.get("data_packets_in", "-")
                data_packets_out = data.get("data_packets_out", "-")
                dest_content = data.get("dest_content", "-")
                dest_headers = data.get("dest_headers", "-")
                dest_ip = data.get("dest_ip", "-")
                dest_mac = data.get("dest_mac", "-")
                dest_port = data.get("dest_port", "-")
                duplicate_packets_in = data.get("duplicate_packets_in", "-")
                duplicate_packets_out = data.get("duplicate_packets_out", "-")
                etag = data.get("etag", "-")
                http_comment = data.get("http_comment", "-")
                http_content_length = data.get("http_content_length", "-")
                http_content_type = data.get("http_content_type", "-")
                http_method = data.get("http_method", "-")
                http_user_agent = data.get("http_user_agent", "-")
                missing_packets_in = data.get("missing_packets_in", "-")
                missing_packets_out = data.get("missing_packets_out", "-")
                network_interface = data.get("network_interface", "-")
                packets_in = data.get("packets_in", "-")
                packets_out = data.get("packets_out", "-")
                reply_time = data.get("reply_time", "-")
                request = data.get("request", "-")
                request_ack_time = data.get("request_ack_time", "-")
                request_time = data.get("request_time", "-")
                response_ack_time = data.get("response_ack_time", "-")
                response_time = data.get("response_time", "-")
                sc_date = data.get("sc_date", "-")
                server = data.get("server", "-")
                server_rtt = data.get("server_rtt", "-")
                server_rtt_packets = data.get("server_rtt_packets", "-")
                server_rtt_sum = data.get("server_rtt_sum", "-")
                site = data.get("site", "-")
                src_headers = data.get("src_headers", "-")
                src_ip = data.get("src_ip", "-")
                src_mac = data.get("src_mac", "-")
                src_port = data.get("src_port", "-")
                status = data.get("status", "-")
                time_taken = data.get("time_taken", "-")
                transport = data.get("transport", "-")
                uri = data.get("uri", "-")
                uri_path = data.get("uri_path", "-")

                cursor.execute("""
                    INSERT INTO json_logs (
                        File_name, Endtime, Timestamp, Accept, Accept_language, Ack_packets_in, Ack_packets_out,
                        Bytes, Bytes_in, Bytes_out, Client_IP, Cached, Capture_Hostname, Client_rtt, Client_rtt_packets,
                        Client_rtt_sum, Connection_type, Cs_pragma, Cs_version, Data_center_time, Data_packets_in,
                        Data_packets_out, Dest_content, Dest_headers, Dest_IP, Dest_MAC, Dest_port, Duplicate_packets_in,
                        Duplicate_packets_out, Etag, Http_comment, Http_content_length, Http_content_type, Http_method,
                        Http_user_agent, Missing_packets_in, Missing_packets_out, Network_interface, Packets_in,
                        Packets_out, Reply_time, Request, Request_ack_time, Request_time, Response_ack_time, Response_time,
                        Sc_date, Server, Server_rtt, Server_rtt_packets, Server_rtt_sum, Site, Src_headers, Src_IP,
                        Src_MAC, Src_port, Status, Time_taken, Transport, Uri, Uri_path
                    ) VALUES (
                        ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
                    );""", (
                        file_name, endtime, timestamp, accept, accept_language, ack_packets_in, ack_packets_out, bytes,
                        bytes_in, bytes_out, c_ip, cached, capture_hostname, client_rtt, client_rtt_packets, client_rtt_sum,
                        connection_type, cs_pragma, cs_version, data_center_time, data_packets_in, data_packets_out,
                        dest_content, dest_headers, dest_ip, dest_mac, dest_port, duplicate_packets_in,
                        duplicate_packets_out, etag, http_comment, http_content_length, http_content_type, http_method,
                        http_user_agent, missing_packets_in, missing_packets_out, network_interface, packets_in,
                        packets_out, reply_time, request, request_ack_time, request_time, response_ack_time, response_time,
                        sc_date, server, server_rtt, server_rtt_packets, server_rtt_sum, site, src_headers, src_ip,
                        src_mac, src_port, status, time_taken, transport, uri, uri_path
                    )
                )
            except json.JSONDecodeError:
                continue

        conn.commit()

    except sqlite3.Error as e:
        logging.error(f"An error occurred: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
