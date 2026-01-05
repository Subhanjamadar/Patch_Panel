import sqlite3
from flask import Flask, jsonify, make_response,request
from flask_cors import CORS
from models import Session, PatchPort
from switch_controller import set_switch_port_state
import pandas as pd
from model_cache import ip_model_map

app = Flask(__name__)

# Configure CORS with comprehensive settings
cors = CORS(app, resources={
    r"/*": {
        "origins": "http://localhost:3000",
        "methods": ["GET", "POST", "PATCH", "OPTIONS", "HEAD", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization", "Cache-Control", "Pragma"],
        "expose_headers": ["Content-Type", "Content-Length"],
        "supports_credentials": True,
        "max_age": 600
    }
})

# Load mapping from Excel at startup
def load_switch_models():
    try:
        # Try to load from Excel first
        df = pd.read_excel("EOR Switch Details - Current.xlsx")
        df.columns = df.columns.str.strip()
        for _, row in df.iterrows():
            ip = str(row["EOR IP Address"]).strip()
            model = str(row["Model Name"]).strip()
            ip_model_map[ip] = model
        print("Successfully loaded switch models from Excel file")
    except Exception as e:
        print(f"Warning: Could not load switch models from Excel: {str(e)}")
        print("Falling back to hardcoded switch models")
        # Hardcoded switch models as fallback
        hardcoded_models = {
            "10.22.74.11": "Aruba 3810M 48G",
            "10.22.74.12": "Aruba 3810M 48G",
            "10.22.74.13": "Aruba 3810M 48G",
            "10.22.74.14": "Aruba 3810M 48G",
            "10.22.74.15": "Aruba 3810M 48G",
            "10.22.74.16": "Aruba 3810M 48G",
            "10.22.74.17": "Aruba 3810M 48G",
            "10.22.74.18": "Aruba 3810M 48G",
            "10.22.74.19": "Aruba 3810M 48G",
            "10.22.74.20": "Aruba 3810M 48G",
            "10.22.74.22": "Aruba 3810M 48G",
            "10.22.74.23": "Aruba 3810M 48G",
            "10.22.74.24": "Aruba 3810M 48G",
            "10.22.74.25": "Aruba 3810M 48G",
            "10.22.74.26": "Aruba 3810M 48G",
            "10.22.74.158": "Aruba 3810M 48G",
            "10.22.74.28": "Aruba 3810M 48G",
            "10.22.74.29": "Aruba 3810M 48G",
            "10.22.74.30": "Aruba 3810M 48G",
            "10.22.75.11": "Aruba 3810M 48G",
            "10.22.75.12": "Aruba 3810M 48G",
            "10.22.75.13": "Aruba 3810M 48G",
            "10.22.75.14": "Aruba 3810M 48G",
            "10.22.75.15": "Aruba 3810M 48G",
            "10.22.75.16": "Aruba 3810M 48G",
            "10.22.75.17": "Aruba 3810M 48G",
            "10.22.75.18": "Aruba 3810M 48G",
            "10.22.75.19": "Aruba 3810M 48G",
            "10.22.75.20": "Aruba 3810M 48G",
            "10.22.75.22": "Aruba 3810M 48G",
            "10.22.75.23": "Aruba 3810M 48G",
            "10.22.75.24": "Aruba 3810M 48G",
            "10.22.75.25": "Aruba 3810M 48G",
            "10.22.75.26": "Aruba 3810M 48G",
            "16.184.2.11": "Aruba 3810M 48G",
            "16.184.2.12": "Aruba 3810M 48G",
            "16.184.2.13": "Aruba 3810M 48G",
            "16.184.2.14": "Aruba 3810M 48G",
            "16.184.2.15": "Aruba 3810M 48G",
            "16.184.2.16": "Aruba 3810M 48G",
            "16.184.2.19": "Aruba 3810M 48G",
            "16.184.2.20": "Aruba 3810M 48G",
            "16.184.2.18": "Aruba 3810M 48G",
            "16.184.2.21": "Aruba 3810M 48G",
            "16.184.2.22": "Aruba 3810M 48G",
            "16.184.2.23": "Aruba 3810M 48G",
            "16.184.2.24": "Aruba 3810M 48G",
            "16.184.2.25": "Aruba 3810M 48G",
            "16.184.2.26": "Aruba 3810M 48G",
            "16.184.1.11": "Aruba 3810M 48G",
            "16.184.1.12": "Aruba 3810M 48G",
            "16.184.1.13": "Aruba 3810M 48G",
            "16.184.1.14": "Aruba 3810M 48G",
            "16.184.1.15": "Aruba 3810M 48G",
            "16.184.1.16": "Aruba 3810M 48G",
            "16.184.1.17": "Aruba 3810M 48G",
            "16.184.1.18": "Aruba 3810M 48G",
            "16.184.1.19": "Aruba 3810M 48G",
            "16.184.1.20": "Aruba 3810M 48G",
            "16.184.1.21": "Aruba 3810M 48G",
            "16.184.1.22": "Aruba 3810M 48G",
            "16.184.1.23": "Aruba 3810M 48G",
            "16.184.1.24": "Aruba 3810M 48G",
            "16.184.1.25": "Aruba 3810M 48G",
            "16.184.1.26": "Aruba 3810M 48G",
            "16.184.1.27": "Aruba 3810M 48G",
            "16.184.1.28": "Aruba 3810M 48G",
            "16.184.0.11": "Aruba 3810M 48G",
            "16.184.0.12": "Aruba 3810M 48G",
            "16.184.0.13": "Aruba 3810M 48G",
            "16.184.0.16": "Aruba 3810M 48G",
            "16.184.0.17": "Aruba 3810M 48G",
            "16.184.0.9": "Aruba 3810M 48G",
            "16.184.0.10": "Aruba 3810M 48G",
            "16.184.0.19": "Aruba 3810M 48G",
            "16.184.0.20": "Aruba 3810M 48G",
            "16.184.0.21": "Aruba 3810M 48G",
            "16.184.0.22": "Aruba 3810M 48G",
            "16.184.0.23": "Aruba 3810M 48G",
            "16.184.0.24": "Aruba 3810M 48G",
            "16.184.0.25": "Aruba 3810M 48G",
            "16.184.0.26": "Aruba 3810M 48G",
            "16.184.0.27": "Aruba 3810M 48G",
            "16.184.0.28": "Aruba 3810M 48G"
        }
        ip_model_map.update(hardcoded_models)
        print(f"Loaded {len(hardcoded_models)} hardcoded switch models")

load_switch_models()

@app.route("/vlans", methods=["GET"])
def get_vlans():
    floor_name = request.args.get("floor")
    if not floor_name:
        return jsonify({"error": "Missing 'floor' query parameter"}), 400

    df = pd.read_excel("VLANS.xlsx")
    df.columns = df.columns.str.strip()
    filtered_df = df[df["Floor Name"].str.strip() == floor_name.strip()]
    vlan_list = filtered_df["VLAN ID"].dropna().astype(int).astype(str).unique().tolist()
    return jsonify(sorted(vlan_list))

@app.route('/api/switch/<switch_ip>/interfaces', methods=['GET'])
def get_switch_interfaces_route(switch_ip):
    """
    Get interface information for a specific switch.
    
    Args:
        switch_ip (str): IP address of the switch
        
    Returns:
        JSON: Interface information including line modules and total interfaces
    """
    from interface import get_line_modules_and_interfaces
    
    # Get credentials from environment variables
    username = os.getenv('SWITCH_USERNAME', 'admin')
    password = os.getenv('SWITCH_PASSWORD')
    
    if not password:
        return jsonify({
            "status": "error",
            "message": "Switch password not configured"
        }), 500
    
    # Get interface data
    result = get_line_modules_and_interfaces(switch_ip, username, password)
    
    if result.get("status") == "error":
        return jsonify({
            "error": result.get("message", "Failed to get interface information"),
            "ip": switch_ip
        }), 500
        
    return jsonify(result)
    
@app.route('/')
def index():
    return "Patch Panel API is running"

# In app.py, update the handle_port function to add more detailed error logging
@app.route('/ports/<path:port_id>', methods=['OPTIONS', 'PATCH', 'POST'])
def handle_port(port_id):
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400

        print(f"\n=== Received request to update port {port_id} ===")
        print(f"Request data: {data}")

        # Get switch IP and password from request
        switch_ip = data.get('ip')
        switch_password = data.get('password')
        
        if not switch_ip or not switch_password:
            error_msg = "Switch IP and password are required"
            print(f"Error: {error_msg}")
            return jsonify({"status": "error", "message": error_msg}), 400

        # Update switch configuration first
        try:
            from switch_config import configure_switch_port
            print(f"Attempting to configure switch {switch_ip} port {port_id} with VLAN {data.get('vlan')}")
            
            result = configure_switch_port(
                switch_ip=switch_ip,
                port=port_id,
                vlan=data.get('vlan'),
                enabled=data.get('enable', True),
                password=switch_password
            )
            
            if not result.get('success', False):
                error_msg = f"Switch configuration failed: {result.get('message', 'Unknown error')}"
                print(f"Error: {error_msg}")
                return jsonify({"status": "error", "message": error_msg}), 500
                
            print("Switch configuration successful")
            
        except Exception as e:
            error_msg = f"Error in switch configuration: {str(e)}"
            print(f"Error: {error_msg}")
            import traceback
            traceback.print_exc()  # This will print the full traceback
            return jsonify({"status": "error", "message": error_msg}), 500

        # Update database
        session = Session()
        try:
            port = session.query(PatchPort).filter_by(switch_port=port_id).first()
            if not port:
                port = session.query(PatchPort).filter_by(name=port_id).first()
            
            if not port:
                port = PatchPort(
                    name=port_id,
                    switch_port=port_id,
                    vlan=data.get('vlan'),
                    enabled=data.get('enable', True)
                )
                session.add(port)
                print(f"Created new port entry for {port_id}")

            if 'vlan' in data:
                port.vlan = data['vlan']
            if 'enable' in data:
                port.enabled = data['enable']
            
            session.commit()
            print(f"Database updated for port {port_id}")

            return jsonify({
                "status": "success",
                "port": port_id,
                "vlan": port.vlan,
                "enabled": port.enabled
            })

        except Exception as e:
            session.rollback()
            error_msg = f"Database error: {str(e)}"
            print(f"Error: {error_msg}")
            import traceback
            traceback.print_exc()
            return jsonify({"status": "error", "message": error_msg}), 500
        finally:
            session.close()

    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        print(f"Error: {error_msg}")
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": error_msg}), 500
        
@app.route('/ports', methods=['OPTIONS'])
def handle_ports_options():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization, Cache-Control, Pragma")
    response.headers.add("Access-Control-Allow-Methods", "GET, OPTIONS")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    return response
    
@app.route('/ports', methods=['GET'])
def list_ports():
    """Return full physical interfaces, merged with DB data if available."""
    ip = request.args.get("ip")
    if not ip:
        return jsonify({"error": "Missing 'ip' query parameter"}), 400

    print(f"\n=== Received request for IP: {ip} ===")
    print(f"IP to model mapping: {ip_model_map}")
    
    model = ip_model_map.get(ip)
    print(f"Found model for IP {ip}: {model}")
    
    if not model:
        error_msg = f"Switch model for {ip} not found in ip_model_map"
        print(error_msg)
        return jsonify({"error": error_msg}), 404

    # Generate physical interfaces based on switch model
    print(f"\n=== Debug: Starting port generation for model: {model} ===")
    print(f"IP: {ip}, Model: {model}")
    
    if "6410" in model:
        # For 6410 switches, generate ports in 1/3/X format (48 ports) starting from 1/3/1
        generated_ports = [{"name": f"1/3/{i}", "enabled": True, "switch_port": f"1/3/{i}"} for i in range(1, 49)]
        print(f"Using 6410 template - generated {len(generated_ports)} ports starting from 1/3/1")
    elif "5900AF-48G" in model:
        # For 5900AF-48G, use GE1/0/X format
        generated_ports = [{"name": f"GE1/0/{i}", "enabled": True, "switch_port": f"GE1/0/{i}"} for i in range(1, 49)]
        print(f"Using 5900AF-48G template - generated {len(generated_ports)} ports")
    elif "3810M" in model:
        # For 3810M, use 1/1/X format
        generated_ports = [{"name": f"1/1/{i}", "enabled": True, "switch_port": f"1/1/{i}"} for i in range(1, 49)]
        print(f"Using 3810M template - generated {len(generated_ports)} ports")
    elif "5412" in model or "5400R" in model:
        # For 5412/5400R, use numeric ports 1-96
        generated_ports = [{"name": str(i), "enabled": True, "switch_port": str(i)} for i in range(1, 97)]
        print(f"Using 5412/5400R template - generated {len(generated_ports)} ports")
    else:
        # Default to 48 ports in 1/1/X format
        generated_ports = [{"name": f"1/1/{i}", "enabled": True, "switch_port": f"1/1/{i}"} for i in range(1, 49)]
        print(f"Using default template - generated {len(generated_ports)} ports")

    print(f"\n=== Debug: Generated Ports ===")
    print(f"Number of generated ports: {len(generated_ports)}")
    if generated_ports:
        print(f"First 5 generated ports: {[p['name'] for p in generated_ports[:5]]}...")
        
    # Get any existing port status from the database
    session = Session()
    try:
        db_ports = session.query(PatchPort).filter(PatchPort.switch_ip == ip).all()
        print(f"\n=== Debug: Database Ports ===")
        print(f"Number of database ports: {len(db_ports)}")
        if db_ports:
            print(f"First 5 database ports: {[p.switch_port for p in db_ports[:5]]}...")
            
        db_port_map = {p.switch_port: p for p in db_ports}
        
        # Merge with generated ports
        filtered_ports = []
        for port in generated_ports:
            # Skip ports that match unwanted patterns
            if 'BB020200' in port['name']:
                print(f"Skipping port (unwanted pattern): {port['name']}")
                continue
                
            if port["switch_port"] in db_port_map:
                dbp = db_port_map[port["switch_port"]]
                port["enabled"] = bool(dbp.enabled) if dbp.enabled is not None else False
                port["vlan"] = int(dbp.vlan) if dbp.vlan is not None else None
                print(f"Using DB settings for port {port['name']}: enabled={port['enabled']}, vlan={port['vlan']}")
            else:
                port["enabled"] = port.get("enabled", False)
                port["vlan"] = port.get("vlan")
                print(f"Using default settings for port {port['name']}")
                
            filtered_ports.append(port)
            
        print(f"\nReturning {len(filtered_ports)} ports after filtering")
        if filtered_ports:
            print(f"First few ports: {[p['name'] for p in filtered_ports[:5]]}...")
            
        return jsonify(filtered_ports)
        
    except Exception as e:
        print(f"Error querying database: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

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
    port = session.get(PatchPort, name)

    if port:
        # DB PatchPort
        interface_name = port.switch_port.name if hasattr(port.switch_port, "name") else port.switch_port
        set_switch_port_state(interface_name, enable, vlan, ip, password)
        port.enabled = enable
        if vlan:
            port.vlan = vlan
        session.commit()
        return jsonify({"status": "success"}), 200
    else:
        # Raw switch interface (like 1/3/12 or GE1/0/5)
        set_switch_port_state(name, enable, vlan, ip, password)
        # optionally persist this in DB for future calls:
        # new_port = PatchPort(name=name, switch_port=name, enabled=enable, vlan=vlan)
        # session.add(new_port)
        # session.commit()
        return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(debug=True)