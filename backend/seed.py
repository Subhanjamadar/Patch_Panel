from models import Session, PatchPort

session = Session()

# Clear existing ports (optional)
session.query(PatchPort).delete()

# Add 8 ports
for i in range(8):
    port = PatchPort(
        name=f"BB020200{i+1}",
        switch_port=f"1/3/{i+1}",
        enabled=False
    )
    session.add(port)

session.commit()
print("✅ Database seeded with 8 patch panel ports.")
