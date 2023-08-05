from bark import SAMPLE_RATE, generate_audio, preload_models, save_as_prompt, generation
from scipy.io.wavfile import write as write_wav
import numpy as np
import sys
import os
from pathlib import Path
from colorama import init as colorama_init, Fore, Style


class VoiceGenerator:
     def __init__(self):
          self.current_voice_model = None
          self.current_voice_model_name = None
          self.text_temp = 0.7
          self.waveform_temp = 0.7
          self.is_using_built_in_model = True
          self.cwd = os.path.dirname(sys.argv[0])
          self.voice_models_dir = os.path.join(self.cwd, 'voice_models')
          self.generated_output_dir = os.path.join(self.cwd, 'output')

          self.main_menu = {
               'Load a voice model': self.load_voice_model,
               'Create a new voice model': self.prompt_for_built_in_voice_models,
               'Continue with current voice model': self.continue_with_current_voice_model,
               'Exit': exit
          }

          self.generate_audio_menu = {
               'Generate audio': self.prompt_for_text_to_speech,
               'Save current voice model': self.save_voice_model,
               'Adjust text generation temperature': self.prompt_for_text_temp,
               'Adjust waveform generation temperature': self.prompt_for_waveform_temp,
               'Back': lambda : self.present_menu(self.main_menu)
          }

          Path(self.voice_models_dir).mkdir(exist_ok=True)
          Path(self.generated_output_dir).mkdir(exist_ok=True)


     def cls(self):
          os.system('cls' if os.name=='nt' else 'clear')
     

     def print(self, message, color=Fore.WHITE):
          print(f'{color}{message}{Style.RESET_ALL}')


     def present_menu(self, menu_items):
          self.print(f'\n(using voice model \'{self.current_voice_model_name}\')', Fore.CYAN)
          self.print(f'(text generation temperature: {self.text_temp}, waveform generation temperature: {self.waveform_temp})', Fore.CYAN)
          self.print('Choose an option to continue:')

          # display menu items
          items = list(menu_items.items())
          for i in range(len(items)):
               self.print(str(i + 1) + ': ' + items[i][0])

          # get user input and show error if they did not enter a number
          try:
               choice = int(input('Enter your choice: '))
          except:
               self.print(f'\nInvalid choice. Please enter a number between 1 and {len(menu_items.items())}.', Fore.RED)
               self.present_menu(menu_items)
               return

          # show error if they entered a number that is not in the menu
          if choice < 1 or choice > len(menu_items):
               self.print(f'\nInvalid choice. Please enter a number between 1 and {len(menu_items.items())}.', Fore.RED)
               self.present_menu(menu_items)
               return

          # call the function associated with the menu item
          items[choice - 1][1]()
     

     def save_voice_model(self):
          if self.is_using_built_in_model:
               self.generate_voice_model('generating new model')

               model_name = input('Enter a name for the model: ')
               model_name += '.npz'
               
               filepath = os.path.join(self.voice_models_dir, model_name)

               try:
                    save_as_prompt(filepath, self.current_voice_model)
               except:
                    self.print('\nPlease generate at least one audio sample before saving the voice model.', Fore.YELLOW)
                    self.present_menu(self.generate_audio_menu)
                    return

               self.print(f'\nVoice model saved to {filepath}.', Fore.GREEN)
               
               with np.load(filepath) as data:
                    self.current_voice_model_name = model_name.replace('.npz', '')
                    self.current_voice_model = {
                         'semantic_prompt': data['semantic_prompt'],
                         'coarse_prompt': data['coarse_prompt'],
                         'fine_prompt': data['fine_prompt']
                    }
               
               self.print(f'Changed current voice model to {model_name.replace(".npz", "")}.', Fore.CYAN)
               self.is_using_built_in_model = False
          else:
               filepath = os.path.join(self.voice_models_dir, self.current_voice_model_name + '.npz')
               save_as_prompt(filepath, self.current_voice_model)
               self.print(f'\nVoice model saved to {filepath}.', Fore.GREEN)


     def load_voice_model(self):
          # get saved voice models from the voice_models folder
          voices = [f for f in os.listdir(self.voice_models_dir) if os.path.isfile(os.path.join(self.voice_models_dir, f)) and f.endswith('.npz')]
          
          if len(voices) == 0:
               self.print(f'\nNo voice models found in {self.voice_models_dir}.\n', Fore.RED)
               self.present_menu(self.main_menu)
          else:
               print('\nSelect a voice model to load:')
               for i in range(len(voices)):
                    self.print(str(i + 1) + ': ' + voices[i])
               
               self.print(str(len(voices) + 1) + ': Back')

               try:
                    voice_choice = int(input('Enter your choice: '))
               except:
                    self.print(f'\nInvalid choice. Please enter a number between 1 and {len(voices)}.', Fore.RED)
                    self.load_voice_model()
                    return
               
               # user selected back, return to main menu
               if voice_choice == len(voices) + 1:
                    self.present_menu(self.main_menu)
                    return
               # show error if they entered a number that is not in the menu
               elif voice_choice < 1 or voice_choice > len(voices):
                    self.print(f'\nInvalid choice. Please enter a number between 1 and {len(voices)}.', Fore.RED)
                    self.load_voice_model()
                    return
                    
               with np.load(os.path.join(self.voice_models_dir, voices[voice_choice - 1])) as data:
                    self.current_voice_model_name = voices[voice_choice - 1].replace('.npz', '')
                    self.current_voice_model = {
                         'semantic_prompt': data['semantic_prompt'],
                         'coarse_prompt': data['coarse_prompt'],
                         'fine_prompt': data['fine_prompt']
                    }
                    self.is_using_built_in_model = False
               
               self.present_menu(self.generate_audio_menu)
     

     def continue_with_current_voice_model(self):
          if self.current_voice_model is None:
               self.print('\nNo voice model loaded.', Fore.RED)
               self.present_menu(self.main_menu)
               return
          else:
               self.present_menu(self.generate_audio_menu)


     def prompt_for_built_in_voice_models(self):
          self.print('\nA list of all the built-in preset voice models:')

          sorted_prompts = sorted(generation.ALLOWED_PROMPTS)

          for i in range(len(sorted_prompts)):
               self.print(str(i + 1) + ': ' + sorted_prompts[i])
          
          self.print(str(len(sorted_prompts) + 1) + ': Back')

          choice = input('Enter your choice or leave blank for default (default is v2/en_speaker_2): ')

          # user selected default
          if choice == '':
               self.current_voice_model = 'v2/en_speaker_2'
               self.current_voice_model_name = 'v2/en_speaker_2'
               self.is_using_built_in_model = True
               self.present_menu(self.generate_audio_menu)
               return
          
          try:
               choice_int = int(choice)
          except:
               self.print(f'\nInvalid choice. Please enter a number between 1 and {len(sorted_prompts)}.', Fore.RED)
               self.prompt_for_built_in_voice_models()
               return
          
          # user selected back, return to main menu
          if choice_int == len(sorted_prompts) + 1:
               self.present_menu(self.main_menu)
               return
          # show error if they entered a number that is not in the menu
          elif choice_int < 1 or choice_int > len(sorted_prompts):
               self.print(f'\nInvalid choice. Please enter a number between 1 and {len(sorted_prompts)}.', Fore.RED)
               self.prompt_for_built_in_voice_models()
               return
          
          self.current_voice_model = sorted_prompts[choice_int - 1]
          self.current_voice_model_name = sorted_prompts[choice_int - 1]
          self.is_using_built_in_model = True

          self.present_menu(self.generate_audio_menu)


     def prompt_for_text_to_speech(self):
          if self.current_voice_model is None:
               print('\nNo voice model loaded.')
               self.present_menu(self.main_menu)
               return

          self.print('\nNotes:')
          self.print('  - To suggest that the voice sing, add a music note (♪) to the start and end of the line.')
          self.print('  - To indicate the end of input, press ctrl+z then press enter (must be on a blank line).')
          self.print('  - To start over press ctrl+r at any point. Then indicate the end of input by pressing ctrl+z on a blank line.')
          self.print('  - To cancel and return to the main menu press ctrl+x at any point. Then indicate the end of input by pressing ctrl+z on a blank line.')
          self.print('\nEnter text to convert to speech')
          self.print('---------')

          text_prompt = ''.join(sys.stdin.readlines()).replace('\n', ' ')

          # ctrl+r
          if '\x12' in text_prompt:
               return
          # ctrl+x
          elif '\x18' in text_prompt or text_prompt == '':
               self.present_menu(self.generate_audio_menu)
               return
          elif text_prompt == '':
               self.print('\nPlease enter some text.', Fore.RED)
               self.prompt_for_text_to_speech()
               return
          
          self.generate_voice_model(text_prompt, save_audio=True)
          self.present_menu(self.generate_audio_menu)
     

     def prompt_for_filename(self):
          filename = input('\nEnter a filename for the audio (or ctrl+x to cancel): ')

          # ctrl+x
          if filename == '\x18':
               self.present_menu(self.main_menu)
               return

          return filename + '.wav'


     def prompt_for_text_temp(self):
          text_temp = input('\nEnter a text temperature (or ctrl+x to cancel): ')

          # ctrl+x
          if text_temp == '\x18':
               self.present_menu(self.main_menu)
               return

          try:
               text_temp = float(text_temp)
          except:
               self.print('\nInvalid temperature. Please enter a number between 0 and 1.', Fore.RED)
               self.prompt_for_text_temp()
               return
          
          self.text_temp = text_temp
          self.present_menu(self.generate_audio_menu)


     def prompt_for_waveform_temp(self):
          waveform_temp = input('\nEnter a waveform temperature (or ctrl+x to cancel): ')

          # ctrl+x
          if waveform_temp == '\x18':
               self.present_menu(self.main_menu)
               return

          try:
               waveform_temp = float(waveform_temp)
          except:
               self.print('\nInvalid temperature. Please enter a number between 0 and 1.', Fore.RED)
               self.prompt_for_waveform_temp()
               return
          
          self.waveform_temp = waveform_temp
          self.present_menu(self.generate_audio_menu)


     def generate_voice_model(self, text_prompt, save_audio=False):
          if save_audio:
               filename = self.prompt_for_filename()
               self.print('\nGenerating voice model and audio file...', Fore.CYAN)
          else:
               self.print('\nGenerating voice model...', Fore.CYAN)

          try:
               (model, audio) = generate_audio(
                    text_prompt,
                    history_prompt=self.current_voice_model,
                    text_temp=self.text_temp,
                    waveform_temp=self.waveform_temp,
                    output_full=True
               )
               self.current_voice_model = model

               # save audio to disk
               if save_audio:
                    filepath = os.path.join(self.generated_output_dir, filename)
                    write_wav(filepath, SAMPLE_RATE, audio)
                    self.print(f'\nFile written to \'{filepath}\'', Fore.GREEN)
               else:
                    self.print('\nVoice model generated', Fore.GREEN)
          except ValueError as e:
               self.print('Error: ' + str(e) + '\n', Fore.RED)
               self.current_voice_model = None
               self.current_voice_model_name = None
               return


def main():
     generator = VoiceGenerator()
     generator.cls()
     print(f'{Fore.CYAN}Loading voice models...{Style.RESET_ALL}')

     # download and load all models
     preload_models()
     generator.cls()
     print('Welcome to the Wakeful Games text to speech generator!\n')

     while(True):
          generator.present_menu(generator.main_menu)


if __name__ == "__main__":
     colorama_init()
     main()
