import dearpygui.dearpygui as dpg
from wgbark import VoiceGenerator
from .base_window import BaseWindow
import wave
import time
import sys
from pyaudio import PyAudio, paContinue
import pyaudio as pa

class AudioWindow(BaseWindow):
  def __init__(self, generator: VoiceGenerator):
    self.generator = generator
    self.tag = 'audio_window'
    self.pyAudio = PyAudio()

    with dpg.window(label='Audio', tag=self.tag, show=False, pos=[400, 20]):
      self.create_audio_controls()
  

  def __del__(self):
    self.pyAudio.terminate()
  

  def create_audio_controls(self):
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
        stream = self.pyAudio.open(
          format=self.pyAudio.get_format_from_width(wf.getsampwidth()),
          channels=wf.getnchannels(),
          rate=wf.getframerate(),
          output=True,
          stream_callback=lambda in_data, frame_count, time_info, status: self.playback_callback(wf, stream, frame_count)
        )
    except FileNotFoundError:
      print('No audio file found')
      return
  

  def playback_callback(self, wf: wave.Wave_read, stream: PyAudio.Stream, frame_count):
    print(f'DEBUG: frame_count: {frame_count}')
    data = wf.readframes(frame_count)
    print(f'DEBUG: len(data): {len(data)}')

    if len(data) <= 0:
      stream.close()

    return (data, paContinue)

