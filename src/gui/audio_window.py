import dearpygui.dearpygui as dpg
from bark import SAMPLE_RATE
from wgbark import VoiceGenerator
from .base_window import BaseWindow
import wave
import time
import sys
import pyaudio as pa

class AudioWindow(BaseWindow):
  def __init__(self, generator: VoiceGenerator):
    self.generator = generator
    self.tag = 'audio_window'
    self.progress_bar_tag = 'playback_progress_bar'
    self.progress_bar_label = 'progress_bar_label'
    self.total_audio_duration = 0.0
    self.playback_position = 0

    with dpg.window(label='Audio', tag=self.tag, show=False, pos=[400, 20]):
      self.create_audio_controls()
  

  def create_audio_controls(self):
    with dpg.group(horizontal=True):
      dpg.add_progress_bar(
        label='progress bar',
        tag=self.progress_bar_tag,
        default_value=self.playback_position,
        overlay='',
        width=100
      )

      dpg.add_text(f'00:00/{self.get_time(self.total_audio_duration)}', tag=self.progress_bar_label)
    
    with dpg.group(horizontal=True):
      dpg.add_button(
        label='Play',
        callback=lambda: self.play_audio_file()
      )

      dpg.add_button(
        label='Save audio to file',
        callback=lambda: print('not implemented yet')
      )
  

  def play_audio_file(self):
    try:
      with wave.open(self.generator.get_temp_audio_file(), 'rb') as wf:
        total_frames = wf.getnframes()
        self.total_audio_duration = wf.getnframes() / wf.getframerate()
        self.playback_position = 0

        # Define callback for playback (1)
        def callback(in_data, frame_count, time_info, status):
          data = wf.readframes(frame_count)
          current_frame = wf.tell()
          playback_percentage = current_frame / total_frames
          self.playback_position = int(playback_percentage * self.total_audio_duration)

          dpg.set_value(self.progress_bar_tag, self.playback_position / int(self.total_audio_duration))
          dpg.set_value(self.progress_bar_label, f'{self.get_time(self.playback_position)}/{self.get_time(self.total_audio_duration)}')
          
          return (data, pa.paContinue)

        p = pa.PyAudio()

        stream = p.open(
          format=p.get_format_from_width(wf.getsampwidth()),
          channels=wf.getnchannels(),
          rate=wf.getframerate(),
          output=True,
          stream_callback=callback
        )

        while stream.is_active():
          time.sleep(0.1)

        stream.close()

        p.terminate()
    except FileNotFoundError:
      self.open_modal('No audio file found', 'no_audio_found_modal', no_close=False)
  

  def get_time(self, num: int):
    min = int(num / 60)
    sec = int(num % 60)
    return f'{min:02d}:{sec:02d}'


  def update_audio_info(self):
    pass

