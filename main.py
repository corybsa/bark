from bark import SAMPLE_RATE, generate_audio, preload_models, save_as_prompt
from scipy.io.wavfile import write as write_wav
import numpy as np
import sys
import os
from pathlib import Path

class VoiceGenerator:
     def __init__(self):
          self.voice_model = None
          self.voice_models_path = 'voice_models'
          self.generated_output_path = 'output'

          Path('./' + self.voice_models_path).mkdir(exist_ok=True)
          Path('./' + self.generated_output_path).mkdir(exist_ok=True)


     def cls(self):
          os.system('cls' if os.name=='nt' else 'clear')
     

     def present_menu(self):
          print('Welcome to the Wakeful Games text to speech generator!')
          print('Choose an option to continue:')
          print('1. Load a voice model')
          print('2. Create a new voice model')
          print('3. Exit')
          choice = input('Enter your choice: ')

          if choice == '1':
               self.load_voice_model()
          elif choice == '2':
               self.prompt()
          else:
               exit()

     
     def load_voice_model(self):
          voices = [f for f in os.listdir(self.voice_models_path) if os.path.isfile(os.path.join(self.voice_models_path, f))]
          
          if len(voices) == 0:
               print('\nNo voice models found in ./' + self.voice_models_path + '.\n\n')
               self.present_menu()
          else:
               print('\nSelect a voice model to load:')
               for i in range(len(voices)):
                    print(str(i + 1) + ': ' + voices[i])

               voice_choice = input('Enter your choice: ')
                    
               with np.load(os.path.join(self.voice_models_path, voices[int(voice_choice) - 1])) as data:
                    self.voice_model = {
                         'semantic_prompt': data['semantic_prompt'],
                         'coarse_prompt': data['coarse_prompt'],
                         'fine_prompt': data['fine_prompt']
                    }
               self.prompt()


     def prompt(self):
          filename = input('\nEnter a filename for the audio (or ctrl+x to exit): ')

          # ctrl+x
          if filename == '\x18':
               if self.voice_model is not None:
                    self.save_voice_model()

               exit()

          filename = filename + '.wav'

          if self.voice_model is None:
               print('\nEnter a voice preset or press just enter for default voice (default is v2/en_speaker_2)')
               print('This voice will be used as a seed. On subsequent runs during this session, the model will grow.')
               print('You can find voice presets here. Use the value in the \'Prompt Name\' column')
               self.voice_model = input('https://suno-ai.notion.site/8b8e8749ed514b0cbf3f699013548683?v=bc67cff786b04b50b3ceb756fd05f68c\n')

               if self.voice_model == '':
                    self.voice_model = 'v2/en_speaker_2'

          print('\nEnter text to convert to speech')
          print('Notes:')
          print('  - To indicate the end of input, press ctrl+z then press enter (must be on a blank line)')
          print('  - To start over press ctrl+r at any point. Then indicate the end of input by pressing ctrl+z on a blank line.')
          print('  - To exit the program press ctrl+x at any point. Then indicate the end of input by pressing ctrl+z on a blank line.')
          print('---------')

          text_prompt = ''.join(sys.stdin.readlines()).replace('\n', ' ')

          # ctrl+r
          if '\x12' in text_prompt:
               self.cls()
               return
          # ctrl+x
          elif '\x18' in text_prompt or text_prompt == '':
               self.save_voice_model()
               exit()
          
          print('Generating audio file...')
          (model, audio) = generate_audio(text_prompt, history_prompt=self.voice_model, output_full=True)
          self.voice_model = model

          # save audio to disk
          write_wav(self.generated_output_path + '/' + filename, SAMPLE_RATE, audio)
          print('File written to \'' + self.generated_output_path + '/' + filename + '\'\n\n')
     

     def save_voice_model(self):
          should_save_voice_model = input('Do you want to save this voice model (y/n)? ') == 'y'

          if should_save_voice_model:
               model_name = input('Enter a name for the model: ')
               save_as_prompt(self.voice_models_path + '/' + model_name + '.npz', self.voice_model)
               print('Voice model saved to \'' + self.voice_models_path + '/' + model_name + '.npz\'')


generator = VoiceGenerator()
generator.cls()
print('Loading voice models...\n')

# download and load all models
preload_models()
generator.present_menu()

while(True):
     generator.prompt()
