import os
import subprocess
import logging
from PyQt5.QtCore import QThread, pyqtSignal

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WorkerThread(QThread):
    progress = pyqtSignal(int)
    error = pyqtSignal(str)
    
    def __init__(self, input_file, output_video, output_audio, settings, video_stream=None, audio_stream=None):
        super().__init__()
        self.input_file = input_file
        self.output_video = output_video
        self.output_audio = output_audio
        self.settings = settings
        self.video_stream = video_stream
        self.audio_stream = audio_stream

    def run(self):
        try:
            ffmpeg_path = self.settings.get('ffmpeg_path')
            video_codec = self.settings.get('video_codec')
            audio_codec = self.settings.get('audio_codec')
            audio_bitrate = self.settings.get('audio_bitrate')

            # Video extraction command
            video_command = [ffmpeg_path, "-i", self.input_file]
            if self.video_stream is not None:
                video_command.extend(["-map", f"0:{self.video_stream}"])
            video_command.extend(["-c:v", video_codec])
            if video_codec == 'h265':  # Special case for h265
                video_command.extend(["-preset", "medium", "-crf", "28"])  # Example parameters
            elif video_codec == 'h264':  # Special case for h264
                video_command.extend(["-preset", "medium", "-crf", "23"])  # Example parameters
            elif video_codec == 'vp9':  # Special case for vp9
                video_command.extend(["-b:v", "2M"])  # Example parameters
            video_command.extend(["-an", self.output_video])

            # Determine the correct file extension for the audio output
            audio_extension = {
                'aac': 'm4a',
                'mp3': 'mp3',
                'flac': 'flac'
            }.get(audio_codec, 'm4a')

            output_audio_file = os.path.splitext(self.output_audio)[0] + f".{audio_extension}"

            # Audio extraction command
            audio_command = [ffmpeg_path, "-i", self.input_file]
            if self.audio_stream is not None:
                audio_command.extend(["-map", f"0:{self.audio_stream}"])
            audio_command.extend(["-vn", "-c:a", audio_codec])
            if audio_codec in ['aac', 'mp3']:  # bitrate only applies to certain codecs
                audio_command.extend(["-b:a", audio_bitrate])
            audio_command.extend(["-y", output_audio_file])  # Ensure output file is overwritten

            commands = [("Video", video_command), ("Audio", audio_command)]

            for index, (desc, command) in enumerate(commands):
                logger.info(f"Running {desc} command: {' '.join(command)}")  # Log the command
                process = subprocess.Popen(
                    command, stderr=subprocess.PIPE,
                    stdout=subprocess.PIPE, text=True  # Use text=True for stderr and stdout
                )
                stdout, stderr = process.communicate()

                if process.returncode != 0:
                    error_message = f"{desc} Extraction Failed: {stderr.strip()}"
                    logger.error(error_message)
                    self.error.emit(error_message)
                    return
                
                # Log output and error messages from FFmpeg
                if stdout:
                    logger.info(f"{desc} stdout:\n{stdout.strip()}") 
                if stderr:
                    logger.warning(f"{desc} stderr:\n{stderr.strip()}")  # Use warning for stderr

                self.progress.emit((index + 1) * 50)

            self.progress.emit(100)

        except FileNotFoundError as e:  # Handle file not found error
            error_message = f"File Not Found: {str(e)}"
            logger.exception(error_message)  # Log the exception with traceback
            self.error.emit(error_message)

        except Exception as e:  # Handle other exceptions
            error_message = f"An unexpected error occurred: {str(e)}"
            logger.exception(error_message)  # Log the exception with traceback
            self.error.emit(error_message)
