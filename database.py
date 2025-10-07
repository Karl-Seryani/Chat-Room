"""
Database configuration and models for MongoDB
"""

from pymongo import MongoClient
from datetime import datetime
import bcrypt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'chatroom_db')

client = MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]

# Collections
users_collection = db['users']
messages_collection = db['messages']
contacts_collection = db['contacts']

# Create indexes for better performance
users_collection.create_index('username', unique=True)
messages_collection.create_index([('sender', 1), ('recipient', 1), ('timestamp', -1)])
contacts_collection.create_index([('user_id', 1), ('contact_id', 1)], unique=True)


class User:
    """User model for authentication and profile"""
    
    @staticmethod
    def create(username, password, email=None):
        """Create a new user with hashed password"""
        # Check if username already exists
        if users_collection.find_one({'username': username}):
            return None
        
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        user_data = {
            'username': username,
            'password': hashed_password,
            'email': email,
            'created_at': datetime.utcnow(),
            'online': False
        }
        
        result = users_collection.insert_one(user_data)
        user_data['_id'] = result.inserted_id
        return user_data
    
    @staticmethod
    def authenticate(username, password):
        """Verify username and password"""
        user = users_collection.find_one({'username': username})
        
        if user:
            # Handle both old format (password) and new format (password_hash)
            password_field = user.get('password_hash') or user.get('password')
            if password_field:
                # Handle both string and bytes password storage
                if isinstance(password_field, str):
                    password_field = password_field.encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), password_field):
                    return user
        return None
    
    @staticmethod
    def get_by_username(username):
        """Get user by username"""
        return users_collection.find_one({'username': username})
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        from bson import ObjectId
        return users_collection.find_one({'_id': ObjectId(user_id)})
    
    @staticmethod
    def set_online(user_id, status=True):
        """Set user online/offline status"""
        from bson import ObjectId
        users_collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'online': status}}
        )


class Message:
    """Message model for storing chat messages"""
    
    @staticmethod
    def create(sender_id, recipient_id, content, message_type='text'):
        """Create a new message (text or image)"""
        message_data = {
            'sender': sender_id,
            'recipient': recipient_id,
            'content': content,
            'type': message_type,  # 'text' or 'image'
            'timestamp': datetime.utcnow(),
            'read': False
        }
        
        result = messages_collection.insert_one(message_data)
        message_data['_id'] = result.inserted_id
        return message_data
    
    @staticmethod
    def get_conversation(user1_id, user2_id, limit=50):
        """Get messages between two users"""
        messages = messages_collection.find({
            '$or': [
                {'sender': user1_id, 'recipient': user2_id},
                {'sender': user2_id, 'recipient': user1_id}
            ]
        }).sort('timestamp', -1).limit(limit)
        
        
        # Reverse to show oldest first
        return list(reversed(list(messages)))
    
    @staticmethod
    def mark_as_read(message_id):
        """Mark message as read"""
        from bson import ObjectId
        messages_collection.update_one(
            {'_id': ObjectId(message_id)},
            {'$set': {'read': True}}
        )


