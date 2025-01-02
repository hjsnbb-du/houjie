"""Notification utilities for the application."""
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.utils import get_color_from_hex

def show_message(text: str, duration: float = 2.0):
    """Show a notification message.
    
    Args:
        text: The message to display
        duration: How long to show the message in seconds
    """
    content = Label(
        text=text,
        color=(1, 1, 1, 1),
        text_size=(400, None),
        size_hint_y=None,
        halign='center',
        valign='middle'
    )
    content.bind(texture_size=content.setter('size'))
    
    popup = Popup(
        title='',
        content=content,
        size_hint=(None, None),
        size=(450, 100),
        background_color=get_color_from_hex('#333333'),
        background='',
        border=(0, 0, 0, 0)
    )
    
    # Position at bottom of screen
    popup.pos_hint = {'center_x': 0.5, 'y': 0.1}
    popup.open()
    
    # Auto dismiss after duration
    Clock.schedule_once(lambda dt: popup.dismiss(), duration)
