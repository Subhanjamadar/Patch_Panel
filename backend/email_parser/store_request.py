import sqlite3

def save_request(parsed_data):
    conn = sqlite3.connect("techdirect_requests.db")
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_time TEXT,
            rack_location TEXT,
            ip_addresses TEXT,
            vlan TEXT,
            patch_panel_serial TEXT,
            status TEXT DEFAULT 'pending'
        )
    ''')

    c.execute('''
        INSERT INTO requests (request_time, rack_location, ip_addresses, vlan, patch_panel_serial)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        parsed_data.get("request_time"),
        parsed_data.get("rack_location"),
        parsed_data.get("ip_addresses"),
        parsed_data.get("vlan"),
        parsed_data.get("patch_panel_serial"),
    ))

    conn.commit()
    conn.close()
