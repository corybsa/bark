import dearpygui.dearpygui as dpg


if __name__ == '__main__':
  dpg.create_context()
  dpg.create_viewport(title='Wakeful Games Text to Speech Generator')
  dpg.setup_dearpygui()

  with dpg.window(label='Wakeful Games', tag='main_window', show=True):
    dpg.set_primary_window('main_window', True)

    with dpg.window(label='settings', tag='settings_window', show=True):
      dpg.add_slider_float(
        label='Text temperature',
        default_value=0.7,
        min_value=0.0,
        max_value=1.0,
        clamped=True
      )

    dpg.add_button(label='Click me', callback=lambda: dpg.delete_item('settings_window'))

  dpg.show_viewport()
  dpg.start_dearpygui()
  dpg.destroy_context()
