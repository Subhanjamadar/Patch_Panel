from sqlalchemy import create_engine, text
from models import Session, PatchPort

# Connect to the same SQLite database
engine = create_engine('sqlite:///patch_panel.db')
connection = engine.connect()

# 1. Add the new column if it doesn't exist
try:
    connection.execute(text("ALTER TABLE patch_ports ADD COLUMN procurve_interface TEXT"))
    print("✅ Column 'procurve_interface' added.")
except Exception as e:
    print("⚠️ Column might already exist:", e)

# 2. Populate some known mappings (add more if needed)
session = Session()
updates = {
    "BB0202001": "A1",
    "BB0202002": "A2",
    "BB0202003": "A3",
    "BB0202004": "A4",
    "BB0202005": "A5",
    "BB0202006": "A6",
    "BB0202007": "A7",
    "BB0202008": "A8",

}

for name, procurve_port in updates.items():
    port = session.query(PatchPort).filter_by(name=name).first()
    if port:
        port.procurve_interface = procurve_port
        print(f"✅ Updated {name} → {procurve_port}")
    else:
        print(f"⚠️ Port {name} not found in DB")

session.commit()
session.close()
connection.close()
