import dearpygui.dearpygui as dpg
from wgbark import VoiceGenerator
import sys
import os


class MainWindow:
  def __init__(self):
    self.generator = VoiceGenerator()
    self.main_window = 'main_window'
    self.preload_modal = 'preload_modal'
    self.settings_window = 'settings_window'
    self.config_dir = os.path.dirname(sys.argv[0])
    self.config_folder = 'config'
    self.config_filename = 'config.ini'
    self.config_path = os.path.join(self.config_dir, self.config_folder, self.config_filename)
    self.is_preload_done = False

    dpg.create_context()
    dpg.create_viewport(title='Wakeful Games Text to Speech Generator')
    dpg.setup_dearpygui()
    dpg.show_viewport()

    self.create_main_window()

    dpg.start_dearpygui()
    dpg.destroy_context()


  def create_main_window(self):
    with dpg.window(label="Wakeful Games", tag=self.main_window, show=False):
      self.create_preload_modal()
      self.create_settings_window()


  def create_preload_modal(self):
    self.generator.preload_models(self.preload_done)

    with dpg.window(label='Voices loading...', show=True, tag=self.preload_modal):
      dpg.set_primary_window(self.preload_modal, True)
      dpg.add_text('Preloading models, please wait...')
  

  def preload_done(self):
    dpg.delete_item(self.preload_modal)
    dpg.set_primary_window(self.main_window, True)
    dpg.configure_item(self.main_window, show=True)
    dpg.configure_item(self.settings_window, show=True)
    self.is_preload_done = True
  

  def create_settings_window(self):
    with dpg.window(label='Settings', tag=self.settings_window, show=False, no_close=True):
      self.create_temperature_controls()

      dpg.add_separator()

      with dpg.group(horizontal=True):
        dpg.add_button(label='Save window positions', callback=lambda: dpg.save_init_file(self.config_path))
  

  def create_temperature_controls(self):
    dpg.add_slider_float(
      label='Text temperature',
      default_value=0.7,
      min_value=0.0,
      max_value=1.0,
      clamped=True,
      callback=lambda id, value: self.generator.set_text_temp(value)
    )

    dpg.add_slider_float(
      label='Waveform temperature',
      default_value=0.7,
      min_value=0.0,
      max_value=1.0,
      clamped=True,
      callback=lambda id, value: self.generator.set_waveform_temp(value)
    )

