from netmiko import ConnectHandler
from netmiko import NetMikoTimeoutException, NetMikoAuthenticationException

def configure_aruba_switch(switch_ip, port, vlan, enabled=True, username='admin', password=None, switch_model='aruba_cx'):
    """
    Configure a switch port with the given VLAN and enabled/disabled status.
    Supports both Aruba AOS-CX and ProCurve switches.
    """
    if not password:
        return {
            "success": False,
            "message": "Switch password is required"
        }

    # Determine device type and commands based on switch model
    if '5412zl' in switch_model.lower() or 'procurve' in switch_model.lower():
        # ProCurve 5412zl configuration
        device_type = 'hp_procurve'
        commands = [
            f'vlan {vlan}',
            f'untagged {port}',
            'exit'
        ]
        save_command = 'write memory'
    else:
        # Default to Aruba AOS-CX
        device_type = 'hp_procurve'  # or 'aruba_os' if needed
        commands = [
            f'interface {port}',
            f'vlan access {vlan}',
            'no shutdown' if enabled else 'shutdown',
            'exit'
        ]
        save_command = 'write memory'

    device = {
        'device_type': device_type,
        'host': switch_ip,
        'username': username,
        'password': password,
        'timeout': 30,
        'global_delay_factor': 2,
    }

    try:
        print(f"Attempting to connect to switch {switch_ip}...")
        net_connect = ConnectHandler(**device)
        print(f"Connected to switch {switch_ip}")

        # Enter configuration mode
        print("Entering configuration mode...")
        net_connect.config_mode()

        print(f"Sending commands: {commands}")
        output = net_connect.send_config_set(commands)
        print(f"Command output: {output}")

        # Save the configuration
        print("Saving configuration...")
        save_output = net_connect.send_command_timing(save_command)
        print(f"Save output: {save_output}")

        # Close the connection
        net_connect.disconnect()
        print("Disconnected from switch")

        return {
            "success": True,
            "message": f"Successfully configured port {port} with VLAN {vlan}",
            "output": output
        }

    except NetMikoTimeoutException as e:
        error_msg = f"Connection to switch {switch_ip} timed out: {str(e)}"
        print(error_msg)
        return {
            "success": False,
            "message": error_msg
        }
    except NetMikoAuthenticationException as e:
        error_msg = f"Authentication failed for switch {switch_ip}: {str(e)}"
        print(error_msg)
        return {
            "success": False,
            "message": error_msg
        }
    except Exception as e:
        error_msg = f"Error configuring switch: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "message": error_msg
        }

def configure_switch_port(switch_ip, port, vlan, enabled=True, password=None, switch_model='aruba_cx'):
    """
    Main function to configure a switch port.
    This is the function called by the API endpoint.
    """
    try:
        print(f"Configuring switch {switch_ip} port {port} with VLAN {vlan}...")
        return configure_aruba_switch(
            switch_ip=switch_ip,
            port=port,
            vlan=vlan,
            enabled=enabled,
            password=password,
            switch_model=switch_model
        )
    except Exception as e:
        error_msg = f"Error in configure_switch_port: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "message": error_msg
        }

def configure_switch_port(switch_ip, port, vlan, enabled=True, password=None):
    """
    Main function to configure a switch port.
    This is the function called by the API endpoint.
    """
    # For now, we'll just use the Aruba implementation
    # You can add switch model detection here in the future if needed
    return configure_aruba_switch(
        switch_ip=switch_ip,
        port=port,
        vlan=vlan,
        enabled=enabled,
        password=password
    )