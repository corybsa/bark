import dearpygui.dearpygui as dpg
from wgbark import VoiceGenerator


class MainWindow:
  def __init__(self):
    self.generator = VoiceGenerator()
    self.main_window = 'main_window'
    self.preload_modal = 'preload_modal'
    self.progress_bar = 'progress_bar'
    self.generating_modal = 'generating_modal'

    dpg.create_context()
    dpg.create_viewport(title='Wakeful Games Text to Speech Generator')
    dpg.setup_dearpygui()
    dpg.show_viewport()

    self.create_main_window()

    dpg.start_dearpygui()
    dpg.destroy_context()


  def create_main_window(self):
    with dpg.window(label='Wakeful Games', tag=self.main_window, show=False):
      self.create_preload_modal()
      self.create_voice_model_dropdown()
      self.create_temperature_controls()
      self.create_generate_button()


  def create_preload_modal(self):
    self.generator.preload_models(self.preload_done)

    with dpg.window(label='Voices loading...', show=True, tag=self.preload_modal):
      dpg.set_primary_window(self.preload_modal, True)
      dpg.add_text('Preloading models, please wait...')
  

  def preload_done(self):
    dpg.delete_item(self.preload_modal)
    dpg.set_primary_window(self.main_window, True)
    dpg.configure_item(self.main_window, show=True)
  

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


  def create_voice_model_dropdown(self):
    dpg.add_combo(
      label='Voice model',
      items=self.generator.get_all_voice_models(),
      width=200,
      default_value='v2\\en_speaker_2',
      callback=lambda id, value: self.generator.set_voice_model(value)
    )


  def create_generate_button(self):
    dpg.add_button(
      label='Generate',
      callback=lambda: self.generate_speech()
    )
  

  def generate_speech(self):
    height = 100
    width = 300
    y = (dpg.get_viewport_height() / 2) - (height / 2)
    x = (dpg.get_viewport_width() / 2) - (width / 2)

    with dpg.window(
      label='Generating speech...',
      tag=self.generating_modal,
      show=True,
      modal=True,
      no_close=True,
      no_collapse=True,
      no_resize=True,
      no_move=True,
      no_title_bar=True,
      pos=[x, y],
      width=width,
      height=height
    ):
      dpg.add_text('Hang tight, generating speech...')

    self.generator.generate_voice_model('this is a test from dear pie gooey', callback=self.close_generate_speech_modal)
  

  def close_generate_speech_modal(self):
    dpg.delete_item(self.generating_modal)

