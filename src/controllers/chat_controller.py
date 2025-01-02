"""Chat controller for managing conversations."""
from datetime import datetime
from typing import Optional

from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar

from models.chat import Conversation, Message
from services.openai_service import OpenAIService

class ChatController(MDScreen):
    """Controller for the chat screen."""
    
    api_service: OpenAIService = ObjectProperty(None)
    current_conversation: Optional[Conversation] = None
    
    def __init__(self, **kwargs):
        """Initialize the chat controller."""
        super().__init__(**kwargs)
        self.api_service = OpenAIService()
    
    def set_conversation(self, conversation: Conversation):
        """Set the current conversation and load messages."""
        self.current_conversation = conversation
        self._load_messages()
    
    def _load_messages(self):
        """Load messages into the chat view."""
        message_list = self.ids.message_list
        message_list.clear_widgets()
        
        if not self.current_conversation:
            return
        
        for message in self.current_conversation.messages:
            self._add_message_bubble(message)
    
    def _add_message_bubble(self, message: Message):
        """Add a message bubble to the chat view."""
        from kivymd.uix.card import MDCard
        
        bubble = MDCard(
            message=message.content,
            timestamp=message.timestamp.strftime("%H:%M"),
            size_hint_x=0.8,
            pos_hint={'right': 1} if message.role == 'user' else {'x': 0},
            md_bg_color=(0.9, 0.9, 1, 1) if message.role == 'user' else (1, 1, 1, 1)
        )
        self.ids.message_list.add_widget(bubble)
        Clock.schedule_once(lambda dt: self._scroll_to_bottom())
    
    async def send_message(self):
        """Send a message and get response from OpenAI."""
        if not self.current_conversation:
            Snackbar(text="No active conversation").open()
            return
        
        message_text = self.ids.message_input.text.strip()
        if not message_text:
            return
        
        self.ids.message_input.text = ""
        user_message = self.current_conversation.add_message(message_text, 'user')
        self._add_message_bubble(user_message)
        
        try:
            messages = [
                {"role": msg.role, "content": msg.content}
                for msg in self.current_conversation.messages
            ]
            
            response = await self.api_service.send_message(
                messages,
                self.current_conversation.model
            )
            
            assistant_message = self.current_conversation.add_message(
                response,
                'assistant'
            )
            self._add_message_bubble(assistant_message)
        except Exception as e:
            Snackbar(text=f"Error: {str(e)}").open()
    
    def _scroll_to_bottom(self):
        """Scroll the chat view to the bottom."""
        chat_scroll = self.ids.chat_scroll
        chat_scroll.scroll_y = 0
    
    def go_back(self):
        """Return to the history screen."""
        self.manager.current = 'history'
    
    def show_settings(self):
        """Show the settings screen."""
        self.manager.current = 'settings'
