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

    def update_file_info_full(self, provider, handle, closure, file):
        duration = ''
        if file.get_mime_type().startswith("video"):
            GObject.timeout_add_seconds(1, self.update_duration, provider, handle, closure, file)
            return Nautilus.OperationResult.IN_PROGRESS
            
        file.add_string_attribute('video_duration', duration)
        
        return Nautilus.OperationResult.COMPLETE
            
    def update_duration(self, provider, handle, closure, file):
        file_path = file.get_location().get_path()
        try:
            result = subprocess.run(['mediainfo', '--Inform=Video;%Duration%', file_path],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True)
            duration_ms = int(result.stdout.strip())
            duration = self.convert_millis(duration_ms)
        except Exception as e:
            duration = ''
            
        file.add_string_attribute('video_duration', duration)
        
        Nautilus.info_provider_update_complete_invoke(closure, provider, 
                               handle, Nautilus.OperationResult.COMPLETE)

        return False

    def convert_millis(self, millis):
        seconds = (millis / 1000) % 60
        minutes = (millis / (1000 * 60)) % 60
        hours = (millis / (1000 * 60 * 60)) % 24
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
