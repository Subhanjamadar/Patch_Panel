import os
import re
from netmiko import ConnectHandler
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Default switch configuration
DEFAULT_SWITCH_CONFIG = {
    "device_type": "aruba_aoscx",
    "username": os.getenv('SWITCH_USERNAME', 'admin'),
    "password": os.getenv('SWITCH_PASSWORD', ''),
    "timeout": 60,
}

# ============================
# FUNCTION: Get Line Modules + Interfaces
# ============================
def get_line_modules_and_interfaces(ip, username=None, password=None):
    """
    Get line modules and interfaces from an Aruba switch.
    
    Args:
        ip (str): IP address of the switch
        username (str, optional): Username for switch authentication
        password (str, optional): Password for switch authentication
        
    Returns:
        dict: Dictionary containing line modules and interfaces information
    """
    # Use provided credentials or fall back to environment variables
    switch_config = DEFAULT_SWITCH_CONFIG.copy()
    switch_config["ip"] = ip
    
    if username:
        switch_config["username"] = username
    if password:
        switch_config["password"] = password
    try:
        conn = ConnectHandler(**switch_config)

        # === GET MODULES (Line Modules only) ===
        module_output = conn.send_command(
            "show module",
            expect_string=r"#",
            read_timeout=60
        )

        section = re.search(
            r"Line Modules\s*=+\s*(.*?)\n\n",
            module_output,
            flags=re.DOTALL
        )

        line_modules = []
        if section:
            text = section.group(1)
            line_modules = re.findall(
                r"^\s*(\d+/\d+)\s",
                text,
                flags=re.MULTILINE
            )

        # === GET INTERFACES ===
        interface_output = conn.send_command(
            "show interface brief",
            expect_string=r"#",
            read_timeout=120
        )

        all_interfaces = re.findall(r"\b\d+/\d+/\d+\b", interface_output)

        # Filter: keep only interfaces from line modules
        filtered_interfaces = [
            iface for iface in all_interfaces
            if any(iface.startswith(f"{mod}/") for mod in line_modules)
        ]

        return {
            "status": "success",
            "ip": ip,
            "line_modules": line_modules,
            "total_line_modules": len(line_modules),
            "interfaces": filtered_interfaces,
            "total_interfaces": len(filtered_interfaces),
        }

    except Exception as e:
        return {
            "status": "error",
            "ip": ip,
            "message": str(e)
        }
    finally:
        if 'conn' in locals():
            conn.disconnect()

# ============================
# MAIN EXECUTION (for testing)
# ============================
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python interface.py <switch_ip> [username] [password]")
        sys.exit(1)

    ip = sys.argv[1]
    username = sys.argv[2] if len(sys.argv) > 2 else None
    password = sys.argv[3] if len(sys.argv) > 3 else None

    print(f"Connecting to switch at {ip}...")
    result = get_line_modules_and_interfaces(ip, username, password)
    
    if result["status"] == "success":
        print("\n=== Switch Interface Report ===")
        print(f"Switch IP: {result['ip']}")
        print(f"Line Modules: {result['line_modules']}")
        print(f"Total Line Modules: {result['total_line_modules']}")
        print(f"Total Interfaces: {result['total_interfaces']}")
        print("\nFirst 10 interfaces:")
        for iface in result['interfaces'][:10]:
            print(f"  - {iface}")
        if len(result['interfaces']) > 10:
            print(f"  ... and {len(result['interfaces']) - 10} more")
    else:
        print(f"\nError: {result.get('message', 'Unknown error')}")
