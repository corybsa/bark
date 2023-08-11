import dearpygui.dearpygui as dpg
from wgbark import VoiceGenerator
from .base_window import BaseWindow


class PromptWindow(BaseWindow):
  def __init__(self, generator: VoiceGenerator):
    self.generator = generator
    self.tag = 'prompt_window'
    self.prompt_tag = self.get_random_tag()
    self.info_modal_tag = self.get_random_tag()
    self.generate_and_learn_tag = self.get_random_tag()
    self.prompt_hint_tag = self.get_random_tag()

    with dpg.window(label='Speech Generation', tag=self.tag, show=False, pos=[225, 160], no_close=True):
      self.create_prompt_input()
      self.create_buttons()
  

  def create_prompt_input(self):
    with dpg.group(horizontal=True):
      dpg.add_text('Prompt:')
      dpg.add_text('(?)', tag=self.prompt_hint_tag)

      with dpg.tooltip(self.prompt_hint_tag):
        dpg.add_text('''You can nudge the AI generate non-speech sounds by using the following tags in your prompt:
[laughter]
[laughs]
[sighs]
[music]
[gasps]
[clears throat]
... for hesitations
CAPITALIZATION for emphasis of a word
[MAN] and [WOMAN] to bias Bark toward male and female speakers, respectively.
And others that are not even known yet. Experiment with it!

Example prompt with non-speech sounds:
  Hello, my name is Suno. And, uh... and I like pizza. [laughs] 
  But I also have other interests such as playing tic tac toe.
''')

    dpg.add_input_text(
      tag=self.prompt_tag,
      multiline=True,
      width=500,
      default_value='',
      hint='Enter your prompt here...'
    )
  

  def create_buttons(self):
    dpg.add_button(label='Generate speech', callback=lambda: self.generate_speech(should_learn=False))
    dpg.add_button(label='Generate speech and learn', tag=self.generate_and_learn_tag, callback=lambda: self.generate_speech(should_learn=True))

    with dpg.tooltip(self.generate_and_learn_tag):
      dpg.add_text('This will generate speech, learn from it, and update the voice model, for better or worse :).\nThe new voice model will not be saved automatically.')


  def generate_speech(self, should_learn=False):
    prompt = dpg.get_value(self.prompt_tag)

    if prompt == '':
      self.open_modal('Please enter a prompt.', no_close=False)
      return
    
    self.open_modal('Hang tight, generating speech...', self.info_modal_tag)
    self.generator.generate_speech(prompt, should_learn=should_learn, callback=self.close_generate_speech_modal)
  

  def close_generate_speech_modal(self):
    dpg.delete_item(self.info_modal_tag)

