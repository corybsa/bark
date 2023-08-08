import dearpygui.dearpygui as dpg


with dpg.window(label="Example Window", autosize=True):
  dpg.add_text("Hello, world")
  
  dpg.add_slider_float(
    label="Text temperature",
    default_value=0.7,
    min_value=0.0,
    max_value=1.0,
    clamped=True
  )

  dpg.add_slider_float(
    label="Waveform temperature",
    default_value=0.7,
    min_value=0.0,
    max_value=1.0,
    clamped=True
  )
