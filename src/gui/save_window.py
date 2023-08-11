import dearpygui.dearpygui as dpg
from wgbark import VoiceGenerator
import os
from .base_window import BaseWindow


class SaveWindow(BaseWindow):
  def __init__(self, generator: VoiceGenerator):
    self.generator = generator
    self.tag = 'save_window'
    self.save_file_dialog_tag = self.get_random_tag()

    with dpg.window(label='Save', tag=self.tag, show=False, pos=[20, 160], no_close=True):
      self.create_save_file_dialog()
      self.create_buttons()
  

  def create_buttons(self):
    dpg.add_button(
      label='Save current voice model',
      callback=lambda: dpg.show_item(self.save_file_dialog_tag)
    )
    
    dpg.add_button(
      label='Save window positions',
      callback=lambda: dpg.save_init_file('bark.ini')
    )
  

  def create_save_file_dialog(self):
    with dpg.file_dialog(
      tag=self.save_file_dialog_tag,
      directory_selector=False,
      show=False,
      default_filename='',
      width=600,
      height=400,
      file_count=-1,
      default_path=self.generator.get_user_voice_models_dir(),
      callback=lambda id, value: self.save_file(value['file_path_name'])
    ):
      dpg.add_file_extension('.npz')
  

  def save_file(self, filepath: str):
    filename = os.path.basename(filepath).split('.')[0]
    self.generator.save_voice_model(filename)

