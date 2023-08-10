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
    self.pyAudio = pa.PyAudio()
    self.audio_duration = 0
    self.playback_position = 0

    with dpg.window(label='Audio', tag=self.tag, show=False, pos=[400, 20]):
      self.create_audio_controls()
  

  def __del__(self):
    self.pyAudio.terminate()
  

  def create_audio_controls(self):
    dpg.add_progress_bar(
      label='progress bar',
      default_value=self.playback_position,
      overlay='00:00'
    )

    dpg.add_slider_int(
      label='slider',
      default_value=self.playback_position,
      enabled=False
    )
    
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
        self.audio_duration = wf.getnframes() / wf.getframerate()
        self.playback_position = 0

        # Define callback for playback (1)
        def callback(in_data, frame_count, time_info, status):
          data = wf.readframes(frame_count)
          current_frame = wf.tell()
          playback_percentage = current_frame / total_frames
          self.playback_position = int(playback_percentage * self.audio_duration)
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
      print('No audio file found')

