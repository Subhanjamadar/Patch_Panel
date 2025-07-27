from models import Session, PatchPort

session = Session()

# Example: Update BB0202001 to multiple interfaces
port = session.query(PatchPort).get("BB0202001")
if port:
    port.switch_port = "1/3/3"
    session.commit()
    print("Updated successfully")
else:
    print("Port not found")
