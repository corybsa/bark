import dearpygui.dearpygui as dpg
from wgbark import VoiceGenerator
from .base_window import BaseWindow


class SaveWindow(BaseWindow):
  def __init__(self, generator: VoiceGenerator):
    self.generator = generator
    self.tag = 'save_window'
    self.save_file_modal = 'save_file_modal'
    self.save_file_modal_text = 'save_file_modal_text'

    with dpg.window(label='Save', tag=self.tag, show=False, pos=[20, 160]):
      self.create_voice_model_name_input()
      self.create_buttons()
  

  def create_voice_model_name_input(self):
    dpg.add_input_text(
      label='Voice model name',
      tag=self.save_file_modal_text,
      default_value=self.generator.get_voice_model_name(),
      width=200
    )
  

  def create_buttons(self):
    with dpg.group(horizontal=True):
      dpg.add_button(
        label='Save config',
        callback=lambda: dpg.save_init_file('config.ini')
      )

      dpg.add_button(
        label='Save current voice model',
        callback=lambda: self.save_voice_model()
      )
  

  def save_voice_model(self):
    voice_model_filename = dpg.get_value(self.save_file_modal_text)
    saved_file = self.generator.save_voice_model(voice_model_filename)

    self.open_modal(
      f'Voice model saved to\n{saved_file}',
      self.save_file_modal,
      no_close=False
    )

