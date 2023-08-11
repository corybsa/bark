from typing import Union
import dearpygui.dearpygui as dpg
import random


class BaseWindow:
  tag = 'base_window'


  def get_random_tag(self):
    return f'{self.tag}_{random.randint(0, 1000000)}'


  def show(self):
    dpg.configure_item(self.tag, show=True)


  def open_modal(self, message: str, tag: str = None, no_close = True, height: Union[int, str] = 'auto', width: Union[int, str] = 'auto'):
    if tag is None:
      tag = self.get_random_tag()
    
    width_padding = 7

    if height == 'auto':
      height = (len(message.split('\n')) * 8)
      height = 98 if height < 98 else height

    if width == 'auto':
      longest_message = max(message.split('\n'), key=len)
      width = (len(longest_message) * 7) + width_padding * 2
    
    y = (dpg.get_viewport_height() / 2) - (height / 2) - 20
    x = (dpg.get_viewport_width() / 2) - (width / 2) - width_padding

    with dpg.window(
      label=' ',
      tag=tag,
      show=True,
      modal=True,
      no_close=no_close,
      no_collapse=True,
      no_resize=True,
      no_move=True,
      no_title_bar=no_close,
      pos=[x, y],
      width=width,
      height=height,
      on_close=lambda: dpg.delete_item(tag)
    ):
      dpg.add_text(message, tag=f'{tag}_text')

