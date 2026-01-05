from netmiko import ConnectHandler
from model_cache import ip_model_map

def flatten_interface(interface):
    return interface.split("/")[-1] if "/" in interface else interface

def configure_aruba_legacy(interface, enabled, vlan, ip, password):
    """
    interface: string (e.g. '1/3/1' or 'GigabitEthernet1/0/12')
    """
    model = ip_model_map.get(ip)
    device_type = "hp_procurve"
    commands = []

    if model in ["ProCurve 5412zl", "Aruba 5400R zl2"]:
        commands = [
            f"vlan {vlan}",
            f"name 1{vlan}",
            f"{'untagged' if enabled else 'no untagged'} {interface}",
            "exit",
            "write memory"
        ]

    elif model == "Aruba 3810M 48G":
        interface = flatten_interface(interface)
        commands = [
            f"vlan {vlan}",
            f"{'untagged' if enabled else 'no untagged'} {interface}",
            "exit",
            "write memory"
        ]

    elif model.startswith("H3C") or model == "HPE 5900AF-48G":
        device_type = "hp_comware"
        port_number = interface.split("/")[-1]
        if model.startswith("H3C"):
            interface = f"GigabitEthernet0/0/{port_number}"
        else:
            interface = f"GigabitEthernet1/0/{port_number}"
        commands = [
            "system-view",
            f"interface {interface}",
            "port link-type access",
            f"port access vlan {vlan}",
            "return",
            "save force"
        ]

    elif model == "Aruba 6410":
        device_type = "aruba_aoscx"
        commands = [
            f"interface {interface}",
            "no vlan access",
            f"vlan access {vlan}",
            "no shutdown" if enabled else "shutdown",
            "exit",
            "write memory"
        ]

    else:
        commands = [
            f"vlan {vlan}",
            f"{'untagged' if enabled else 'no untagged'} {interface}",
            "exit",
            "write memory"
        ]

    device = {
        "device_type": device_type,
        "host": ip,
        "username": "admin",
        "password": password,
        "secret": password
    }

    if device_type == "hp_comware":
        device["banner_timeout"] = 30

    print(f"[Executing on {ip} ({model})] Commands: {commands}")
    connection = ConnectHandler(**device)

    if device_type == "hp_comware":
        output = ""
        for cmd in commands[:-1]:
            cmd_output = connection.send_command(
                cmd,
                expect_string=r"[<\[].*[>#\]]",
                strip_prompt=False,
                strip_command=False,
                delay_factor=2,
            )
            output += f"\n[DEBUG] {cmd} ->\n{cmd_output}"

        save_output = connection.send_command("save", expect_string=r"\[Y/N\]", delay_factor=2, read_timeout=30)
        save_output += connection.send_command("Y", expect_string=r"[<\[].*[>#\]]", read_timeout=30)
        output += "\n[DEBUG] save ->\n" + save_output

    else:
        output = connection.send_config_set(commands)

    connection.disconnect()
    return output
