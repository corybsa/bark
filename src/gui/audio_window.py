import dearpygui.dearpygui as dpg
from bark import SAMPLE_RATE
from wgbark import VoiceGenerator
from .base_window import BaseWindow
import wave
import time
import pyaudio as pa
import os

class AudioWindow(BaseWindow):
  def __init__(self, generator: VoiceGenerator):
    self.generator = generator
    self.tag = 'audio_window'
    self.progress_bar_tag = self.get_random_tag()
    self.progress_bar_label_tag = self.get_random_tag()
    self.save_file_dialog_tag = self.get_random_tag()
    self.update_voice_model_button_tag = self.get_random_tag()
    self.is_audio_file_loaded = False
    self.total_audio_duration = 0.0
    self.playback_position = 0

    self.generator.add_speech_generation_callback(self.update_audio_info)
    self.generator.add_speech_generation_callback(lambda: self.set_is_audio_file_loaded(True))

    with dpg.window(label='Audio Preview', tag=self.tag, show=False, pos=[625, 20], no_close=True):
      self.create_audio_controls()
      self.create_save_file_dialog()
  

  def set_is_audio_file_loaded(self, is_audio_file_loaded: bool):
    self.is_audio_file_loaded = is_audio_file_loaded
  

  def create_audio_controls(self):
    with dpg.group(horizontal=True):
      dpg.add_progress_bar(
        label='progress bar',
        tag=self.progress_bar_tag,
        default_value=self.playback_position,
        overlay='',
        width=100
      )

      dpg.add_text(f'00:00/{self.get_time(self.total_audio_duration)}', tag=self.progress_bar_label_tag)
    
    with dpg.group(horizontal=True):
      dpg.add_button(
        label='Play',
        callback=lambda: self.play_audio_file()
      )

      dpg.add_button(
        label='Save audio to file',
        callback=lambda: self.open_save_file_dialog()
      )
    
    dpg.add_button(label='Update current voice model', tag=self.update_voice_model_button_tag, callback=lambda: self.generator.update_current_voice_model_with_temp())

    with dpg.tooltip(self.update_voice_model_button_tag):
      dpg.add_text('''An updated voice model was generated along with the speech audio.
Click this button to update the current voice model with the updated voice model.
Note: the updated voice model is not automatically saved to file.
''')
  

  def open_save_file_dialog(self):
    if not self.is_audio_file_loaded:
      self.open_modal('No audio file loaded', no_close=False)
      return
    
    dpg.show_item(self.save_file_dialog_tag)
  

  def create_save_file_dialog(self):
    with dpg.file_dialog(
      tag=self.save_file_dialog_tag,
      directory_selector=False,
      show=False,
      default_filename='',
      width=600,
      height=400,
      file_count=-1,
      default_path=self.generator.generated_output_dir,
      callback=lambda id, value: self.save_audio_file(value['file_path_name'])
    ):
      dpg.add_file_extension('.wav')
  

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
          dpg.set_value(self.progress_bar_label_tag, f'{self.get_time(self.playback_position)}/{self.get_time(self.total_audio_duration)}')
          
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
      self.open_modal('No audio file loaded', no_close=False)
      self.reset_audio_info()
  

  def get_time(self, num: int):
    min = int(num / 60)
    sec = int(num % 60)
    return f'{min:02d}:{sec:02d}'


  def update_audio_info(self):
    try:
      with wave.open(self.generator.get_temp_audio_file(), 'rb') as wf:
        self.total_audio_duration = wf.getnframes() / wf.getframerate()
        self.playback_position = 0

        dpg.set_value(self.progress_bar_tag, self.playback_position / int(self.total_audio_duration))
        dpg.set_value(self.progress_bar_label_tag, f'{self.get_time(self.playback_position)}/{self.get_time(self.total_audio_duration)}')
        self.set_is_audio_file_loaded(True)
    except FileNotFoundError:
      self.open_modal('No audio file found', no_close=False)
      self.reset_audio_info()
  

  def save_audio_file(self, file_path: str):
    try:
      os.rename(self.generator.get_temp_audio_file(), file_path)
      self.open_modal(f'Audio saved to\n{file_path}', no_close=False)
      self.reset_audio_info()
    except FileNotFoundError:
      self.open_modal('No audio file loaded', no_close=False)
      self.reset_audio_info()
  

  def reset_audio_info(self):
    self.playback_position = 0
    self.total_audio_duration = 0
    dpg.set_value(self.progress_bar_tag, 0)
    dpg.set_value(self.progress_bar_label_tag, f'00:00/00:00')
    self.set_is_audio_file_loaded(False)

