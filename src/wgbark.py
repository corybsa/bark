from bark import SAMPLE_RATE, generate_audio, preload_models, save_as_prompt, generation
from scipy.io.wavfile import write as write_wav
import numpy as np
import sys
import os
from pathlib import Path
from threading import Thread


class VoiceGenerator:
  def __init__(self):
    self.is_using_built_in_model = True
    self.current_voice_model = None
    self.current_voice_model_name = None

    self.text_temp = 0.7
    self.waveform_temp = 0.7
    
    self.bark_dir = os.path.dirname(sys.argv[0])
    self.voice_models_dir = os.path.join(self.bark_dir, 'voice_models')
    self.generated_output_dir = os.path.join(self.bark_dir, 'output')
    self.temp_dir = os.path.join(self.bark_dir, '.tmp')

    self.save_as_name = 'custom voice model'
    self.generated_audio_data = None

    Path(self.voice_models_dir).mkdir(exist_ok=True)
    Path(self.generated_output_dir).mkdir(exist_ok=True)
    Path(self.temp_dir).mkdir(exist_ok=True)
  

  def __del__(self):
    # TODO: uncomment this before release
    # delete temp files
    # for f in os.listdir(self.temp_dir):
    #   os.remove(os.path.join(self.temp_dir, f))
    pass


  def preload_models(self, callback):
    callback()
    # TODO: uncomment this before release
    # Thread(target=self.preload_models_thread, args=(callback,)).start()


  def preload_models_thread(self, callback):
    preload_models()
    callback()


  def get_all_voice_models(self):
    voices = [f for f in os.listdir(self.voice_models_dir) if os.path.isfile(os.path.join(self.voice_models_dir, f)) and f.endswith('.npz')]
    voices += list(sorted(generation.ALLOWED_PROMPTS))
    return voices


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
      
    print(f'DEBUG: Loaded voice model: {voice_model_name}')


  def get_voice_model(self):
    if self.is_using_built_in_model:
      return self.current_voice_model_name
    else:
      return self.current_voice_model
  

  def get_voice_model_name(self):
    return self.current_voice_model_name


  def set_text_temp(self, value: float):
    self.text_temp = value
   

  def set_waveform_temp(self, value: float):
    self.waveform_temp = value


  def get_audio_data(self):
    return self.generated_audio_data


  def get_temp_audio_file(self):
    return os.path.join(self.temp_dir, 'generated.wav')


  def save_voice_model(self, filename: str):
    if self.is_using_built_in_model:
      filename = filename.replace('/', '_').replace('\\', '_') + '.npz'
      filepath = os.path.join(self.voice_models_dir, filename)
      built_in_model = os.path.join(generation.CUR_PATH, 'assets', 'prompts', self.current_voice_model_name + '.npz')

      with np.load(built_in_model) as data:
        self.current_voice_model = {
          'semantic_prompt': data['semantic_prompt'],
          'coarse_prompt': data['coarse_prompt'],
          'fine_prompt': data['fine_prompt']
        }

      save_as_prompt(filepath, self.current_voice_model)
      self.set_voice_model(filename)

      return os.path.abspath(filepath)
    else:
      filename = filename.replace('/', '_').replace('\\', '_') + '.npz'
      filepath = os.path.join(self.voice_models_dir, filename)
      save_as_prompt(filepath, self.current_voice_model)
      return os.path.abspath(filepath)


  def generate_voice_model(self, text_prompt: str, callback=None):
    (model, audio) = generate_audio(
      text_prompt,
      history_prompt=self.current_voice_model_name if self.is_using_built_in_model else self.current_voice_model,
      text_temp=self.text_temp,
      waveform_temp=self.waveform_temp,
      # TODO: uncomment this before release
      # silent=True,
      output_full=True
    )

    self.generated_audio_data = audio
    self.current_voice_model = model

    filepath = os.path.join(self.temp_dir, 'generated.wav')
    write_wav(filepath, SAMPLE_RATE, self.generated_audio_data)
    # write_wav(filepath, SAMPLE_RATE, self.float2pcm(self.generated_audio_data))
    print(f'DEBUG: generated audio saved to {filepath}')

    callback()
  

  def float2pcm(self, sig, dtype='int16'):
    sig = np.asarray(sig)
    dtype = np.dtype(dtype)
    i = np.iinfo(dtype)
    abs_max = 2 ** (i.bits - 1)
    offset = i.min + abs_max
    return (sig * abs_max + offset).clip(i.min, i.max).astype(dtype)

