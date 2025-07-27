import smtplib
from email.mime.text import MIMEText

def notify_daniel(request_data):
    body = f"""Hi Daniel,

A new port enablement request was received from TechDirect:

- Rack Location(s): {request_data['rack_location']}
- IP(s): {request_data['ip_addresses']}
- VLAN: {request_data['vlan'] or 'N/A'}

Please provide:
- Patch Panel Serial Number
- Switch Port Interface
- Switch IP

Regards,
Patch Panel Automation
"""

    msg = MIMEText(body)
    msg["Subject"] = "Patch Panel Info Required - TechDirect Request"
    msg["From"] = "patchpanel-automation@hpe.com"
    msg["To"] = "daniel@hpe.com"

    with smtplib.SMTP("16.230.255.157", 25) as server:
        server.sendmail(msg["From"], [msg["To"]], msg.as_string())
