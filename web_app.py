#!/usr/bin/env python3
"""
Web-based Chat Room using Flask and Socket.IO
Provides a browser-based interface for the chat room
"""

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import os
import json
from datetime import datetime
from pathlib import Path

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

# Initialize Socket.IO for WebSocket communication
socketio = SocketIO(app, cors_allowed_origins="*")

# Store connected users: {session_id: username}
connected_users = {}

# Chat history file
HISTORY_FILE = 'chat_history.json'

def load_chat_history():
    """Load chat history from file"""
    if Path(HISTORY_FILE).exists():
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_chat_history(history):
    """Save chat history to file"""
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def get_user_messages(username, limit=50):
    """Get last N messages for a specific user"""
    history = load_chat_history()
    user_messages = history.get(username, [])
    return user_messages[-limit:]  # Return last 'limit' messages

def save_user_message(username, message):
    """Save a message for a specific user"""
    history = load_chat_history()
    
    if username not in history:
        history[username] = []
    
    # Add message with timestamp
    history[username].append({
        'message': message,
        'timestamp': datetime.now().isoformat()
    })
    
    # Keep only last 100 messages per user to avoid huge files
    history[username] = history[username][-100:]
    
    save_chat_history(history)

@app.route('/')
def index():
    """Serve the main chat page"""
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    """Handle new client connection"""
    print(f'Client connected: {request.sid}')

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    if request.sid in connected_users:
        username = connected_users[request.sid]
        del connected_users[request.sid]
        # Notify all users that someone left
        emit('user_left', {'username': username}, broadcast=True)
        print(f'User {username} disconnected')

@socketio.on('join')
def handle_join(data):
    """Handle user joining the chat room"""
    username = data['username']
    
    # Check if username is already taken (currently online)
    if username in connected_users.values():
        emit('join_error', {'message': 'Username already taken'})
        return
    
    # Add user to connected users
    connected_users[request.sid] = username
    
    # Load chat history for this user
    user_history = get_user_messages(username)
    
    # Notify user they successfully joined and send their history
    emit('join_success', {
        'username': username,
        'history': user_history
    })
    
    # Notify all other users that someone joined
    emit('user_joined', {'username': username}, broadcast=True, include_self=False)
    
    print(f'User {username} joined the chat (loaded {len(user_history)} messages)')

@socketio.on('send_message')
def handle_message(data):
    """Handle incoming chat message"""
    if request.sid not in connected_users:
        return
    
    username = connected_users[request.sid]
    message = data['message']
    
    # Save message to user's history
    save_user_message(username, message)
    
    # Broadcast message to all users
    emit('receive_message', {
        'username': username,
        'message': message
    }, broadcast=True)
    
    print(f'{username}: {message}')

@socketio.on('get_online_users')
def handle_get_users():
    """Send list of online users to requesting client"""
    users = list(connected_users.values())
    emit('online_users', {'users': users})

if __name__ == '__main__':
    # Run the app on all interfaces (0.0.0.0) for network accessibility
    # Port 8080 (avoiding macOS AirPlay on 5000)
    # Using SSL/TLS for HTTPS
    socketio.run(app, 
                 host='0.0.0.0', 
                 port=8080, 
                 debug=True,
                 certfile='cert.pem',
                 keyfile='key.pem')
