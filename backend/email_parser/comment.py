import win32com.client
import re

def extract_patch_panel_details(body):
    match = re.search(r"End User Comments:(.*?)(?:\n\s*\n|\Z)", body, re.DOTALL | re.IGNORECASE)
    if not match:
        return None

    comments = match.group(1)

    num_ports_match = re.search(r"Number of ports[:\-]?\s*(\d+)", comments)
    num_ports = int(num_ports_match.group(1)) if num_ports_match else None

    ports = re.findall(r"\b([A-Z]{2}\d{7})\b", comments)

    vlan_match = re.search(r"VLAN\s*[:\-]?\s*(\d+)", comments)
    vlan = int(vlan_match.group(1)) if vlan_match else None

    return {
        "number_of_ports": num_ports,
        "ports": ports,
        "vlan": vlan
    }

# Connect to Outlook
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.Folders("mehaboobsubhani.jamadar-ext@hpe.com").Folders("Inbox").Folders("BIZIT-NW")  # your main mailbox
messages = inbox.Items
messages.Sort("[ReceivedTime]", True)

print("📥 TechDirect Requests Sent to BIZIT-NW:")
print("=" * 60)

for message in messages:
    if message.Class != 43:
        continue

    sender = message.SenderEmailAddress.lower()
    subject = message.Subject or ""
    body = message.Body or ""

    # Filter: must be from TechDirect and contain End User Comments
    if "techdirect@hpe.com" in sender and "End User Comments" in body:
        extracted = extract_patch_panel_details(body)
        if extracted:
            print(f"Subject: {subject}")
            print(f"Received: {message.ReceivedTime}")
            print(f"Parsed Data: {extracted}")
            print("-" * 50)
