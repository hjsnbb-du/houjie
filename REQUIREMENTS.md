# Notebook.cv - Technical Requirements Document

## Core Features

### 1. Markdown Editor
- Text area for Markdown input/paste
- Real-time Markdown preview
- Basic editing toolbar (optional)
- Implementation: React frontend with markdown-it or similar library

### 2. Content Sharing
- Convert Markdown to HTML
- Generate unique URLs for shared content
- Anonymous access to shared content
- URL format: `username.notebook.cv/s/{unique-id}`
- Implementation: FastAPI endpoint for content storage and retrieval

### 3. User System
- Registration with username, password, email (optional)
- Secure password storage using bcrypt
- JWT-based authentication
- Automatic subdomain allocation (`username.notebook.cv`)
- User dashboard for managing notes
- Implementation: FastAPI with SQLite + SQLAlchemy

### 4. Subdomain Handling
- Nginx configuration for wildcard subdomains
- Proxy requests to FastAPI backend
- Pass username from subdomain to backend
- Implementation: Nginx reverse proxy configuration

### 5. Blog Feature
- Public listing of user's shared notes
- Accessible via user's subdomain
- Title extraction from Markdown content
- Creation timestamp and preview
- Implementation: FastAPI endpoints + React components

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Notes Table
```sql
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    content TEXT NOT NULL,
    title TEXT,
    share_id TEXT UNIQUE NOT NULL,
    is_public BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## API Endpoints

### Authentication
- POST /api/auth/register - User registration
- POST /api/auth/login - User login
- GET /api/auth/me - Get current user

### Notes
- POST /api/notes - Create new note
- GET /api/notes/{share_id} - Get shared note
- GET /api/notes/user/{username} - Get user's public notes
- PUT /api/notes/{id} - Update note
- DELETE /api/notes/{id} - Delete note

## Security Considerations
- XSS prevention in Markdown rendering
- SQL injection protection via SQLAlchemy
- CSRF protection
- Secure password hashing
- Rate limiting on authentication endpoints

## Development Phases

### Phase 1: Core Functionality
1. Set up project structure ✓
2. Implement Markdown editor
3. Implement note sharing

### Phase 2: User System
1. Implement user registration/login
2. Set up JWT authentication
3. Create user dashboard

### Phase 3: Subdomain & Blog
1. Configure Nginx
2. Implement subdomain routing
3. Create blog listing feature

## Non-functional Requirements
- Responsive design (mobile-first)
- Fast page load times
- Clean, intuitive UI
- Secure data handling
- Scalable architecture
