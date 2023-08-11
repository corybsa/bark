import dearpygui.dearpygui as dpg
from wgbark import VoiceGenerator
from .base_window import BaseWindow


class PromptWindow(BaseWindow):
  def __init__(self, generator: VoiceGenerator):
    self.generator = generator
    self.tag = 'prompt_window'
    self.info_modal_tag = self.get_random_tag()

    with dpg.window(label='Speech Generation', tag=self.tag, show=False, pos=[225, 160]):
      self.create_prompt_input()
      self.create_buttons()
  

  def create_prompt_input(self):
    dpg.add_text('Prompt:')
    dpg.add_input_text(
      tag='prompt_input',
      multiline=True,
      width=300,
      default_value='',
      hint='Enter your prompt here...'
    )
  

  def create_buttons(self):
    with dpg.group(horizontal=True):
      dpg.add_button(
        label='Generate speech',
        callback=lambda: self.generate_speech()
      )


  def generate_speech(self):
    self.open_modal('Hang tight, generating speech...', self.info_modal_tag)

    self.generator.generate_speech(
      'this is a test from dear pie gooey',
      callback=self.close_generate_speech_modal
    )
  

  def close_generate_speech_modal(self):
    dpg.delete_item(self.info_modal_tag)