class FriendRequest:
    """Friend request model"""
    
    @staticmethod
    def send(sender_id, recipient_username):
        """Send a friend request"""
        # Get recipient user
        recipient = User.get_by_username(recipient_username)
        if not recipient:
            return None, "User not found"
        
        recipient_id = str(recipient['_id'])
        
        # Can't send to yourself
        if sender_id == recipient_id:
            return None, "Cannot add yourself"
        
        # Check if already contacts
        if Contact.is_contact(sender_id, recipient_id):
            return None, "Already in contacts"
        
        # Check if request already exists
        existing = db['friend_requests'].find_one({
            'sender_id': sender_id,
            'recipient_id': recipient_id,
            'status': 'pending'
        })
        if existing:
            return None, "Friend request already sent"
        
        # Check if recipient already sent you a request
        reverse = db['friend_requests'].find_one({
            'sender_id': recipient_id,
            'recipient_id': sender_id,
            'status': 'pending'
        })
        if reverse:
            return None, "This user already sent you a request"
        
        request_data = {
            'sender_id': sender_id,
            'recipient_id': recipient_id,
            'recipient_username': recipient_username,
            'status': 'pending',
            'sent_at': datetime.utcnow()
        }
        
        result = db['friend_requests'].insert_one(request_data)
        request_data['_id'] = result.inserted_id
        return request_data, None
    
    @staticmethod
    def get_pending(user_id):
        """Get pending friend requests for a user"""
        requests = db['friend_requests'].find({
            'recipient_id': user_id,
            'status': 'pending'
        })
        
        result = []
        for req in requests:
            sender = User.get_by_id(req['sender_id'])
            if sender:
                result.append({
                    'id': str(req['_id']),
                    'sender_id': req['sender_id'],
                    'sender_username': sender['username'],
                    'sent_at': req['sent_at'].isoformat()
                })
        return result
    
    @staticmethod
    def accept(request_id, user_id):
        """Accept a friend request"""
        from bson import ObjectId
        
        req = db['friend_requests'].find_one({
            '_id': ObjectId(request_id),
            'recipient_id': user_id,
            'status': 'pending'
        })
        
        if not req:
            return False
        
        # Add both as contacts
        Contact.add_direct(req['sender_id'], req['recipient_id'])
        Contact.add_direct(req['recipient_id'], req['sender_id'])
        
        # Update request status
        db['friend_requests'].update_one(
            {'_id': ObjectId(request_id)},
            {'$set': {'status': 'accepted', 'accepted_at': datetime.utcnow()}}
        )
        
        return True
    
    @staticmethod
    def reject(request_id, user_id):
        """Reject a friend request"""
        from bson import ObjectId
        
        db['friend_requests'].update_one(
            {'_id': ObjectId(request_id), 'recipient_id': user_id},
            {'$set': {'status': 'rejected', 'rejected_at': datetime.utcnow()}}
        )
        return True


class Contact:
    """Contact model for managing user connections"""
    
    @staticmethod
    def add_direct(user_id, contact_id):
        """Add a contact directly (used after accepting friend request)"""
        contact_user = User.get_by_id(contact_id)
        if not contact_user:
            return None
        
        contact_data = {
            'user_id': user_id,
            'contact_id': contact_id,
            'contact_username': contact_user['username'],
            'added_at': datetime.utcnow()
        }
        
        try:
            result = contacts_collection.insert_one(contact_data)
            contact_data['_id'] = result.inserted_id
            return contact_data
        except:
            return None
    
    @staticmethod
    def remove(user_id, contact_id):
        """Remove a contact (one-way)"""
        contacts_collection.delete_one({
            'user_id': user_id,
            'contact_id': contact_id
        })
    
    @staticmethod
    def remove_mutual(user1_id, user2_id):
        """Remove contact from both users and delete all messages"""
        # Remove from both sides
        contacts_collection.delete_one({'user_id': user1_id, 'contact_id': user2_id})
        contacts_collection.delete_one({'user_id': user2_id, 'contact_id': user1_id})
        
        # Delete all messages between them (using correct field names: 'sender' and 'recipient')
        result = messages_collection.delete_many({
            '$or': [
                {'sender': user1_id, 'recipient': user2_id},
                {'sender': user2_id, 'recipient': user1_id}
            ]
        })
        
        print(f"🗑️ Deleted {result.deleted_count} messages between users")
        return True
    
    @staticmethod
    def get_contacts(user_id):
        """Get all contacts for a user with real-time online status"""
        contacts = contacts_collection.find({'user_id': user_id})
        
        contact_list = []
        for contact in contacts:
            contact_user = User.get_by_id(contact['contact_id'])
            if contact_user:
                contact_list.append({
                    'id': str(contact_user['_id']),
                    'username': contact_user['username'],
                    'online': contact_user.get('online', False)
                })
        
        return contact_list
    
    @staticmethod
    def set_online_status(user_id, online=True):
        """Update user's online status"""
        from bson import ObjectId
        users_collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'online': online, 'last_seen': datetime.utcnow()}}
        )
        return True
    
    @staticmethod
    def is_contact(user_id, contact_id):
        """Check if two users are contacts"""
        return contacts_collection.find_one({
            'user_id': user_id,
            'contact_id': contact_id
        }) is not None


# Initialize database on import
def init_db():
    """Initialize database with indexes"""
    print(f"Connected to MongoDB: {DATABASE_NAME}")
    print(f"Collections: users, messages, contacts")

init_db()
