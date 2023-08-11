import dearpygui.dearpygui as dpg
from wgbark import VoiceGenerator
import os
from .base_window import BaseWindow

class SpeechGenerationWindow(BaseWindow):
  def __init__(self, generator: VoiceGenerator):
    self.generator = generator
    self.tag = 'voice_generation_window'
    self.current_voice_model_label = 'current_voice_model_label'
    self.built_in_voice_model_dialog_tag = 'built_in_voice_model_dialog'
    self.voice_model_dialog_tag = 'voice_model_dialog'
    self.info_modal_tag = 'info_modal'
    self.generation_callback = None

    with dpg.window(label='Voice Generation', tag=self.tag, show=False, pos=[20, 20]):
      self.create_voice_model_controls()
      self.create_temperature_controls()
      self.create_buttons()
      self.create_load_voice_model_dialogs()


  def create_voice_model_controls(self):
    self.generator.set_voice_model('v2\\en_speaker_2')
    dpg.add_text(f'Current voice model: {self.generator.get_voice_model_name()}', tag=self.current_voice_model_label)
    dpg.add_separator()

    with dpg.group(horizontal=True):
      dpg.add_button(
        label='Load saved voice model',
        callback=lambda: dpg.show_item(self.voice_model_dialog_tag)
      )

      dpg.add_button(
        label='Load built-in voice model',
        callback=lambda: dpg.show_item(self.built_in_voice_model_dialog_tag)
      )


  def create_temperature_controls(self):
    dpg.add_slider_float(
      label='Text temperature',
      default_value=0.7,
      min_value=0.0,
      max_value=1.0,
      clamped=True,
      width=200,
      callback=lambda id, value: self.generator.set_text_temp(value)
    )

    dpg.add_slider_float(
      label='Waveform temperature',
      default_value=0.7,
      min_value=0.0,
      max_value=1.0,
      clamped=True,
      width=200,
      callback=lambda id, value: self.generator.set_waveform_temp(value)
    )
  

  def create_buttons(self):
    with dpg.group(horizontal=True):
      dpg.add_button(
        label='Generate speech',
        callback=lambda: self.generate_speech()
      )
  

  def create_load_voice_model_dialogs(self):
    # user saved voice models
    with dpg.file_dialog(
      tag=self.voice_model_dialog_tag,
      directory_selector=False,
      show=False,
      width=600,
      height=400,
      file_count=1,
      default_path=self.generator.get_user_voice_models_dir(),
      callback=lambda id, value: self.load_voice_model(list(value['selections'])[0])
    ):
      dpg.add_file_extension('.npz')
    
    # built in voice models
    with dpg.file_dialog(
      tag=self.built_in_voice_model_dialog_tag,
      directory_selector=False,
      show=False,
      width=600,
      height=400,
      file_count=1,
      default_path=self.generator.get_built_in_voice_models_dir(),
      callback=lambda id, value: self.load_voice_model(list(value['selections'])[0])
    ):
      dpg.add_file_extension('.npz')


  def generate_speech(self):
    self.open_modal('Hang tight, generating speech...', self.info_modal_tag)

    self.generator.generate_voice_model(
      'this is a test from dear pie gooey',
      callback=self.close_generate_speech_modal
    )
  

  def close_generate_speech_modal(self):
    dpg.delete_item(self.info_modal_tag)

    if self.generation_callback is not None:
      self.generation_callback()
  

  def load_voice_model(self, model_name: str):
    self.generator.set_voice_model(model_name)
    dpg.set_value(self.current_voice_model_label, f'Current voice model: {self.generator.get_voice_model_name()}')


  def set_generate_speech_callback(self, callback):
    self.generation_callback = callback

