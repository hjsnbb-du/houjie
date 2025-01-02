# UI Design Specification

## Overview
This document details the UI design for the OpenAI Chat Application, following Kivy's Material Design principles for an elegant and intuitive user experience.

## Color Palette
- Primary: #2196F3 (Blue)
- Secondary: #FFC107 (Amber)
- Background: #FFFFFF (White)
- Surface: #F5F5F5 (Light Grey)
- Error: #F44336 (Red)
- Text Primary: #212121 (Dark Grey)
- Text Secondary: #757575 (Medium Grey)

## Typography
- Primary Font: Roboto
- Monospace Font: Roboto Mono (for code blocks)
- Font Sizes:
  - Heading 1: 24sp
  - Heading 2: 20sp
  - Body: 16sp
  - Caption: 14sp

## Layout Specifications

### 1. Configuration Screen (settings.kv)
```
[Window]
├── AppBar
│   └── Title: "Settings"
├── ScrollView
│   └── StackLayout
│       ├── APIKeySection
│       │   ├── Label: "OpenAI API Key"
│       │   └── SecureTextInput
│       ├── BaseURLSection
│       │   ├── Label: "API Base URL"
│       │   └── TextInput: "https://api.openai.com/v1"
│       ├── ModelSection
│       │   ├── Label: "Model"
│       │   └── Spinner: ["gpt-3.5-turbo", "gpt-4"]
│       └── AdvancedSection
│           ├── Label: "Advanced Settings"
│           ├── Slider: "Temperature (0-2)"
│           └── Slider: "Max Tokens"
└── ButtonBar
    ├── Button: "Test Connection"
    ├── Button: "Save"
    └── Button: "Cancel"
```

### 2. Chat History Screen (history.kv)
```
[Window]
├── AppBar
│   ├── Title: "Conversations"
│   └── SearchBar
├── ScrollView
│   └── ConversationList
│       └── ConversationItem (repeated)
│           ├── Title
│           ├── Preview
│           ├── Timestamp
│           └── ModelBadge
└── FloatingActionButton: "New Chat"
```

### 3. Chat Interface Screen (chat.kv)
```
[Window]
├── AppBar
│   ├── BackButton
│   ├── Title: "Chat"
│   └── SettingsButton
├── ChatArea
│   └── ScrollView
│       └── MessageList
│           └── Message (repeated)
│               ├── Avatar
│               ├── Content
│               │   ├── Text/Markdown
│               │   └── CodeBlock (if applicable)
│               └── Timestamp
└── InputArea
    ├── TextInput: "Type your message..."
    └── SendButton
```

## Component Details

### Messages
- User Messages:
  - Right-aligned
  - Blue background (#E3F2FD)
  - Round corners (12dp)
  - Max width: 75% of screen

- Assistant Messages:
  - Left-aligned
  - White background
  - Light border
  - Round corners (12dp)
  - Max width: 75% of screen

### Buttons
- Primary Button:
  - Height: 48dp
  - Padding: 16dp horizontal
  - Round corners (4dp)
  - Elevation: 2dp
  - Ripple effect on press

### Input Fields
- Height: 56dp
- Padding: 16dp
- Underline indicator
- Floating labels
- Error states with red underline

### Lists
- Item Height: 72dp
- Divider: 1dp light grey line
- Padding: 16dp horizontal
- Ripple effect on press

## Animations
- Screen Transitions: Slide animation (300ms)
- Button Press: Ripple effect (200ms)
- Message Appear: Fade in (150ms)
- Loading Indicator: Circular progress
- Error Notifications: Slide down (250ms)

## Responsive Design
- Minimum window width: 320dp
- Maximum message width: 75% of container
- Flexible layout adjustments:
  - Single column layout (width < 600dp)
  - Two column layout (width >= 600dp)

## Accessibility
- Minimum touch target size: 48x48dp
- High contrast text colors
- Screen reader support
- Keyboard navigation support

## Error States
- Input validation feedback
- Network error notifications
- API error handling
- Loading states

## Implementation Notes
All UI components will be implemented using Kivy's built-in widgets and custom widgets where necessary. The design follows Material Design principles while maintaining Kivy's native look and feel.
