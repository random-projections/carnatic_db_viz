from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import json

# Create database engine
DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL)

# Create declarative base
Base = declarative_base()


# Define the Songs model
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
    
    # Add relationship to recordings
    recordings = relationship("Recording", back_populates="song")
    annotations = relationship("Annotation", back_populates="song")


class Recording(Base):
    __tablename__ = "recordings"
    
    recording_id = Column(Integer, primary_key=True)
    song_id = Column(Integer, ForeignKey('songs.song_id'), nullable=False)
    file_path = Column(Text, nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    analysis_data = Column(JSON, nullable=True)
    
    # Add relationship to song
    song = relationship("Song", back_populates="recordings")


class Annotation(Base):
    __tablename__ = "annotations"
    
    annotation_id = Column(Integer, primary_key=True)
    song_id = Column(Integer, ForeignKey('songs.song_id'), nullable=False)
    note_text = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship to song
    song = relationship("Song", back_populates="annotations")


# Create all tables
Base.metadata.create_all(engine)


# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Function to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def print_help():
    print("\nAvailable commands:")
    print("1. add_song - Add a new song")
    print("2. add_recording - Add a recording to a song")
    print("3. add_annotation - Add an annotation to a song")
    print("4. list_songs - List all songs")
    print("5. list_recordings - List recordings for a song")
    print("6. list_annotations - List annotations for a song")
    print("7. help - Show this help message")
    print("8. exit - Exit the program")


def add_song(db):
    print("\nAdding a new song:")
    title = input("Title: ")
    composer = input("Composer: ")
    raaga = input("Raaga: ")
    taal = input("Taal: ")
    lyrics = input("Lyrics (optional, press enter to skip): ")
    source = input("Source: ")
    
    song = Song(
        title=title,
        composer=composer,
        raaga=raaga,
        taal=taal,
        lyrics=lyrics if lyrics else None,
        source=source
    )
    db.add(song)
    db.commit()
    print(f"Song '{title}' added successfully with ID: {song.song_id}")


def add_recording(db):
    print("\nAdding a new recording:")
    song_id = int(input("Song ID: "))
    file_path = input("File path: ")
    analysis_data_str = input("Analysis data (JSON format, press enter to skip): ")
    
    analysis_data = None
    if analysis_data_str:
        try:
            analysis_data = json.loads(analysis_data_str)
        except json.JSONDecodeError:
            print("Invalid JSON format. Skipping analysis data.")
    
    recording = Recording(
        song_id=song_id,
        file_path=file_path,
        analysis_data=analysis_data
    )
    db.add(recording)
    db.commit()
    print(f"Recording added successfully with ID: {recording.recording_id}")


def add_annotation(db):
    print("\nAdding a new annotation:")
    song_id = int(input("Song ID: "))
    note_text = input("Note text: ")
    
    annotation = Annotation(
        song_id=song_id,
        note_text=note_text
    )
    db.add(annotation)
    db.commit()
    print(f"Annotation added successfully with ID: {annotation.annotation_id}")


def list_songs(db):
    songs = db.query(Song).all()
    print("\nAll Songs:")
    for song in songs:
        print(f"ID: {song.song_id}, Title: {song.title}, Composer: {song.composer}, "
              f"Raaga: {song.raaga}, Taal: {song.taal}")


def list_recordings(db):
    song_id = int(input("Enter song ID: "))
    recordings = db.query(Recording).filter(Recording.song_id == song_id).all()
    print(f"\nRecordings for song ID {song_id}:")
    for rec in recordings:
        print(f"ID: {rec.recording_id}, File: {rec.file_path}, "
              f"Recorded at: {rec.recorded_at}")


def list_annotations(db):
    song_id = int(input("Enter song ID: "))
    annotations = db.query(Annotation).filter(Annotation.song_id == song_id).all()
    print(f"\nAnnotations for song ID {song_id}:")
    for ann in annotations:
        print(f"ID: {ann.annotation_id}, Note: {ann.note_text}, "
              f"Timestamp: {ann.timestamp}")


def main():
    print("Welcome to the Music Database Manager")
    print_help()
    
    db = SessionLocal()
    try:
        while True:
            command = input("\nEnter command (type 'help' for commands): ").lower()
            
            try:
                if command == 'exit':
                    break
                elif command == 'help':
                    print_help()
                elif command == 'add_song':
                    add_song(db)
                elif command == 'add_recording':
                    add_recording(db)
                elif command == 'add_annotation':
                    add_annotation(db)
                elif command == 'list_songs':
                    list_songs(db)
                elif command == 'list_recordings':
                    list_recordings(db)
                elif command == 'list_annotations':
                    list_annotations(db)
                else:
                    print("Unknown command. Type 'help' for available commands.")
            
            except Exception as e:
                print(f"Error: {str(e)}")
                db.rollback()
    
    finally:
        db.close()


if __name__ == "__main__":
    main()
