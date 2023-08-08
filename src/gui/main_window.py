import dearpygui.dearpygui as dpg
from wgbark import VoiceGenerator


class MainWindow:
  def __init__(self):
    dpg.create_context()
    dpg.create_viewport()
    dpg.setup_dearpygui()

    with dpg.window(label="Loading...", autosize=True) as loading_window:
      dpg.add_text("Loading voice models...")
      dpg.set_primary_window(loading_window, True)

      # dpg.add_slider_float(
      #   label="Text temperature",
      #   default_value=0.7,
      #   min_value=0.0,
      #   max_value=1.0,
      #   clamped=True
      # )

      # dpg.add_slider_float(
      #   label="Waveform temperature",
      #   default_value=0.7,
      #   min_value=0.0,
      #   max_value=1.0,
      #   clamped=True
      # )

      self.generator = VoiceGenerator()
    
    with dpg.window(label="Done!", autosize=True) as main_window:
      dpg.add_text("Hello, world")
      dpg.set_primary_window(main_window, True)

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

