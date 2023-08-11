import dearpygui.dearpygui as dpg
from wgbark import VoiceGenerator
import os
from .base_window import BaseWindow
from .save_window import SaveWindow
from .generation_options_window import GenerationOptionsWindow
from .audio_window import AudioWindow
from .prompt_window import PromptWindow


class MainWindow(BaseWindow):
  def __init__(self):
    self.generator = VoiceGenerator()
    self.preload_modal_tag = self.get_random_tag()
    self.preload_modal_text_tag = self.get_random_tag()
    self.generation_options_window = None
    self.save_window = None
    self.audio_window = None
    self.prompt_window = None

    dpg.create_context()

    if(os.path.isfile('bark.ini') and os.path.exists('bark.ini')):
      dpg.configure_app(init_file='bark.ini')
    
    dpg.create_viewport(
      title='Wakeful Games Text to Speech Generator',
      width=800,
      height=600
    )
    dpg.setup_dearpygui()
    dpg.show_viewport()

    self.create_windows()

    dpg.start_dearpygui()
    dpg.destroy_context()


  def create_windows(self):
    self.generation_options_window = GenerationOptionsWindow(self.generator)
    self.audio_window = AudioWindow(self.generator)
    self.save_window = SaveWindow(self.generator)
    self.prompt_window = PromptWindow(self.generator)

    self.create_preload_modal()


  def create_preload_modal(self):
    self.generator.preload_models(self.preload_done)

    with dpg.window(label='Voices loading...', show=True, tag=self.preload_modal_tag):
      dpg.set_primary_window(self.preload_modal_tag, True)
      dpg.add_text('Preloading models, please wait...', tag=self.preload_modal_text_tag)
  

  def preload_done(self):
    dpg.delete_item(self.preload_modal_text_tag)
    self.generation_options_window.show()
    self.save_window.show()
    self.audio_window.show()
    self.prompt_window.show()

