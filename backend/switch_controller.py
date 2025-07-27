from netmiko import ConnectHandler

def set_switch_port_state(interface_name, enable, vlan=None, ip=None, password=None):
    device = {
        "device_type": "aruba_aoscx",  # Correct for Aruba OS-CX switches
        "ip": ip,              # Replace with your actual switch IP
        "username": "admin",
        "password": password,
    }

    commands = []

    if enable:
        if vlan:
            # Optional: ensure VLAN exists
            commands.append(f"vlan {vlan}")

        commands.append(f"interface {interface_name}")
        commands.append("no shutdown")

        if vlan:
            commands.append(f"vlan access {vlan}")
    else:
        commands.append(f"interface {interface_name}")
        commands.append("shutdown")

    try:
        conn = ConnectHandler(**device)
        output = conn.send_config_set(commands)
        print(output)
        conn.disconnect()
    except Exception as e:
        print(f"Error: {e}")
