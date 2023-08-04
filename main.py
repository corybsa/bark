from bark import SAMPLE_RATE, generate_audio, preload_models, save_as_prompt, generation
from scipy.io.wavfile import write as write_wav
import numpy as np
import sys
import os
from pathlib import Path


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
               'Back': lambda : self.present_menu(self.main_menu)
          }

          Path(self.voice_models_dir).mkdir(exist_ok=True)
          Path(self.generated_output_dir).mkdir(exist_ok=True)


     def cls(self):
          os.system('cls' if os.name=='nt' else 'clear')
     

     def present_menu(self, menu_items):
          print(f'\n(using voice model \'{self.current_voice_model_name}\')')
          print('Choose an option to continue:')

          # display menu items
          items = list(menu_items.items())
          for i in range(len(items)):
               print(str(i + 1) + ': ' + items[i][0])

          # get user input and show error if they did not enter a number
          try:
               choice = int(input('Enter your choice: '))
          except:
               print(f'\nInvalid choice. Please enter a number between 1 and {len(menu_items.items())}.\n')
               self.present_menu(menu_items)
               return

          # show error if they entered a number that is not in the menu
          if choice < 1 or choice > len(menu_items):
               print(f'\nInvalid choice. Please enter a number between 1 and {len(menu_items.items())}.\n')
               self.present_menu(menu_items)
               return

          # call the function associated with the menu item
          items[choice - 1][1]()
     

     def save_voice_model(self):
          if self.is_using_built_in_model:
               model_name = input('Enter a name for the model: ')
               model_name += '.npz'
               
               filepath = os.path.join(self.voice_models_dir, model_name)

               try:
                    save_as_prompt(filepath, self.current_voice_model)
               except:
                    print('\nPlease generate at least one audio sample before saving the voice model.')
                    self.present_menu(self.generate_audio_menu)
                    return

               print('\nVoice model saved to ' + filepath + '.')
               
               with np.load(filepath) as data:
                    self.current_voice_model_name = model_name.replace('.npz', '')
                    self.current_voice_model = {
                         'semantic_prompt': data['semantic_prompt'],
                         'coarse_prompt': data['coarse_prompt'],
                         'fine_prompt': data['fine_prompt']
                    }
               
               print(f'Changed current voice model to {model_name.replace(".npz", "")}.')
               self.is_using_built_in_model = False
          else:
               filepath = os.path.join(self.voice_models_dir, model_name)
               save_as_prompt(filepath, self.current_voice_model)
               print('Voice model saved to ' + filepath + '.\n')


     def load_voice_model(self):
          # get saved voice models from the voice_models folder
          voices = [f for f in os.listdir(self.voice_models_dir) if os.path.isfile(os.path.join(self.voice_models_dir, f)) and f.endswith('.npz')]
          
          if len(voices) == 0:
               print('\nNo voice models found in ' + self.voice_models_dir + '.\n')
               self.present_menu(self.main_menu)
          else:
               print('\nSelect a voice model to load:')
               for i in range(len(voices)):
                    print(str(i + 1) + ': ' + voices[i])
               
               print(str(len(voices) + 1) + ': Back')

               try:
                    voice_choice = int(input('Enter your choice: '))
               except:
                    print(f'\nInvalid choice. Please enter a number between 1 and {len(voices)}.')
                    self.load_voice_model()
                    return
               
               # user selected back, return to main menu
               if voice_choice == len(voices) + 1:
                    self.present_menu(self.main_menu)
                    return
               # show error if they entered a number that is not in the menu
               elif voice_choice < 1 or voice_choice > len(voices):
                    print(f'\nInvalid choice. Please enter a number between 1 and {len(voices)}.')
                    self.load_voice_model()
                    return
                    
               with np.load(os.path.join(self.voice_models_dir, voices[voice_choice - 1])) as data:
                    self.current_voice_model_name = voices[voice_choice - 1].replace('.npz', '')
                    self.current_voice_model = {
                         'semantic_prompt': data['semantic_prompt'],
                         'coarse_prompt': data['coarse_prompt'],
                         'fine_prompt': data['fine_prompt']
                    }
               
               self.present_menu(self.generate_audio_menu)
     

     def continue_with_current_voice_model(self):
          if self.current_voice_model is None:
               print('\nNo voice model loaded.')
               self.present_menu(self.main_menu)
               return
          else:
               self.present_menu(self.generate_audio_menu)


     def prompt_for_built_in_voice_models(self):
          print('\nEnter a voice preset or leave blank for default voice (default is v2/en_speaker_2)')

          sorted_prompts = sorted(generation.ALLOWED_PROMPTS)

          for i in range(len(sorted_prompts)):
               print(str(i + 1) + ': ' + sorted_prompts[i])
          
          print(str(len(sorted_prompts) + 1) + ': Back')

          choice = input('Enter your choice: ')

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
               print(f'\nInvalid choice. Please enter a number between 1 and {len(sorted_prompts)}.')
               self.prompt_for_built_in_voice_models()
               return
          
          # user selected back, return to main menu
          if choice_int == len(sorted_prompts) + 1:
               self.present_menu(self.main_menu)
               return
          # show error if they entered a number that is not in the menu
          elif choice_int < 1 or choice_int > len(sorted_prompts):
               print(f'\nInvalid choice. Please enter a number between 1 and {len(sorted_prompts)}.')
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

          print('\nEnter text to convert to speech')
          print('Notes:')
          print('  - To indicate the end of input, press ctrl+z then press enter (must be on a blank line)')
          print('  - To start over press ctrl+r at any point. Then indicate the end of input by pressing ctrl+z on a blank line.')
          print('  - To cancel and return to the main menu press ctrl+x at any point. Then indicate the end of input by pressing ctrl+z on a blank line.')
          print('---------')

          text_prompt = ''.join(sys.stdin.readlines()).replace('\n', ' ')

          # ctrl+r
          if '\x12' in text_prompt:
               return
          # ctrl+x
          elif '\x18' in text_prompt or text_prompt == '':
               self.present_menu(self.generate_audio_menu)
               return
          
          filename = self.prompt_for_filename()
          print('Generating voice model and audio file...')

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
               write_wav(os.path.join(self.generated_output_dir, filename), SAMPLE_RATE, audio)
               print('File written to \'' + self.generated_output_dir + '/' + filename + '\'\n\n')
          except ValueError as e:
               print('Error: ' + str(e) + '\n')
               self.current_voice_model = None
               self.current_voice_model_name = None
               return
          
          self.present_menu(self.generate_audio_menu)
     

     def prompt_for_filename(self):
          filename = input('\nEnter a filename for the audio (or ctrl+x to cancel): ')

          # ctrl+x
          if filename == '\x18':
               self.present_menu(self.main_menu)
               return

          return filename + '.wav'


def main():
     generator = VoiceGenerator()
     generator.cls()
     print('Loading voice models...')

     # download and load all models
     preload_models()
     generator.cls()
     print('Welcome to the Wakeful Games text to speech generator!\n')

     while(True):
          generator.present_menu(generator.main_menu)


if __name__ == "__main__":
     main()
