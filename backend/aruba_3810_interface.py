from sqlalchemy import create_engine, text
from models import Session, PatchPort

engine = create_engine('sqlite:///patch_panel.db')
connection = engine.connect()

# Add the column if it doesn't exist
try:
    connection.execute(text("ALTER TABLE patch_ports ADD COLUMN aruba_3810_interface TEXT"))
    print("✅ Column 'aruba_3810_interface' added.")
except Exception as e:
    print("⚠️ Column might already exist:", e)

# Optionally add known mappings
session = Session()
updates = {
    "BB0202001": "1",
    "BB0202002": "2",
    "BB0202003": "3",
    "BB0202004": "4",
    "BB0202005": "5",
    "BB0202006": "6",
    "BB0202007": "7",
    "BB0202008": "8",
}

for name, port in updates.items():
    patch = session.query(PatchPort).filter_by(name=name).first()
    if patch:
        patch.aruba_3810_interface = port
        print(f"✅ Updated {name} → {port}")
    else:
        print(f"⚠️ PatchPort {name} not found.")

session.commit()
session.close()
connection.close()
