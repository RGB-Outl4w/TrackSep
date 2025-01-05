import os
import logging
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QIcon, QPalette
from PyQt5.QtWidgets import QApplication, QFileDialog, QFormLayout, QGroupBox, QHBoxLayout, QMainWindow, QMessageBox, QProgressBar, QVBoxLayout, QWidget, QPushButton, QLabel
from backend.settings import Settings
from backend.log_handler import LogHandler
from ui.settings_dialog import QComboBox, QDialog, QLineEdit, SettingsDialog
from backend.stream_info import StreamInfo
from ui.log_widget import LogWidget
from backend.worker_thread import WorkerThread

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.setWindowTitle("Track Separator")
        self.setGeometry(100, 100, 800, 600)
        
        # Apply theme
        self.apply_theme()
        
        self.input_file = None
        self.stream_info = None
        
        # Initialize logging widget
        self.log_widget = LogWidget()
        self.logger = logging.getLogger(__name__)
        log_handler = LogHandler(self.log_widget)
        self.logger.addHandler(log_handler)
        self.init_ui()

    def apply_theme(self):
        app = QApplication.instance()
        theme = self.settings.get('theme')
        app.setStyle(theme)

        unsupported_themes = ['windowsvista', 'Macintosh']
        if theme in unsupported_themes:
            self.settings.set('dark_mode', 'false')
            app.setPalette(app.style().standardPalette())
            app.setStyleSheet("")
        elif self.settings.get('dark_mode') == 'true':
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            app.setPalette(palette)

            # Fix tooltip style in dark mode for all themes
            app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
        else:  # If not dark mode, reset to default palette
            app.setPalette(app.style().standardPalette())

    def init_ui(self):
        main_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Title
        title_label = QLabel("Track Separator")
        title_label.setFont(QFont('Arial', 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Input File Section
        input_group = QGroupBox("Input File")
        input_layout = QVBoxLayout()
        
        file_select_layout = QHBoxLayout()
        self.file_path_field = QLineEdit()
        self.file_path_field.setPlaceholderText("No file selected")
        self.file_path_field.setReadOnly(True)
        
        self.file_button = QPushButton("Browse")
        self.file_button.setMinimumWidth(100)
        self.clear_button = QPushButton("Clear")
        self.clear_button.setMinimumWidth(100)
        file_select_layout.addWidget(self.file_path_field)
        file_select_layout.addWidget(self.file_button)
        file_select_layout.addWidget(self.clear_button)
        
        input_layout.addLayout(file_select_layout)

        # Stream Selection
        streams_layout = QHBoxLayout()
        
        self.video_stream_combo = QComboBox()
        self.video_stream_combo.setEnabled(False)
        self.audio_stream_combo = QComboBox()
        self.audio_stream_combo.setEnabled(False)
        
        video_stream_layout = QVBoxLayout()
        video_stream_layout.addWidget(QLabel("Video Stream:"))
        video_stream_layout.addWidget(self.video_stream_combo)
        
        audio_stream_layout = QVBoxLayout()
        audio_stream_layout.addWidget(QLabel("Audio Stream:"))
        audio_stream_layout.addWidget(self.audio_stream_combo)
        
        streams_layout.addLayout(video_stream_layout)
        streams_layout.addLayout(audio_stream_layout)
        input_layout.addLayout(streams_layout)
        
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # Output Settings Section
        output_group = QGroupBox("Output Settings")
        output_layout = QVBoxLayout()

        # Output folder selection
        folder_layout = QHBoxLayout()
        self.output_folder_field = QLineEdit()
        self.output_folder_field.setPlaceholderText("Select output folder or use same as input")
        self.output_folder_field.setText(self.settings.get('default_output_folder'))
        
        self.output_button = QPushButton("Browse")
        self.same_as_input = QPushButton("Same as Input")
        
        folder_layout.addWidget(self.output_folder_field)
        folder_layout.addWidget(self.output_button)
        folder_layout.addWidget(self.same_as_input)
        output_layout.addLayout(folder_layout)

        # Custom filename templates
        filename_group = QGroupBox("Output Filenames")
        filename_layout = QFormLayout()
        
        self.video_filename = QLineEdit()
        self.video_filename.setText(self.settings.get('video_template'))
        self.audio_filename = QLineEdit()
        self.audio_filename.setText(self.settings.get('audio_template'))
        
        filename_layout.addRow("Video:", self.video_filename)
        filename_layout.addRow("Audio:", self.audio_filename)
        
        filename_group.setLayout(filename_layout)
        output_layout.addWidget(filename_group)
        
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        # Progress Section
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        progress_layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Status: Ready")
        progress_layout.addWidget(self.status_label)
        
        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)

        # Buttons
        button_layout = QHBoxLayout()
        
        self.settings_button = QPushButton("Settings")
        self.settings_button.setIcon(QIcon.fromTheme("preferences-system"))
        
        self.extract_button = QPushButton("Extract")
        self.extract_button.setIcon(QIcon.fromTheme("media-playback-start"))
        self.extract_button.setEnabled(False)
        
        button_layout.addWidget(self.settings_button)
        button_layout.addStretch()
        button_layout.addWidget(self.extract_button)
        
        layout.addLayout(button_layout)
        
        # Add log widget
        layout.addWidget(self.log_widget)

        # Set up the main widget
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        # Connect signals
        self.file_button.clicked.connect(self.browse_file)
        self.clear_button.clicked.connect(self.clear_fields)
        self.output_button.clicked.connect(self.browse_output_folder)
        self.same_as_input.clicked.connect(self.use_input_folder)
        self.settings_button.clicked.connect(self.show_settings)
        self.extract_button.clicked.connect(self.extract)

    def clear_fields(self):
        self.file_path_field.clear()
        self.video_stream_combo.clear()
        self.audio_stream_combo.clear()
        self.progress_bar.setValue(0)
        self.status_label.setText("Status: Ready")
        self.log_widget.log_text.clear()
        self.extract_button.setEnabled(False)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Video File", "",
            "Video Files (*.mp4 *.mkv *.avi *.mov);;All Files (*.*)"
        )
        if file_path:
            self.input_file = file_path
            self.file_path_field.setText(file_path)
            self.extract_button.setEnabled(True)
            
            # Probe for streams
            self.stream_info = StreamInfo(file_path, self.settings.get('ffmpeg_path'))
            
            # Update stream selection combos
            self.video_stream_combo.clear()
            self.audio_stream_combo.clear()
            
            for stream in self.stream_info.video_streams:
                self.video_stream_combo.addItem(
                    f"Stream {stream['index']}: {stream['codec']} ({stream['resolution']})",
                    stream['index']
                )
            
            for stream in self.stream_info.audio_streams:
                self.audio_stream_combo.addItem(
                    f"Stream {stream['index']}: {stream['codec']} ({stream['channels']} ch, {stream['sample_rate']} Hz)",
                    stream['index']
                )
            
            self.video_stream_combo.setEnabled(True)
            self.audio_stream_combo.setEnabled(True)

            if not self.output_folder_field.text():
                self.use_input_folder()

    def browse_output_folder(self):
        folder_path = QFileDialog.getExistingDirectory(
            self, "Select Output Folder",
            self.output_folder_field.text()
        )
        if folder_path:
            self.output_folder_field.setText(folder_path)

    def use_input_folder(self):
        if self.input_file:
            self.output_folder_field.setText(os.path.dirname(self.input_file))

    def show_settings(self):
        dialog = SettingsDialog(self.settings, self)
        if dialog.exec_() == QDialog.Accepted:
            # Re-read settings in case they were changed
            self.settings = Settings()
            self.apply_theme()

    def extract(self):
        if not self.input_file:
            self.status_label.setText("Error: No input file selected.")
            return
            
        if not self.output_folder_field.text():
            self.status_label.setText("Error: No output folder selected.")
            return

        # Get selected streams
        video_stream = None
        audio_stream = None
        
        if self.video_stream_combo.currentData() is not None:
            video_stream = self.video_stream_combo.currentData()
            
        if self.audio_stream_combo.currentData() is not None:
            audio_stream = self.audio_stream_combo.currentData()

        # Prepare output filenames
        input_filename = os.path.splitext(os.path.basename(self.input_file))[0]
        video_template = self.video_filename.text() or self.settings.get('video_template')
        audio_template = self.audio_filename.text() or self.settings.get('audio_template')

        # Determine the correct file extension for the audio output
        audio_extension = {
            'aac': 'm4a',
            'mp3': 'mp3',
            'flac': 'flac'
        }.get(self.settings.get('audio_codec'), 'm4a')
        
        output_video = os.path.join(
            self.output_folder_field.text(),
            f"{video_template.format(filename=input_filename)}.mp4"
        )
        output_audio = os.path.join(
            self.output_folder_field.text(),
            f"{audio_template.format(filename=input_filename)}.{audio_extension}"
        )

        # Disable buttons during extraction
        self.file_button.setEnabled(False)
        self.clear_button.setEnabled(False)
        self.output_button.setEnabled(False)
        self.same_as_input.setEnabled(False)
        self.settings_button.setEnabled(False)
        self.extract_button.setEnabled(False)

        # Start extraction
        self.worker = WorkerThread(
            self.input_file, output_video, output_audio,
            self.settings, video_stream, audio_stream
        )
        self.worker.progress.connect(self.update_progress)
        self.worker.error.connect(self.display_error)
        self.worker.finished.connect(self.enable_buttons)
        self.worker.start()

        self.status_label.setText("Processing...")

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        if value == 100:
            self.status_label.setText("Extraction Complete!")

    def display_error(self, message):
        self.status_label.setText(f"Error: {message}")
        QMessageBox.critical(self, "Error", message)
        self.enable_buttons()

    def enable_buttons(self):
        self.file_button.setEnabled(True)
        self.clear_button.setEnabled(True)
        self.output_button.setEnabled(True)
        self.same_as_input.setEnabled(True)
        self.settings_button.setEnabled(True)
        self.extract_button.setEnabled(True)
