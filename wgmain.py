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
          self.voice_models_path = 'voice_models'
          self.generated_output_path = 'output'

          self.main_menu_items = {
               'Load a voice model': self.load_voice_model,
               'Create a new voice model': self.prompt_for_text_to_speech,
               'List built-in voice models': self.list_built_in_voice_models,
               'Exit': exit
          }

          self.prompt_menu_items = {
               'Generate audio file': self.prompt_for_text_to_speech,
               'Save voice model': self.save_voice_model,
               'Back': lambda : self.present_menu(self.main_menu_items)
          }

          Path('./' + self.voice_models_path).mkdir(exist_ok=True)
          Path('./' + self.generated_output_path).mkdir(exist_ok=True)


     def cls(self):
          os.system('cls' if os.name=='nt' else 'clear')
     

     def present_menu(self, menu_items):
          print('\nChoose an option to continue:')

          # display menu items
          items = list(menu_items.items())
          for i in range(len(items)):
               print(str(i + 1) + ': ' + items[i][0])

          # get user input and show error if they did not enter a number
          try:
               choice = int(input('Enter your choice: '))
          except:
               print('Invalid choice. Please try again.\n')
               self.present_menu(menu_items)
               return

          # show error if they entered a number that is not in the menu
          if choice < 1 or choice > len(menu_items):
               print('Invalid choice. Please try again.\n')
               self.present_menu(menu_items)
               return

          # call the function associated with the menu item
          items[choice - 1][1]()
     

     def list_built_in_voice_models(self, menu_items):
          sorted_prompts = sorted(generation.ALLOWED_PROMPTS)

          for item in sorted_prompts:
               print(item)
          
          self.present_menu(menu_items)
     

     def save_voice_model(self):
          should_save_voice_model = input('\nDo you want to save this voice model (y/n)? ') == 'y'

          if should_save_voice_model:
               model_name = input('Enter a name for the model: ')
               model_name += '.npz'
               
               save_as_prompt(os.path.join(self.voice_models_path, model_name), self.current_voice_model)
               print('Voice model saved to \'' + self.voice_models_path + '/' + model_name + '\'')


     def load_voice_model(self):
          # get saved voice models from the voice_models folder
          voices = [f for f in os.listdir(self.voice_models_path) if os.path.isfile(os.path.join(self.voice_models_path, f)) and f.endswith('.npz')]
          
          if len(voices) == 0:
               print('\nNo voice models found in ./' + self.voice_models_path + '.\n')
               self.present_menu(self.main_menu_items)
          else:
               print('\nSelect a voice model to load:')
               for i in range(len(voices)):
                    print(str(i + 1) + ': ' + voices[i])
               
               print(str(len(voices) + 1) + ': Back')

               try:
                    voice_choice = int(input('Enter your choice: '))
               except:
                    print('Invalid choice. Please try again.')
                    self.load_voice_model()
                    return
               
               # user selected back, return to main menu
               if voice_choice == len(voices) + 1:
                    self.present_menu(self.main_menu_items)
                    return
               # show error if they entered a number that is not in the menu
               elif voice_choice < 1 or voice_choice > len(voices):
                    print('Invalid choice. Please try again.')
                    self.load_voice_model()
                    return
                    
               with np.load(os.path.join(self.voice_models_path, voices[voice_choice - 1])) as data:
                    self.current_voice_model_name = voices[voice_choice - 1].replace('.npz', '')
                    self.current_voice_model = {
                         'semantic_prompt': data['semantic_prompt'],
                         'coarse_prompt': data['coarse_prompt'],
                         'fine_prompt': data['fine_prompt']
                    }
                    
               self.prompt_for_text_to_speech()


     def prompt_for_text_to_speech(self):
          if self.current_voice_model is None:
               print('\nEnter a voice preset or press just enter for default voice (default is v2/en_speaker_2)')
               print('This voice will be used as a seed. On subsequent runs during this session, the model will grow.')
               print('You can find voice presets here. Use the value in the \'Prompt Name\' column')
               self.current_voice_model = input('https://suno-ai.notion.site/8b8e8749ed514b0cbf3f699013548683?v=bc67cff786b04b50b3ceb756fd05f68c\n')

               if self.current_voice_model == '':
                    self.current_voice_model = 'v2/en_speaker_2'

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
               self.save_voice_model()
               self.present_menu(self.prompt_menu_items)
               return
          
          filename = self.prompt_for_filename()
          print('Generating audio file...')
          (model, audio) = generate_audio(text_prompt, history_prompt=self.current_voice_model, output_full=True)
          self.current_voice_model = model

          # save audio to disk
          write_wav(os.path.join(self.generated_output_path, filename), SAMPLE_RATE, audio)
          print('File written to \'' + self.generated_output_path + '/' + filename + '\'\n\n')
     

     def prompt_for_filename(self):
          filename = input('\nEnter a filename for the audio (or ctrl+x to return to main menu): ')

          # ctrl+x
          if filename == '\x18':
               if self.current_voice_model is not None:
                    self.save_voice_model()

               self.present_menu(self.main_menu_items)
               return

          return filename + '.wav'


def main():
     generator = VoiceGenerator()
     generator.cls()
     print('Loading voice models...\n')

     # download and load all models
     preload_models()
     generator.cls()
     print('Welcome to the Wakeful Games text to speech generator!\n')
     generator.present_menu(generator.main_menu_items)

     while(True):
          generator.prompt_for_text_to_speech()


main()
