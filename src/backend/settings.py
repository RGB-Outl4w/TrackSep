from PyQt5.QtCore import QSettings
from pathlib import Path

class Settings:
    def __init__(self):
        self.settings = QSettings('TrackSep', 'VideoAudioSeparator')
        self.defaults = {
            'default_output_folder': str(Path.home() / 'Videos'),
            'ffmpeg_path': 'ffmpeg',
            'video_template': '{filename}_video',
            'audio_template': '{filename}_audio',
            'theme': 'Fusion',
            'logging_level': 'INFO',
            'video_codec': 'copy',
            'audio_codec': 'aac',
            'audio_bitrate': '192k',
            'dark_mode': False
        }
        self.load_settings()

    def load_settings(self):
        for key, default in self.defaults.items():
            if not self.settings.contains(key):
                self.settings.setValue(key, default)

    def get(self, key):
        return self.settings.value(key, self.defaults.get(key))

    def set(self, key, value):
        self.settings.setValue(key, value)
