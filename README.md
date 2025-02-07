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

### Interactive Interfaces

The system provides two ways to interact with the database:

#### 1. Command Line Interface
Access the database through a text-based interface with commands:
- `add_song`: Add new Carnatic compositions
- `add_recording`: Link recordings to existing songs
- `add_annotation`: Add notes or comments to songs
- `list_songs`: View all stored compositions
- `list_recordings`: View recordings for a specific song
- `list_annotations`: View annotations for a specific song

#### 2. Graphical Interface
A modern GUI browser that provides:
- Search bar with raaga autocomplete
- Two-panel view:
  - Left panel: Songs table with details (title, composer, raaga, taal)
  - Right panel: Associated recordings for selected song
- Real-time filtering as you type
- Responsive layout that adjusts to window size

## Installation

1. Create a Python environment (recommended Python 3.11):
```bash
conda create -n carnatic_music python=3.11
conda activate carnatic_music
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface
Run the REPL interface:
```bash
python repl.py
```

### Graphical Interface
Launch the GUI browser:
```bash
python gui.py
```

The GUI provides an intuitive way to:
- Browse songs by raaga using the search bar
- View all song details in a tabular format
- See recordings associated with each song
- Filter results in real-time as you type

## Technical Details

- Built with SQLAlchemy ORM
- Uses SQLite database for simple deployment
- GUI built with PyQt6
- Stores data locally in `database.db`

## Use Cases

- Maintain a personal collection of Carnatic compositions
- Track multiple recordings of the same composition
- Add notes about specific aspects of compositions
- Keep track of raaga and taal information
- Document sources of compositions
- Quickly find songs by raaga using the GUI browser

## Data Storage

All data is stored locally in a SQLite database file (`database.db`). This makes it easy to backup and transfer your music database.
