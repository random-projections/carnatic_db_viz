from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Create database engine
DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL)

# Create declarative base
Base = declarative_base()

class Song(Base):
    __tablename__ = "songs"
    
    song_id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    composer = Column(String(255), nullable=False)
    raaga = Column(String(100), nullable=False)
    taal = Column(String(100), nullable=False)
    lyrics = Column(Text, nullable=True)
    source = Column(String(50), nullable=False)
    date_added = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    recordings = relationship("Recording", back_populates="song")
    annotations = relationship("Annotation", back_populates="song")

class Recording(Base):
    __tablename__ = "recordings"
    
    recording_id = Column(Integer, primary_key=True)
    song_id = Column(Integer, ForeignKey('songs.song_id'), nullable=False)
    file_path = Column(Text, nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    analysis_data = Column(JSON, nullable=True)
    
    song = relationship("Song", back_populates="recordings")

class Annotation(Base):
    __tablename__ = "annotations"
    
    annotation_id = Column(Integer, primary_key=True)
    song_id = Column(Integer, ForeignKey('songs.song_id'), nullable=False)
    note_text = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    song = relationship("Song", back_populates="annotations")

# Create all tables
Base.metadata.create_all(engine)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 