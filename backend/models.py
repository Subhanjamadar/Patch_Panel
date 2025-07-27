# backend/models.py

from sqlalchemy import create_engine, Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///patch_panel.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()

class PatchPort(Base):
    __tablename__ = 'patch_ports'

    name = Column(String, primary_key=True)
    switch_port = Column(String)
    vlan = Column(String)
    enabled = Column(Boolean)

Base.metadata.create_all(engine)
