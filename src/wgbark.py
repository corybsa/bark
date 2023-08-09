from bark import SAMPLE_RATE, generate_audio, preload_models, save_as_prompt, generation
from scipy.io.wavfile import write as write_wav
import numpy as np
import sys
import os
from pathlib import Path
from colorama import Fore, Style
from threading import Thread


class VoiceGenerator:
  def __init__(self):
    self.current_voice_model = None
    self.current_voice_model_name = None
    self.text_temp = 0.7
    self.waveform_temp = 0.7
    self.is_using_built_in_model = True
    self.bark_dir = os.path.dirname(sys.argv[0])
    self.voice_models_dir = os.path.join(self.bark_dir, 'voice_models')
    self.generated_output_dir = os.path.join(self.bark_dir, 'output')
    self.save_as_name = 'custom voice model'

    Path(self.voice_models_dir).mkdir(exist_ok=True)
    Path(self.generated_output_dir).mkdir(exist_ok=True)


  def preload_models(self, callback=None):
    callback()
    # Thread(target=self.preload_models_thread, args=(callback,)).start()


  def preload_models_thread(self, callback=None):
    preload_models()
  
    if(callback):
      callback()


  def set_text_temp(self, value):
    self.text_temp = value
   

  def set_waveform_temp(self, value):
     self.waveform_temp = value


  def set_voice_model(self, voice_model_name: str):
    # if voice_model_name ends with .npz, it's a custom voice model
    if(voice_model_name.endswith('.npz')):
      self.current_voice_model = os.path.join(self.voice_models_dir, voice_model_name)
      self.is_using_built_in_model = False

      with np.load(os.path.join(self.voice_models_dir, voice_model_name)) as data:
        self.current_voice_model_name = voice_model_name.replace('.npz', '')
        self.current_voice_model = {
          'semantic_prompt': data['semantic_prompt'],
          'coarse_prompt': data['coarse_prompt'],
          'fine_prompt': data['fine_prompt']
        }
    else:
      self.current_voice_model_name = voice_model_name
      self.is_using_built_in_model = True


  def get_voice_model(self):
    if self.is_using_built_in_model:
      return self.current_voice_model_name
    else:
      return self.current_voice_model
   

  def save_voice_model(self):
    if self.is_using_built_in_model:
      filepath = os.path.join(self.voice_models_dir, self.current_voice_model_name)
      built_in_model = os.path.join(generation.CUR_PATH, 'assets', 'prompts', 'v2' if 'v2' in self.current_voice_model_name else '', self.current_voice_model_name + '.npz')

      with np.load(built_in_model) as data:
        self.current_voice_model = {
          'semantic_prompt': data['semantic_prompt'],
          'coarse_prompt': data['coarse_prompt'],
          'fine_prompt': data['fine_prompt']
        }

      save_as_prompt(filepath, self.current_voice_model)
      
      self.is_using_built_in_model = False
    else:
      filepath = os.path.join(self.voice_models_dir, self.current_voice_model_name + '.npz')
      save_as_prompt(filepath, self.current_voice_model)


  def get_all_voice_models(self):
    voices = [f for f in os.listdir(self.voice_models_dir) if os.path.isfile(os.path.join(self.voice_models_dir, f)) and f.endswith('.npz')]
    voices += list(sorted(generation.ALLOWED_PROMPTS))
    return voices


  def generate_voice_model(self, text_prompt: str, save_audio=False, callback=None):
    try:
      (model, audio) = generate_audio(
        text_prompt,
        history_prompt=self.current_voice_model,
        text_temp=self.text_temp,
        waveform_temp=self.waveform_temp,
        silent=True,
        output_full=True
      )
      
      self.current_voice_model = model

      # save audio to disk
      if save_audio:
        filename = self.current_voice_model_name + '.wav'
        filepath = os.path.join(self.generated_output_dir, filename)
        write_wav(filepath, SAMPLE_RATE, audio)
    except ValueError as e:
      # self.print('\nError: ' + str(e) + '\n', Fore.RED)
      self.current_voice_model = None
      self.current_voice_model_name = None
      return
    finally:
      if callback is not None:
        callback()