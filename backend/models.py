from sqlalchemy import create_engine, Column, String, Boolean, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Create SQLAlchemy engine and session
engine = create_engine('sqlite:///patch_panel.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()

class PatchPort(Base):
    __tablename__ = 'patch_ports'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    switch_port = Column(String, nullable=False)
    switch_ip = Column(String, nullable=True)
    vlan = Column(String)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    procurve_interface = Column(String)
    aruba_3810_interface = Column(String)
    comware_interface = Column(String)

# Create all tables
def init_db():
    Base.metadata.create_all(engine)
    print("Database tables created successfully!")

# Initialize the database when this module is imported
if __name__ == '__main__':
    init_db()