from bark import SAMPLE_RATE, generate_audio, preload_models, save_as_prompt, generation
from bark.api import semantic_to_waveform
from scipy.io.wavfile import write as write_wav
import numpy as np
import sys
import os
from pathlib import Path
from threading import Thread
import nltk
nltk.download('punkt')


class VoiceGenerator:
  def __init__(self):
    self.current_voice_model = None
    self.current_voice_model_name = None
    self.temp_voice_model = None
    self.is_voice_model_updated = False

    self.text_temp = 0.7
    self.waveform_temp = 0.7
    self.long_text_threshold = 150
    
    self.bark_dir = os.path.dirname(sys.argv[0])
    self.voice_models_dir = os.path.join(self.bark_dir, 'voice_models')
    self.generated_output_dir = os.path.join(self.bark_dir, 'output')
    self.temp_dir = os.path.join(self.bark_dir, '.tmp')

    self.save_as_name = 'custom voice model'
    self.generated_audio_data = None

    self.speech_generation_callbacks = []
    self.speech_model_set_callbacks = []

    Path(self.voice_models_dir).mkdir(exist_ok=True)
    Path(self.generated_output_dir).mkdir(exist_ok=True)
    Path(self.temp_dir).mkdir(exist_ok=True)
  

  def __del__(self):
    # delete temp files
    for f in os.listdir(self.temp_dir):
      os.remove(os.path.join(self.temp_dir, f))


  def preload_models(self, callback):
    Thread(target=self.preload_models_thread, args=(callback,)).start()


  def preload_models_thread(self, callback):
    preload_models()
    callback()


  def get_built_in_voice_models_dir(self):
    return os.path.join(generation.CUR_PATH, 'assets', 'prompts')


  def get_all_voice_models(self):
    voices = [f for f in os.listdir(self.voice_models_dir) if os.path.isfile(os.path.join(self.voice_models_dir, f)) and f.endswith('.npz')]
    voices += list(sorted(generation.ALLOWED_PROMPTS))
    return voices


  def set_voice_model(self, voice_model_name: str):
    # if voice_model_name ends with .npz, it's a custom voice model
    if(voice_model_name.endswith('.npz')):
      self.current_voice_model = os.path.join(self.voice_models_dir, voice_model_name)

      # load custom voice model
      with np.load(os.path.join(self.voice_models_dir, voice_model_name)) as data:
        self.current_voice_model_name = voice_model_name.replace('.npz', '')
        self.current_voice_model = {
          'semantic_prompt': data['semantic_prompt'],
          'coarse_prompt': data['coarse_prompt'],
          'fine_prompt': data['fine_prompt']
        }

      self.current_voice_model_name = voice_model_name.replace('.npz', '')
    else:
      built_in_model = os.path.join(generation.CUR_PATH, 'assets', 'prompts', voice_model_name + '.npz')

      # load built-in voice model
      with np.load(built_in_model) as data:
        self.current_voice_model = {
          'semantic_prompt': data['semantic_prompt'],
          'coarse_prompt': data['coarse_prompt'],
          'fine_prompt': data['fine_prompt']
        }
      
      self.current_voice_model_name = voice_model_name
    
    self.temp_voice_model = None
    self.is_voice_model_updated = False
    self.dispatch_speech_model_set_callbacks()
  

  def update_current_voice_model_with_temp(self):
    if self.temp_voice_model is not None:
      self.current_voice_model = self.temp_voice_model
      self.is_voice_model_updated = True
      self.dispatch_speech_model_set_callbacks()
  

  def dispatch_speech_model_set_callbacks(self):
    for c in self.speech_model_set_callbacks:
      c()
  

  def dispatch_speech_generation_callbacks(self):
    for c in self.speech_generation_callbacks:
      c()
  

  def set_text_temp(self, value: float):
    self.text_temp = value
   

  def set_waveform_temp(self, value: float):
    self.waveform_temp = value


  def get_temp_audio_file(self):
    return os.path.join(self.temp_dir, 'generated.wav')


  def add_speech_generation_callback(self, callback):
    self.speech_generation_callbacks.append(callback)
  

  def add_speech_model_set_callback(self, callback):
    self.speech_model_set_callbacks.append(callback)


  def save_voice_model(self, filename: str):
    filename = filename.replace('/', '_').replace('\\', '_') + '.npz'
    filepath = os.path.join(self.voice_models_dir, filename)
    save_as_prompt(filepath, self.current_voice_model)
    self.set_voice_model(filename)
    self.is_voice_model_updated = False
    return os.path.abspath(filepath)


  def generate_speech(self, text_prompt: str, should_learn=False, callback=None):
    if len(text_prompt) > self.long_text_threshold:
      self.generate_long_speech(text_prompt, should_learn, callback)
      return

    (model, audio) = generate_audio(
      text_prompt,
      history_prompt=self.current_voice_model,
      text_temp=self.text_temp,
      waveform_temp=self.waveform_temp,
      output_full=True
    )

    self.generated_audio_data = audio

    if should_learn:
      self.current_voice_model = model
      self.is_voice_model_updated = True
    else:
      self.temp_voice_model = model

    filepath = os.path.join(self.temp_dir, 'generated.wav')
    write_wav(filepath, SAMPLE_RATE, self.float2pcm(self.generated_audio_data))

    callback()

    self.dispatch_speech_generation_callbacks()


  def generate_long_speech(self, text_prompt: str, should_learn=False, callback=None):
    sentences = nltk.sent_tokenize(text_prompt.replace('\n', ' ').strip())
    silence = np.zeros(int(0.25 * SAMPLE_RATE)) # quarter second of silence
    pieces = []

    for sentence in sentences:
      semantic_tokens = generation.generate_text_semantic(
        sentence,
        history_prompt=self.current_voice_model,
        temp=self.text_temp,
        min_eos_p=0.05 # this controls how likely the generation is to end
      )

      (model, audio) = semantic_to_waveform(semantic_tokens, history_prompt=self.current_voice_model, output_full=True)
      pieces += [audio, silence.copy()]

      if should_learn:
        self.current_voice_model = model
        self.is_voice_model_updated = True
      else:
        self.temp_voice_model = model
    
    self.generated_audio_data = np.concatenate(pieces)

    filepath = os.path.join(self.temp_dir, 'generated.wav')
    write_wav(filepath, SAMPLE_RATE, self.float2pcm(self.generated_audio_data))

    callback()

    self.dispatch_speech_generation_callbacks()
  

  def float2pcm(self, sig, dtype='int16'):
    sig = np.asarray(sig)
    dtype = np.dtype(dtype)
    i = np.iinfo(dtype)
    abs_max = 2 ** (i.bits - 1)
    offset = i.min + abs_max
    return (sig * abs_max + offset).clip(i.min, i.max).astype(dtype)

