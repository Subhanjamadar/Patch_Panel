import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS
from models import Session, PatchPort
from switch_controller import set_switch_port_state
import pandas as pd

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

import pandas as pd
from flask import jsonify

@app.route("/vlans", methods=["GET"])
def get_vlans():
    floor_name = request.args.get("floor")  # e.g., "1st Floor"
    if not floor_name:
        return jsonify({"error": "Missing 'floor' query parameter"}), 400

    df = pd.read_excel("VLANS.xlsx")

    # Normalize column headers (in case of Excel formatting issues)
    df.columns = df.columns.str.strip()

    # Filter rows based on the floor name
    filtered_df = df[df["Floor Name"].str.strip() == floor_name.strip()]

    # Extract unique VLAN IDs
    vlan_list = filtered_df["VLAN ID"].dropna().astype(int).astype(str).unique().tolist()
    
    return jsonify(sorted(vlan_list))

@app.route('/')
def index():
    return "Patch Panel API is running"

@app.route("/switches", methods=["GET"])
def get_switches():
    switches = {
        "BB": {
            "floor": "1st",
            "password": "10fwIB1@E0r!$#",
            "devices": {
                "BB01": "10.22.74.11",
                "BB03": "10.22.74.12",
                "BB05": "10.22.74.13",
                "BB07": "10.22.74.14",
                "BB09": "10.22.74.15",
                "BB11": "10.22.74.16",
                "BB13": "10.22.74.17",
                "BB15": "10.22.74.18",
                "BBHD02": "10.22.74.19",
                "BBHD04": "10.22.74.20",
                "BB18": "10.22.74.22",
                "BB20": "10.22.74.23",
                "BB22": "10.22.74.24",
                "BB24": "10.22.74.25",
                "BB26": "10.22.74.26",
                "BB27": "10.22.74.158",
                "ATCBB28": "10.22.74.28",
                "ATCBB30": "10.22.74.29",
                "ATCBB32": "10.22.74.30"              
            }
        }
    }
    return jsonify(switches)

@app.route('/ports', methods=['GET'])
def list_ports():
    session = Session()
    ports = session.query(PatchPort).all()
    return jsonify([
        {"name": p.name, "switch_port": p.switch_port, "enabled": p.enabled, "vlan": p.vlan}
        for p in ports
    ])

# Flask route to get patching status
@app.route("/patch-status/<patch_serial>")
def check_patch_status(patch_serial):
    conn = sqlite3.connect("techdirect_requests.db")
    c = conn.cursor()
    c.execute("SELECT status FROM requests WHERE patch_panel_serial=?", (patch_serial,))
    row = c.fetchone()
    conn.close()

    return jsonify({"status": row[0] if row else "pending"})


@app.route('/ports/<name>', methods=['POST'])
def toggle_port(name):
    enable = request.json.get('enable')
    vlan = request.json.get('vlan')
    ip = request.json.get('ip')
    password = request.json.get('password')

    session = Session()
    port = session.query(PatchPort).get(name)

    if port:
        set_switch_port_state(port.switch_port, enable, vlan, ip, password)
        port.enabled = enable
        if vlan:
            port.vlan = vlan
        session.commit()
        return jsonify({"status": "success"}), 200


    return jsonify({"error": "Port not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
