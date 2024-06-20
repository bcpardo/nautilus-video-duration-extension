import os
import subprocess
from gi.repository import Nautilus, GObject

class VideoDurationColumnExtension(GObject.GObject, Nautilus.ColumnProvider, Nautilus.InfoProvider):

    def __init__(self):
        pass

    def get_columns(self):
        return [Nautilus.Column(name="NautilusPython::video_duration_column",
                                attribute="video_duration",
                                label="Duration",
                                description="Shows the duration of video files")]

    def update_file_info(self, file):
        if file.get_mime_type().startswith("video"):
            file_path = file.get_location().get_path()
            try:
                result = subprocess.run(['mediainfo', '--Inform=Video;%Duration%', file_path],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        text=True)
                duration_ms = int(result.stdout.strip())
                duration = self.convert_millis(duration_ms)
                file.add_string_attribute('video_duration', duration)
            except Exception as e:
                file.add_string_attribute('video_duration', '')
        else:
            file.add_string_attribute('video_duration', '')

    def convert_millis(self, millis):
        seconds = (millis / 1000) % 60
        minutes = (millis / (1000 * 60)) % 60
        hours = (millis / (1000 * 60 * 60)) % 24
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
