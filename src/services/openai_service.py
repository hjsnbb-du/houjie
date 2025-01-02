"""OpenAI API service for the chat application."""
import json
from pathlib import Path
from typing import Dict, List, Optional

import openai
from openai import OpenAI

class OpenAIService:
    """Service for interacting with OpenAI API."""
    
    def __init__(self):
        """Initialize the OpenAI service."""
        self.config_path = Path.home() / '.openai_chat_config.json'
        self.client: Optional[OpenAI] = None
        self.load_config()

    def load_config(self) -> None:
        """Load configuration from file."""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                openai.api_key = config.get('api_key')
                self.client = OpenAI(
                    api_key=config.get('api_key'),
                    base_url=config.get('base_url', "https://api.openai.com/v1")
                )

    def save_config(self, api_key: str, base_url: str) -> None:
        """Save configuration to file."""
        config = {
            'api_key': api_key,
            'base_url': base_url
        }
        with open(self.config_path, 'w') as f:
            json.dump(config, f)
        self.load_config()

    async def send_message(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-3.5-turbo"
    ) -> str:
        """Send a message to OpenAI API and get the response."""
        if not self.client:
            raise ValueError("OpenAI client not initialized. Please configure API key.")

        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True
            )
            
            full_response = ""
            async for chunk in response:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
            
            return full_response
        except Exception as e:
            raise Exception(f"Error calling OpenAI API: {str(e)}")

    def test_connection(self) -> bool:
        """Test the connection to OpenAI API."""
        if not self.client:
            return False
        
        try:
            self.client.models.list()
            return True
        except Exception:
            return False
