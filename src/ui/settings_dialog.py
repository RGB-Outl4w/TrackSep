import sys
from PyQt5.QtWidgets import QDialog, QFileDialog, QFormLayout, QHBoxLayout, QStyleFactory, QVBoxLayout, QTabWidget, QLineEdit, QComboBox, QCheckBox, QPushButton, QWidget

class SettingsDialog(QDialog):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.setWindowTitle("Preferences")
        self.setMinimumWidth(500)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        tabs = QTabWidget()

        # General Settings Tab
        general_tab = QWidget()
        general_layout = QFormLayout()

        self.output_folder = QLineEdit(self.settings.get('default_output_folder'))
        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self.browse_output_folder)
        output_layout = QHBoxLayout()
        output_layout.addWidget(self.output_folder)
        output_layout.addWidget(browse_button)

        self.ffmpeg_path = QLineEdit(self.settings.get('ffmpeg_path'))
        ffmpeg_browse = QPushButton("Browse...")
        ffmpeg_browse.clicked.connect(self.browse_ffmpeg)
        ffmpeg_layout = QHBoxLayout()
        ffmpeg_layout.addWidget(self.ffmpeg_path)
        ffmpeg_layout.addWidget(ffmpeg_browse)

        self.video_template = QLineEdit(self.settings.get('video_template'))
        self.audio_template = QLineEdit(self.settings.get('audio_template'))
        
        general_layout.addRow("Default Output Folder:", output_layout)
        general_layout.addRow("FFmpeg Path:", ffmpeg_layout)
        general_layout.addRow("Video Filename Template:", self.video_template)
        general_layout.addRow("Audio Filename Template:", self.audio_template)
        
        general_tab.setLayout(general_layout)

        # Advanced Settings Tab
        advanced_tab = QWidget()
        advanced_layout = QFormLayout()

        self.video_codec = QComboBox()
        self.video_codec.addItems(['copy', 'h264', 'h265', 'vp9'])
        self.video_codec.setCurrentText(self.settings.get('video_codec'))

        self.audio_codec = QComboBox()
        self.audio_codec.addItems(['aac', 'mp3', 'flac'])
        self.audio_codec.setCurrentText(self.settings.get('audio_codec'))

        self.audio_bitrate = QComboBox()
        self.audio_bitrate.addItems(['128k', '192k', '256k', '320k'])
        self.audio_bitrate.setCurrentText(self.settings.get('audio_bitrate'))

        self.logging_level = QComboBox()
        self.logging_level.addItems(['DEBUG', 'INFO', 'WARNING', 'ERROR'])
        self.logging_level.setCurrentText(self.settings.get('logging_level'))

        advanced_layout.addRow("Video Codec:", self.video_codec)
        advanced_layout.addRow("Audio Codec:", self.audio_codec)
        advanced_layout.addRow("Audio Bitrate:", self.audio_bitrate)
        advanced_layout.addRow("Logging Level:", self.logging_level)
        
        advanced_tab.setLayout(advanced_layout)

        # Appearance Tab
        appearance_tab = QWidget()
        appearance_layout = QFormLayout()

        self.theme = QComboBox()
        self.theme.addItems(QStyleFactory.keys())
        self.theme.setCurrentText(self.settings.get('theme'))
        self.theme.currentTextChanged.connect(self.on_theme_change)

        self.dark_mode = QCheckBox("Enable Dark Mode")
        self.dark_mode.setChecked(self.settings.get('dark_mode') == 'true')

        appearance_layout.addRow("Theme:", self.theme)
        appearance_layout.addRow("", self.dark_mode)
        
        appearance_tab.setLayout(appearance_layout)

        # Add tabs
        tabs.addTab(general_tab, "General")
        tabs.addTab(advanced_tab, "Advanced")
        tabs.addTab(appearance_tab, "Appearance")

        # Buttons
        button_layout = QHBoxLayout()
        help_button = QPushButton("?")
        help_button.setFixedWidth(30)
        help_button.clicked.connect(self.open_help)
        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")
        save_button.clicked.connect(self.save_settings)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(help_button)
        button_layout.addStretch()
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        layout.addWidget(tabs)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def on_theme_change(self, theme):
        unsupported_themes = ['windowsvista', 'Macintosh']  # Remove 'Windows' from unsupported themes
        if theme in unsupported_themes:
            self.previous_dark_mode = self.dark_mode.isChecked()
            self.dark_mode.setChecked(False)
            self.dark_mode.setEnabled(False)
        else:
            if hasattr(self, 'previous_dark_mode'):
                self.dark_mode.setChecked(self.previous_dark_mode)
            self.dark_mode.setEnabled(True)

    def browse_output_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Select Default Output Folder",
            self.output_folder.text()
        )
        if folder:
            self.output_folder.setText(folder)

    def browse_ffmpeg(self):
        file_filter = "FFmpeg executable (*)"
        if sys.platform == "win32":
            file_filter = "FFmpeg executable (*.exe)"
        
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select FFmpeg Executable",
            self.ffmpeg_path.text(), file_filter
        )
        if file_path:
            self.ffmpeg_path.setText(file_path)

    def open_help(self):
        import webbrowser
        webbrowser.open('https://github.com/RGB-Outl4w')

    def save_settings(self):
        self.settings.set('default_output_folder', self.output_folder.text())
        self.settings.set('ffmpeg_path', self.ffmpeg_path.text())
        self.settings.set('video_template', self.video_template.text())
        self.settings.set('audio_template', self.audio_template.text())
        self.settings.set('video_codec', self.video_codec.currentText())
        self.settings.set('audio_codec', self.audio_codec.currentText())
        self.settings.set('audio_bitrate', self.audio_bitrate.currentText())
        self.settings.set('logging_level', self.logging_level.currentText())
        self.settings.set('theme', self.theme.currentText())
        self.settings.set('dark_mode', str(self.dark_mode.isChecked()).lower())

        # Force settings to sync
        self.settings.settings.sync()
        self.accept()
