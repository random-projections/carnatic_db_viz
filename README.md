# Carnatic Music Database Manager

A lightweight database management system designed specifically for organizing and tracking Carnatic music compositions, recordings, and annotations.

## Features

### Database Structure

The system manages three main entities:

1. **Songs**
   - Stores basic information about Carnatic compositions
   - Tracks title, composer, raaga, taal, and lyrics
   - Records source and date of entry

2. **Recordings**
   - Links audio recordings to specific songs
   - Stores file paths to audio files
   - Can include analysis data (e.g., pitch patterns, rhythm analysis)
   - Timestamps when recordings were added

3. **Annotations**
   - Allows adding notes and comments to songs
   - Useful for marking important aspects of compositions
   - Timestamps all annotations

### Interactive Interface

The system provides a simple command-line interface with the following capabilities:

- `add_song`: Add new Carnatic compositions
- `add_recording`: Link recordings to existing songs
- `add_annotation`: Add notes or comments to songs
- `list_songs`: View all stored compositions
- `list_recordings`: View recordings for a specific song
- `list_annotations`: View annotations for a specific song

## Technical Details

- Built with SQLAlchemy ORM
- Uses SQLite database for simple deployment
- Written in Python
- Stores data locally in `database.db`

## Usage

1. Install requirements:
```bash
pip install -r requirements.txt
```

2. Run the program:
```bash
python main.py
```

3. Use the interactive prompt to manage your Carnatic music collection:
```
Welcome to the Music Database Manager
Available commands:
1. add_song - Add a new song
2. add_recording - Add a recording to a song
...
```

## Use Cases

- Maintain a personal collection of Carnatic compositions
- Track multiple recordings of the same composition
- Add notes about specific aspects of compositions
- Keep track of raaga and taal information
- Document sources of compositions

## Data Storage

All data is stored locally in a SQLite database file (`database.db`). This makes it easy to backup and transfer your music database.
