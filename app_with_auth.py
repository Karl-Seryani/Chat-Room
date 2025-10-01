#!/usr/bin/env python3
"""
Authenticated Chat Room with MongoDB
Features: User authentication, contacts, private messaging
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from functools import wraps
import os
import base64
import uuid
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database models
try:
    from database import User, Message, Contact, FriendRequest, db, contacts_collection
    DB_AVAILABLE = True
except Exception as e:
    print(f"⚠️  Database not configured: {e}")
    print("📝 Please set up MongoDB Atlas and create .env file")
    DB_AVAILABLE = False

# Initialize Flask app
app = Flask(__name__, 
            static_folder='frontend/dist/assets',
            static_url_path='/assets')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-this')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')

# Initialize Socket.IO
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'  # Redirect to React app

# Store active connections: {user_id: session_id}
active_users = {}

# Flask-Login user loader
class AuthUser(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data['username']
        self.email = user_data.get('email')

@login_manager.user_loader
def load_user(user_id):
    if not DB_AVAILABLE:
        return None
    user_data = User.get_by_id(user_id)
    if user_data:
        return AuthUser(user_data)
    return None

# Routes
@app.route('/')
def index():
    """Serve React app"""
    return send_from_directory('frontend/dist', 'index.html')

@app.route('/<path:path>')
def serve_react(path):
    """Serve React app for all routes (for React Router)"""
    if path.startswith('api/') or path.startswith('socket.io/'):
        return jsonify({'error': 'Not found'}), 404
    
    # Check if file exists in dist folder
    file_path = os.path.join('frontend/dist', path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return send_from_directory('frontend/dist', path)
    
    # Otherwise serve index.html (for React Router)
    return send_from_directory('frontend/dist', 'index.html')

# Old template routes removed - React handles all routing

# Authentication API
@app.route('/api/signup', methods=['POST'])
def signup():
    """Create new user account"""
    if not DB_AVAILABLE:
        return jsonify({'error': 'Database not configured'}), 500
    
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    # Validate username
    if len(username) < 3 or len(username) > 20:
        return jsonify({'error': 'Username must be 3-20 characters'}), 400
    
    # Create user
    user_data = User.create(username, password, email)
    
    if not user_data:
        return jsonify({'error': 'Username already exists'}), 400
    
    return jsonify({'message': 'Account created successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    """Authenticate user"""
    if not DB_AVAILABLE:
        return jsonify({'error': 'Database not configured'}), 500
    
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    # Authenticate
    user_data = User.authenticate(username, password)
    
    if not user_data:
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # Login user
    user = AuthUser(user_data)
    login_user(user)
    
    return jsonify({
        'message': 'Login successful',
        'user': {
            'id': user.id,
            'username': user.username
        }
    }), 200

@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    """Logout user"""
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

# Contact API
@app.route('/api/contacts', methods=['GET'])
@login_required
def get_contacts():
    """Get user's contact list"""
    if not DB_AVAILABLE:
        return jsonify({'error': 'Database not configured'}), 500
    
    contacts = Contact.get_contacts(current_user.id)
    return jsonify({'contacts': contacts}), 200

# Username search/autocomplete
@app.route('/api/users/search', methods=['GET'])
@login_required
def search_users():
    """Search users by username (for autocomplete)"""
    if not DB_AVAILABLE:
        return jsonify({'error': 'Database not configured'}), 500
    
    query = request.args.get('q', '').strip()
    if len(query) < 2:
        return jsonify({'users': []}), 200
    
    # Search for users (case-insensitive, partial match)
    users = db['users'].find({
        'username': {'$regex': f'^{query}', '$options': 'i'}
    }).limit(10)
    
    results = []
    for user in users:
        if str(user['_id']) != current_user.id:  # Exclude self
            results.append({
                'username': user['username'],
                'id': str(user['_id'])
            })
    
    return jsonify({'users': results}), 200

# Friend Request APIs
@app.route('/api/friend-requests/send', methods=['POST'])
@login_required
def send_friend_request():
    """Send a friend request"""
    if not DB_AVAILABLE:
        return jsonify({'error': 'Database not configured'}), 500
    
    data = request.json
    recipient_username = data.get('username')
    
    if not recipient_username:
        return jsonify({'error': 'Username required'}), 400
    
    request_data, error = FriendRequest.send(current_user.id, recipient_username)
    
    if error:
        return jsonify({'error': error}), 400
    
    # Notify recipient via WebSocket
    recipient_user = User.get_by_username(recipient_username)
    if recipient_user and str(recipient_user['_id']) in active_users:
        recipient_sid = active_users[str(recipient_user['_id'])]
        socketio.emit('friend_request_received', {
            'sender_username': current_user.username,
            'sender_id': current_user.id
        }, room=recipient_sid)
    
    return jsonify({'message': 'Friend request sent', 'request': {
        'id': str(request_data['_id']),
        'recipient': recipient_username
    }}), 200

@app.route('/api/friend-requests/pending', methods=['GET'])
@login_required
def get_pending_requests():
    """Get pending friend requests"""
    if not DB_AVAILABLE:
        return jsonify({'error': 'Database not configured'}), 500
    
    requests = FriendRequest.get_pending(current_user.id)
    return jsonify({'requests': requests}), 200

