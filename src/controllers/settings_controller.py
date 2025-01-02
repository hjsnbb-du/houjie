"""Settings controller for managing application configuration."""
from pathlib import Path
import json
from typing import Dict, Optional

from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar

from services.openai_service import OpenAIService

class SettingsController(MDScreen):
    """Controller for the settings screen."""
    
    api_service: OpenAIService = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        """Initialize the settings controller."""
        super().__init__(**kwargs)
        self.api_service = OpenAIService()
        Clock.schedule_once(self._load_settings)
    
    def _load_settings(self, *args):
        """Load settings from config file."""
        config = self._read_config()
        if config:
            self.ids.api_key.text = config.get('api_key', '')
            self.ids.base_url.text = config.get('base_url', 'https://api.openai.com/v1')
            self.ids.model_spinner.text = config.get('model', 'gpt-3.5-turbo')
    
    def save_settings(self):
        """Save settings to config file."""
        config = {
            'api_key': self.ids.api_key.text,
            'base_url': self.ids.base_url.text,
            'model': self.ids.model_spinner.text
        }
        
        try:
            self.api_service.save_config(
                api_key=config['api_key'],
                base_url=config['base_url']
            )
            self._write_config(config)
            Snackbar(text="Settings saved successfully").open()
            self.manager.current = 'history'
        except Exception as e:
            Snackbar(text=f"Error saving settings: {str(e)}").open()
    
    def test_connection(self):
        """Test the OpenAI API connection."""
        try:
            self.api_service.save_config(
                api_key=self.ids.api_key.text,
                base_url=self.ids.base_url.text
            )
            if self.api_service.test_connection():
                Snackbar(text="Connection successful!").open()
            else:
                Snackbar(text="Connection failed. Please check your settings.").open()
        except Exception as e:
            Snackbar(text=f"Connection error: {str(e)}").open()
    
    def cancel(self):
        """Cancel settings changes and return to previous screen."""
        self.manager.current = 'history'
    
    def _read_config(self) -> Optional[Dict]:
        """Read configuration from file."""
        config_path = Path.home() / '.openai_chat_config.json'
        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        return None
    
    def _write_config(self, config: Dict):
        """Write configuration to file."""
        config_path = Path.home() / '.openai_chat_config.json'
        with open(config_path, 'w') as f:
            json.dump(config, f)
