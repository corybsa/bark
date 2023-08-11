import dearpygui.dearpygui as dpg
from wgbark import VoiceGenerator
import os
from .save_window import SaveWindow
from .speech_generation_window import SpeechGenerationWindow
from .audio_window import AudioWindow


class MainWindow:
  def __init__(self):
    self.generator = VoiceGenerator()
    self.preload_modal = 'preload_modal'
    self.preload_modal_text = 'preload_modal_text'
    self.progress_bar = 'progress_bar'
    self.save_file_modal = 'save_file_modal'
    self.voice_generation_window = None
    self.save_window = None
    self.audio_window = None

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
    self.save_window = SaveWindow(self.generator)
    self.audio_window = AudioWindow(self.generator)
    self.voice_generation_window = SpeechGenerationWindow(self.generator)

    self.voice_generation_window.set_generate_speech_callback(self.voice_generation_done)

    self.create_preload_modal()


  def create_preload_modal(self):
    self.generator.preload_models(self.preload_done)

    with dpg.window(label='Voices loading...', show=True, tag=self.preload_modal):
      dpg.set_primary_window(self.preload_modal, True)
      dpg.add_text('Preloading models, please wait...', tag=self.preload_modal_text)
  

  def preload_done(self):
    dpg.delete_item(self.preload_modal_text)
    self.voice_generation_window.show()
    self.save_window.show()
    self.audio_window.show()
  

  def voice_generation_done(self):
    print('done')

