from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLineEdit, QTableWidget, QTableWidgetItem, QCompleter)
from PyQt6.QtCore import Qt, QSortFilterProxyModel
from db import SessionLocal, Song, Recording

class SortableTableWidget(QTableWidget):
    """Custom TableWidget that supports sorting"""
    def __init__(self):
        super().__init__()
        self.setSortingEnabled(True)  # Enable sorting
        
    def setup_sorting(self):
        """Configure how different columns should be sorted"""
        self.horizontalHeader().setSectionsClickable(True)
        # Sort IDs as numbers instead of strings
        self.id_column = 0  # Assuming ID is always first column
        self.horizontalHeader().sectionClicked.connect(self.handle_sort)
    
    def handle_sort(self, column):
        """Custom sort handler for specific columns"""
        if column == self.id_column:
            # Sort IDs numerically
            self.sortItems(column, Qt.SortOrder.AscendingOrder if 
                          self.horizontalHeader().sortIndicatorOrder() == Qt.SortOrder.DescendingOrder 
                          else Qt.SortOrder.DescendingOrder)

class CarnaticMusicBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self.db = SessionLocal()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('Carnatic Music Browser')
        self.setGeometry(100, 100, 1200, 600)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Create search bar with autocomplete
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText('Search by Raaga...')
        self.setup_autocomplete()
        self.search_bar.textChanged.connect(self.on_search)
        layout.addWidget(self.search_bar)
        
        # Create tables layout
        tables_layout = QHBoxLayout()
        
        # Songs table
        self.songs_table = SortableTableWidget()
        self.songs_table.setColumnCount(7)
        self.songs_table.setHorizontalHeaderLabels([
            'ID', 'Title', 'Composer', 'Raaga', 'Taal', 'Type', 'Source'
        ])
        self.songs_table.setup_sorting()
        self.songs_table.itemSelectionChanged.connect(self.on_song_selected)
        tables_layout.addWidget(self.songs_table)
        
        # Recordings table
        self.recordings_table = SortableTableWidget()
        self.recordings_table.setColumnCount(5)
        self.recordings_table.setHorizontalHeaderLabels([
            'ID', 'File Path', 'Artist', 'Teacher', 'Recorded At'
        ])
        self.recordings_table.setup_sorting()
        tables_layout.addWidget(self.recordings_table)
        
        layout.addLayout(tables_layout)
        self.setLayout(layout)
        
        # Set table column widths
        self.resize_tables()
    
    def setup_autocomplete(self):
        # Get unique raagas from database
        raagas = [r[0] for r in self.db.query(Song.raaga).distinct().all()]
        completer = QCompleter(raagas)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.search_bar.setCompleter(completer)
    
    def resize_tables(self):
        # Resize songs table columns
        total_width = self.songs_table.width()
        self.songs_table.setColumnWidth(0, int(total_width * 0.08))  # ID
        self.songs_table.setColumnWidth(1, int(total_width * 0.25))  # Title
        self.songs_table.setColumnWidth(2, int(total_width * 0.17))  # Composer
        self.songs_table.setColumnWidth(3, int(total_width * 0.15))  # Raaga
        self.songs_table.setColumnWidth(4, int(total_width * 0.12))  # Taal
        self.songs_table.setColumnWidth(5, int(total_width * 0.15))  # Type
        self.songs_table.setColumnWidth(6, int(total_width * 0.08))  # Source
        
        # Resize recordings table columns
        total_width = self.recordings_table.width()
        self.recordings_table.setColumnWidth(0, int(total_width * 0.1))   # ID
        self.recordings_table.setColumnWidth(1, int(total_width * 0.3))   # File Path
        self.recordings_table.setColumnWidth(2, int(total_width * 0.2))   # Artist
        self.recordings_table.setColumnWidth(3, int(total_width * 0.2))   # Teacher
        self.recordings_table.setColumnWidth(4, int(total_width * 0.2))   # Recorded At
    
    def on_search(self, text):
        # Clear tables
        self.songs_table.setRowCount(0)
        self.recordings_table.setRowCount(0)
        
        if not text:
            return
            
        # Query songs by raaga
        songs = self.db.query(Song).filter(
            Song.raaga.ilike(f'%{text}%')
        ).all()
        
        # Populate songs table
        self.songs_table.setRowCount(len(songs))
        for row, song in enumerate(songs):
            # Create items that can be sorted properly
            id_item = QTableWidgetItem()
            id_item.setData(Qt.ItemDataRole.DisplayRole, song.song_id)
            
            self.songs_table.setItem(row, 0, id_item)
            self.songs_table.setItem(row, 1, QTableWidgetItem(song.title))
            self.songs_table.setItem(row, 2, QTableWidgetItem(song.composer))
            self.songs_table.setItem(row, 3, QTableWidgetItem(song.raaga))
            self.songs_table.setItem(row, 4, QTableWidgetItem(song.taal))
            self.songs_table.setItem(row, 5, QTableWidgetItem(song.type_of_song or ''))
            self.songs_table.setItem(row, 6, QTableWidgetItem(song.source))
    
    def on_song_selected(self):
        self.recordings_table.setRowCount(0)
        selected_items = self.songs_table.selectedItems()
        if not selected_items:
            return
            
        # Get song_id from the first column of selected row
        song_id = int(self.songs_table.item(selected_items[0].row(), 0).text())
        
        # Query recordings for selected song
        recordings = self.db.query(Recording).filter(
            Recording.song_id == song_id
        ).all()
        
        # Populate recordings table
        self.recordings_table.setRowCount(len(recordings))
        for row, recording in enumerate(recordings):
            # Create items that can be sorted properly
            id_item = QTableWidgetItem()
            id_item.setData(Qt.ItemDataRole.DisplayRole, recording.recording_id)
            
            date_item = QTableWidgetItem()
            date_item.setData(Qt.ItemDataRole.DisplayRole, recording.recorded_at)
            
            self.recordings_table.setItem(row, 0, id_item)
            self.recordings_table.setItem(row, 1, QTableWidgetItem(recording.file_path))
            self.recordings_table.setItem(row, 2, QTableWidgetItem(recording.artist or ''))
            self.recordings_table.setItem(row, 3, QTableWidgetItem(recording.teacher or ''))
            self.recordings_table.setItem(row, 4, date_item)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resize_tables()
    
    def closeEvent(self, event):
        self.db.close()
        super().closeEvent(event)

def main():
    import sys
    app = QApplication(sys.argv)
    browser = CarnaticMusicBrowser()
    browser.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 