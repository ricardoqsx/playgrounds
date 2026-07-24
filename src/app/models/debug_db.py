import json

from app.models.db import get_conn


def serialize_value(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return value


def create_request_logs():
    with get_conn() as con:
        cur = con.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS request_logs(
                id INT AUTO_INCREMENT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                method VARCHAR(10),
                path TEXT,
                remote_addr VARCHAR(45),
                x_forwarded_for TEXT,
                x_real_ip VARCHAR(45),
                cf_connecting_ip VARCHAR(45),
                user_agent_raw TEXT,
                user_agent_platform VARCHAR(100),
                user_agent_browser VARCHAR(100),
                user_agent_version VARCHAR(100),
                ip_country_code VARCHAR(10),
                ip_country_name VARCHAR(100),
                request_headers JSON,
                request_body LONGTEXT,
                response_status INT,
                response_headers JSON,
                response_body LONGTEXT,
                duration_ms DECIMAL(10, 2)
            )''')


def insert_request_log(
    method,
    path,
    remote_addr,
    x_forwarded_for,
    x_real_ip,
    cf_connecting_ip,
    user_agent_raw,
    user_agent_platform,
    user_agent_browser,
    user_agent_version,
    ip_country_code,
    ip_country_name,
    request_headers,
    request_body,
    response_status,
    response_headers,
    response_body,
    duration_ms,
):
    with get_conn() as con:
        cur = con.cursor()
        cur.execute(
            '''
            INSERT INTO request_logs(
                method,
                path,
                remote_addr,
                x_forwarded_for,
                x_real_ip,
                cf_connecting_ip,
                user_agent_raw,
                user_agent_platform,
                user_agent_browser,
                user_agent_version,
                ip_country_code,
                ip_country_name,
                request_headers,
                serialize_value(request_body),
                response_status,
                response_headers,
                serialize_value(response_body),
                duration_ms
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''',
            (
                method,
                path,
                remote_addr,
                x_forwarded_for,
                x_real_ip,
                cf_connecting_ip,
                user_agent_raw,
                user_agent_platform,
                user_agent_browser,
                user_agent_version,
                ip_country_code,
                ip_country_name,
                json.dumps(request_headers, ensure_ascii=False),
                request_body,
                response_status,
                json.dumps(response_headers, ensure_ascii=False),
                response_body,
                duration_ms,
            ),
        )