@app.route('/api/friend-requests/accept', methods=['POST'])
@login_required
def accept_friend_request():
    """Accept a friend request"""
    if not DB_AVAILABLE:
        return jsonify({'error': 'Database not configured'}), 500
    
    data = request.json
    request_id = data.get('request_id')
    
    if not request_id:
        return jsonify({'error': 'Request ID required'}), 400
    
    success = FriendRequest.accept(request_id, current_user.id)
    
    if not success:
        return jsonify({'error': 'Request not found'}), 404
    
    # Get the request to find sender
    from bson import ObjectId
    req = db['friend_requests'].find_one({'_id': ObjectId(request_id)})
    sender = User.get_by_id(req['sender_id'])
    
    # Notify sender via WebSocket
    if sender and req['sender_id'] in active_users:
        sender_sid = active_users[req['sender_id']]
        socketio.emit('friend_request_accepted', {
            'accepter_username': current_user.username,
            'accepter_id': current_user.id
        }, room=sender_sid)
    
    # Send updated contacts to both users
    if current_user.id in active_users:
        contacts = Contact.get_contacts(current_user.id)
        socketio.emit('contacts_updated', {'contacts': contacts}, room=active_users[current_user.id])
    
    if req['sender_id'] in active_users:
        sender_contacts = Contact.get_contacts(req['sender_id'])
        socketio.emit('contacts_updated', {'contacts': sender_contacts}, room=active_users[req['sender_id']])
    
    return jsonify({'message': 'Friend request accepted'}), 200

@app.route('/api/friend-requests/reject', methods=['POST'])
@login_required
def reject_friend_request():
    """Reject a friend request"""
    if not DB_AVAILABLE:
        return jsonify({'error': 'Database not configured'}), 500
    
    data = request.json
    request_id = data.get('request_id')
    
    if not request_id:
        return jsonify({'error': 'Request ID required'}), 400
    
    FriendRequest.reject(request_id, current_user.id)
    return jsonify({'message': 'Friend request rejected'}), 200

@app.route('/api/contacts/remove', methods=['POST'])
@login_required
def remove_contact():
    """Remove a contact and delete all chat history"""
    if not DB_AVAILABLE:
        return jsonify({'error': 'Database not configured'}), 500
    
    data = request.json
    contact_id = data.get('contact_id')
    
    if not contact_id:
        return jsonify({'error': 'Contact ID required'}), 400
    
    # Get contact username before removing
    contact_user = User.get_by_id(contact_id)
    contact_username = contact_user['username'] if contact_user else 'User'
    
    # Remove mutual contact and all messages
    Contact.remove_mutual(current_user.id, contact_id)
    
    # Notify the other user via WebSocket
    if contact_id in active_users:
        contact_sid = active_users[contact_id]
        socketio.emit('contact_removed', {
            'removed_by_username': current_user.username,
            'removed_by_id': current_user.id
        }, room=contact_sid)
        
        # Send updated contact list to the other user
        updated_contacts = Contact.get_contacts(contact_id)
        socketio.emit('contacts_updated', {'contacts': updated_contacts}, room=contact_sid)
    
    # Send updated contact list to current user
    if current_user.id in active_users:
        my_contacts = Contact.get_contacts(current_user.id)
        socketio.emit('contacts_updated', {'contacts': my_contacts}, room=active_users[current_user.id])
    
    return jsonify({
        'message': 'Contact removed and chat history deleted',
        'contact_username': contact_username
    }), 200

@app.route('/api/messages/image', methods=['POST'])
@login_required
def upload_image():
    """Handle image upload and send as message"""
    if not DB_AVAILABLE:
        return jsonify({'error': 'Database not configured'}), 500
    
    # Check if image file is present
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    recipient_id = request.form.get('recipient_id')
    
    if not recipient_id:
        return jsonify({'error': 'Recipient ID required'}), 400
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Validate file type
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
    
    if file_ext not in allowed_extensions:
        return jsonify({'error': 'Invalid file type. Use: png, jpg, jpeg, gif, webp'}), 400
    
    try:
        # Read file and convert to base64 (for simplicity, storing inline)
        # In production, you'd upload to S3/CDN
        file_data = file.read()
        
        # Create data URI
        mime_type = f"image/{file_ext}"
        base64_data = base64.b64encode(file_data).decode('utf-8')
        data_uri = f"data:{mime_type};base64,{base64_data}"
        
        # Save message to database
        message = Message.create(
            sender_id=current_user.id,
            recipient_id=recipient_id,
            content=data_uri,
            message_type='image'
        )
        
        # Send via WebSocket to recipient if online
        if recipient_id in active_users:
            socketio.emit('new_message', {
                'sender_id': current_user.id,
                'sender_username': current_user.username,
                'content': data_uri,
                'type': 'image',
                'timestamp': message['timestamp'].isoformat(),
                'is_mine': False
            }, room=active_users[recipient_id])
        
        # Send confirmation to sender
        if current_user.id in active_users:
            socketio.emit('new_message', {
                'sender_id': current_user.id,
                'sender_username': current_user.username,
                'recipient_id': recipient_id,
                'content': data_uri,
                'type': 'image',
                'timestamp': message['timestamp'].isoformat(),
                'is_mine': True
            }, room=active_users[current_user.id])
        
        return jsonify({
            'success': True,
            'message': 'Image sent successfully',
            'image_url': data_uri
        }), 200
        
    except Exception as e:
        print(f"❌ Error uploading image: {e}")
        return jsonify({'error': 'Failed to upload image'}), 500

