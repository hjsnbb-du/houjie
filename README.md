# OpenAI Chat Application

An elegant OpenAI API chat application built with Python's Kivy framework.

## Features

- Configure OpenAI API settings
- Chat history management
- Real-time chat interface
- Elegant Material Design UI

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python src/main.py
```

## Configuration

Before using the application, you need to configure your OpenAI API key in the settings screen.

## Development

The project follows a modular architecture with the following structure:

```
src/
├── main.py          # Application entry point
├── views/           # Kivy view definitions
├── models/          # Data models
└── controllers/     # Business logic
```

## License

MIT License
