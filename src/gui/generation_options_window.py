import dearpygui.dearpygui as dpg
from wgbark import VoiceGenerator
from .base_window import BaseWindow

class GenerationOptionsWindow(BaseWindow):
  def __init__(self, generator: VoiceGenerator):
    self.generator = generator
    self.tag = 'voice_generation_window'
    self.current_voice_model_label_tag = self.get_random_tag()
    self.built_in_voice_model_dialog_tag = self.get_random_tag()
    self.voice_model_dialog_tag = self.get_random_tag()
    self.text_temp_tag = self.get_random_tag()
    self.waveform_temp_tag = self.get_random_tag()

    with dpg.window(label='Speech Generation Settings', tag=self.tag, show=False, pos=[20, 20], no_close=True):
      self.create_voice_model_controls()
      self.create_temperature_controls()
      self.create_load_voice_model_dialogs()


  def create_voice_model_controls(self):
    self.generator.set_voice_model('v2\\en_speaker_2')
    dpg.add_text(f'Current voice model: {self.generator.get_voice_model_name()}', tag=self.current_voice_model_label_tag)

    with dpg.group(horizontal=True):
      dpg.add_button(
        label='Load custom voice model',
        callback=lambda: dpg.show_item(self.voice_model_dialog_tag)
      )

      dpg.add_button(
        label='Load built-in voice model',
        callback=lambda: dpg.show_item(self.built_in_voice_model_dialog_tag)
      )
    
    dpg.add_separator()


  def create_temperature_controls(self):
    dpg.add_slider_float(
      label='Text temperature (?)',
      tag=self.text_temp_tag,
      default_value=0.7,
      min_value=0.0,
      max_value=1.0,
      clamped=True,
      width=200,
      callback=lambda id, value: self.generator.set_text_temp(value)
    )

    with dpg.tooltip(self.text_temp_tag):
      dpg.add_text('''This parameter determines the creativity and diversity of the speech generated.
Higher values will allow the model to take more risks and to be more creative with its word choice,
lower values will result in speech that is closer to the entered prompt.
This value is generally between 0.5 and 0.9 (default is 0.7)''')

    dpg.add_slider_float(
      label='Waveform temperature (?)',
      tag=self.waveform_temp_tag,
      default_value=0.7,
      min_value=0.0,
      max_value=1.0,
      clamped=True,
      width=200,
      callback=lambda id, value: self.generator.set_waveform_temp(value)
    )

    with dpg.tooltip(self.waveform_temp_tag):
      dpg.add_text('''Waveform temperature controls how random the generated audio is.
Higher values will result in more random noises (music, people in the background, etc.),
lower values will result in less random noises.
This value is generally between 0.5 and 0.9 (default is 0.7)''')
  

  def create_load_voice_model_dialogs(self):
    # user saved voice models
    with dpg.file_dialog(
      tag=self.voice_model_dialog_tag,
      directory_selector=False,
      show=False,
      default_filename='',
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
      default_filename='',
      width=600,
      height=400,
      file_count=1,
      default_path=self.generator.get_built_in_voice_models_dir(),
      callback=lambda id, value: self.load_voice_model(list(value['selections'])[0], is_built_in=True)
    ):
      dpg.add_file_extension('.npz')
  

  def load_voice_model(self, model_name: str, is_built_in = False):
    if is_built_in:
      model_name = model_name.replace('.npz', '')

    self.generator.set_voice_model(model_name)
    dpg.set_value(self.current_voice_model_label_tag, f'Current voice model: {self.generator.get_voice_model_name()}')

