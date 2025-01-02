#!/usr/bin/env python3
"""
OpenAI Chat Application
Main entry point for the Kivy-based OpenAI chat application.
"""
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

# Set window size and make it resizable
Config.set('graphics', 'minimum_width', '800')
Config.set('graphics', 'minimum_height', '600')
Window.size = (1024, 768)

class ChatApp(App):
    """Main application class."""
    
    def build(self):
        """Initialize and return the root widget."""
        # Load all kv files
        Builder.load_file('views/settings.kv')
        Builder.load_file('views/history.kv')
        Builder.load_file('views/chat.kv')
        
        # Create screen manager
        sm = ScreenManager(transition=SlideTransition())
        
        # Add screens
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(HistoryScreen(name='history'))
        sm.add_widget(ChatScreen(name='chat'))
        
        return sm

class SettingsScreen(Screen):
    """Settings screen for API configuration."""
    pass

class HistoryScreen(Screen):
    """History screen showing chat history."""
    pass

class ChatScreen(Screen):
    """Main chat interface screen."""
    pass

if __name__ == '__main__':
    ChatApp().run()
