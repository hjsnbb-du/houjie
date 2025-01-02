"""History controller for managing chat history."""
import json
from pathlib import Path
from typing import List, Optional

from kivy.properties import ObjectProperty
from kivy.uix.screen import Screen

from models.chat import Conversation
from services.openai_service import OpenAIService

class HistoryController(Screen):
    """Controller for the history screen."""
    
    api_service: OpenAIService = ObjectProperty(None)
    conversations: List[Conversation] = []
    
    def __init__(self, **kwargs):
        """Initialize the history controller."""
        super().__init__(**kwargs)
        self.api_service = OpenAIService()
        self._load_conversations()
    
    def _load_conversations(self):
        """Load conversations from storage."""
        conversations = self._read_conversations()
        self.conversations = conversations or []
        self._update_conversation_list()
    
    def _update_conversation_list(self):
        """Update the conversation list in the UI."""
        conversation_list = self.ids.conversation_list
        conversation_list.clear_widgets()
        
        for conv in sorted(
            self.conversations,
            key=lambda x: x.updated_at,
            reverse=True
        ):
            self._add_conversation_item(conv)
    
    def _add_conversation_item(self, conversation: Conversation):
        """Add a conversation item to the list."""
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.behaviors import ButtonBehavior
        
        class ConversationItem(ButtonBehavior, BoxLayout):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.orientation = 'vertical'
                self.size_hint_y = None
                self.height = '72dp'
                self.padding = '12dp'
                self.spacing = '4dp'
        
        item = ConversationItem(
            title=conversation.title,
            preview=conversation.preview,
            timestamp=conversation.updated_at.strftime("%Y-%m-%d %H:%M")
        )
        item.bind(on_release=lambda x: self._open_conversation(conversation))
        self.ids.conversation_list.add_widget(item)
    
    def new_chat(self):
        """Create a new conversation and open it."""
        conversation = Conversation(
            title=f"New Chat {len(self.conversations) + 1}"
        )
        self.conversations.append(conversation)
        self._save_conversations()
        self._open_conversation(conversation)
    
    def _open_conversation(self, conversation: Conversation):
        """Open a conversation in the chat screen."""
        chat_screen = self.manager.get_screen('chat')
        chat_screen.set_conversation(conversation)
        self.manager.current = 'chat'
    
    def _read_conversations(self) -> Optional[List[Conversation]]:
        """Read conversations from storage."""
        storage_path = Path.home() / '.openai_chat_history.json'
        if not storage_path.exists():
            return None
        
        with open(storage_path, 'r') as f:
            data = json.load(f)
            return [Conversation(**conv) for conv in data]
    
    def _save_conversations(self):
        """Save conversations to storage."""
        storage_path = Path.home() / '.openai_chat_history.json'
        with open(storage_path, 'w') as f:
            json.dump([conv.__dict__ for conv in self.conversations], f)
