import subprocess
import json
import logging

# Configure logger
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class StreamInfo:
    def __init__(self, input_file, ffmpeg_path):
        self.input_file = input_file
        self.ffmpeg_path = ffmpeg_path
        self.video_streams = []
        self.audio_streams = []
        self.probe_streams()

    def probe_streams(self):
        try:
            # Get ffprobe path from ffmpeg path
            ffprobe_path = self.ffmpeg_path.replace('ffmpeg', 'ffprobe')
            command = [
                ffprobe_path,
                "-v", "quiet",
                "-print_format", "json",
                "-show_streams",
                self.input_file
            ]
            result = subprocess.run(
                command, capture_output=True, text=True
            )
            
            if result.returncode != 0:
                logger.error(f"FFprobe failed: {result.stderr}")
                return

            streams = json.loads(result.stdout).get('streams', [])
            
            for stream in streams:
                if (stream['codec_type'] == 'video'):
                    self.video_streams.append({
                        'index': stream['index'],
                        'codec': stream['codec_name'],
                        'resolution': f"{stream.get('width', '?')}x{stream.get('height', '?')}"
                    })
                elif (stream['codec_type'] == 'audio'):
                    self.audio_streams.append({
                        'index': stream['index'],
                        'codec': stream['codec_name'],
                        'channels': stream.get('channels', '?'),
                        'sample_rate': stream.get('sample_rate', '?')
                    })
        except Exception as e:
            logger.error(f"Error probing streams: {str(e)}")
