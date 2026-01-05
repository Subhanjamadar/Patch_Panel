# backend/switch_interfaces.py
from netmiko import ConnectHandler
import re

def get_switch_interfaces(ip, username, password):
    switch = {
        "device_type": "aruba_aoscx",
        "ip": ip,
        "username": username,
        "password": password,
        "timeout": 60,
    }
    
    try:
        conn = ConnectHandler(**switch)
        
        # Get modules
        module_output = conn.send_command("show module")
        line_module_section = re.search(
            r"Line Modules\s*=+\s*(.*?)\n\n",
            module_output,
            flags=re.DOTALL
        )

        line_modules = []
        if line_module_section:
            section_text = line_module_section.group(1)
            line_modules = re.findall(
                r"^\s*(\d+/\d+)\s",
                section_text,
                flags=re.MULTILINE
            )

        # Get interfaces
        interface_output = conn.send_command("show interface brief")
        all_interfaces = re.findall(r"\b\d+/\d+/\d+\b", interface_output)

        # Filter interfaces
        filtered_interfaces = []
        for mod in line_modules:
            prefix = mod + "/"
            filtered_interfaces.extend(
                iface for iface in all_interfaces 
                if iface.startswith(prefix)
            )

        return {
            "line_modules": line_modules,
            "total_line_modules": len(line_modules),
            "interfaces": filtered_interfaces,
            "total_interfaces": len(filtered_interfaces),
        }

    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals():
            conn.disconnect()