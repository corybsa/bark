import dearpygui.dearpygui as dpg
from wgbark import VoiceGenerator
from .base_window import BaseWindow

class SpeechGenerationWindow(BaseWindow):
  def __init__(self, generator: VoiceGenerator):
    self.generator = generator
    self.tag = 'voice_generation_window'
    self.info_modal = 'info_modal'

    with dpg.window(label='Voice Generation', tag=self.tag, show=False, pos=[20, 20]):
      self.create_voice_model_dropdown()
      self.create_temperature_controls()
      self.create_buttons()


  def create_voice_model_dropdown(self):
    dpg.add_combo(
      label='Voice model',
      items=self.generator.get_all_voice_models(),
      width=200,
      default_value='v2\\en_speaker_2',
      callback=lambda id, value: self.generator.set_voice_model(value)
    )

    self.generator.set_voice_model('v2\\en_speaker_2')
  

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


  def generate_speech(self):
    self.open_modal('Hang tight, generating speech...', self.info_modal)

    self.generator.generate_voice_model(
      'this is a test from dear pie gooey',
      callback=self.close_generate_speech_modal
    )
  

  def close_generate_speech_modal(self):
    dpg.delete_item(self.info_modal)

