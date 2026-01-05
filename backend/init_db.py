from models import Base, engine, Session
from sqlalchemy.exc import OperationalError

def init_db():
    try:
        # Create all tables
        Base.metadata.create_all(engine)
        print("Database tables created successfully.")
        
        # Add some sample data
        session = Session()
        
        # Check if we already have data
        from models import PatchPort
        if not session.query(PatchPort).first():
            print("Adding sample data...")
            # Add some sample ports
            for i in range(1, 49):
                port = PatchPort(
                    name=f"Port {i}",
                    switch_port=f"1/3/{i}",
                    vlan="1",
                    enabled=True,
                    aruba_3810_interface=f"1/3/{i}"
                )
                session.add(port)
            
            session.commit()
            print(f"Added {session.query(PatchPort).count()} sample ports.")
        else:
            print("Database already contains data. No sample data added.")
            
        session.close()
        return True
        
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        return False

if __name__ == "__main__":
    if init_db():
        print("Database initialization completed successfully.")
    else:
        print("Database initialization failed.")
