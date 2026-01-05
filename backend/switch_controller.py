from models import Session, PatchPort
from model_cache import ip_model_map
from netmiko_commands import configure_aruba_legacy

def set_switch_port_state(port_name, enabled, vlan, ip, password):
    session = Session()
    patch_port = session.query(PatchPort).filter_by(name=port_name).first()
    session.close()

    model = ip_model_map.get(ip)
    if not model:
        raise Exception(f"Switch model for IP {ip} not found.")

    # --- Case 1: Port comes from DB mapping ---
    if patch_port:
        if model == "ProCurve 5412zl":
            interface = patch_port.procurve_interface or patch_port.switch_port
        elif model == "Aruba 3810M 48G":
            interface = patch_port.aruba_3810_interface or patch_port.switch_port
        elif model.startswith("H3C") or model == "HPE 5900AF-48G":
            interface = patch_port.comware_interface or patch_port.switch_port
        elif model == "Aruba 6410":
            interface = patch_port.switch_port.name   # usually stored as "1/3/1"
        else:
            interface = patch_port.switch_port
    else:
        # --- Case 2: Direct switch interface ---
        interface = port_name

    if not isinstance(interface, str):
        raise Exception(f"Interface resolved to non-string: {interface}")

    print(f"Switch IP: {ip}, Model: {model}, Interface: {interface}, VLAN: {vlan}, Enabled: {enabled}")
    configure_aruba_legacy(interface, enabled, vlan, ip, password)