# WebSocket Events
def notify_contacts_status_change(user_id, online):
    """Notify all contacts when a user's status changes"""
    # Get all users who have this user as a contact
    contacts_with_user = contacts_collection.find({'contact_id': user_id})
    
    for contact_entry in contacts_with_user:
        contact_user_id = contact_entry['user_id']
        if contact_user_id in active_users:
            # Send updated contact list to this user
            updated_contacts = Contact.get_contacts(contact_user_id)
            socketio.emit('contacts_updated', {
                'contacts': updated_contacts
            }, room=active_users[contact_user_id])

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    if current_user.is_authenticated:
        # Track active user
        active_users[current_user.id] = request.sid
        
        # Set user as online in database
        Contact.set_online_status(current_user.id, online=True)
        
        # Notify all contacts that this user is now online
        notify_contacts_status_change(current_user.id, online=True)
        
        print(f'✅ User {current_user.username} connected')

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    if current_user.is_authenticated:
        # Remove from active users
        if current_user.id in active_users:
            del active_users[current_user.id]
        
        # Set user as offline in database
        Contact.set_online_status(current_user.id, online=False)
        
        # Notify all contacts that this user is now offline
        notify_contacts_status_change(current_user.id, online=False)
        
        print(f'❌ User {current_user.username} disconnected')

@socketio.on('load_conversation')
def handle_load_conversation(data):
    """Load conversation history with a contact"""
    if not current_user.is_authenticated or not DB_AVAILABLE:
        return
    
    contact_id = data.get('contact_id')
    
    if not contact_id:
        return
    
    # Load messages
    messages = Message.get_conversation(current_user.id, contact_id)
    
    # Format messages
    formatted_messages = []
    for msg in messages:
        contact = User.get_by_id(msg['sender'] if msg['sender'] != current_user.id else msg['recipient'])
        formatted_messages.append({
            'id': str(msg['_id']),
            'sender_id': msg['sender'],
            'sender_name': current_user.username if msg['sender'] == current_user.id else contact['username'],
            'content': msg['content'],
            'type': msg.get('type', 'text'),  # Include message type (text or image)
            'timestamp': msg['timestamp'].isoformat(),
            'is_mine': msg['sender'] == current_user.id
        })
    
    emit('conversation_loaded', {'messages': formatted_messages})

@socketio.on('send_private_message')
def handle_private_message(data):
    """Send private message to a contact"""
    if not current_user.is_authenticated or not DB_AVAILABLE:
        return
    
    recipient_id = data.get('recipient_id')
    content = data.get('content')
    
    if not recipient_id or not content:
        return
    
    # Check if they are contacts
    if not Contact.is_contact(current_user.id, recipient_id):
        emit('error', {'message': 'Not in contacts'})
        return
    
    # Save message
    message = Message.create(current_user.id, recipient_id, content)
    
    # Format message
    msg_data = {
        'id': str(message['_id']),
        'sender_id': current_user.id,
        'sender_name': current_user.username,
        'recipient_id': recipient_id,
        'content': content,
        'type': 'text',  # Text message type
        'timestamp': message['timestamp'].isoformat(),
        'is_mine': True
    }
    
    # Send to sender
    emit('message_sent', msg_data)
    
    # Send to recipient if online
    if recipient_id in active_users:
        recipient_sid = active_users[recipient_id]
        msg_data['is_mine'] = False
        socketio.emit('new_message', msg_data, room=recipient_sid)
    
    print(f'💬 {current_user.username} → Contact: {content}')

if __name__ == '__main__':
    if not DB_AVAILABLE:
        print("\n" + "="*60)
        print("⚠️  WARNING: MongoDB is not configured!")
        print("="*60)
        print("\n📝 To fix this:")
        print("1. Set up MongoDB Atlas (see MONGODB_SETUP.md)")
        print("2. Create .env file with your connection string")
        print("3. Run: pip3 install -r requirements.txt")
        print("\n" + "="*60 + "\n")
    
    # Run the app
    use_ssl = os.getenv('USE_SSL', 'true').lower() == 'true'
    
    if use_ssl:
        print("🔐 HTTPS mode with SSL certificates")
        socketio.run(app, 
                     host='0.0.0.0', 
                     port=8080, 
                     debug=True,
                     certfile='cert.pem',
                     keyfile='key.pem')
    else:
        print("🌐 HTTP mode (for ngrok)")
        socketio.run(app, 
                     host='0.0.0.0', 
                     port=8080, 
                     debug=True)
