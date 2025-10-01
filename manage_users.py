#!/usr/bin/env python3
"""
User Management Script for Chat Room
Allows you to view, delete, and manage users in the database
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId

# Load environment variables
load_dotenv()

# Connect to MongoDB
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client = MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]

users_collection = db.users
contacts_collection = db.contacts
messages_collection = db.messages
friend_requests_collection = db.friend_requests


def list_all_users():
    """List all users in the database"""
    users = users_collection.find()
    
    print("\n" + "="*60)
    print("📋 ALL USERS IN DATABASE")
    print("="*60)
    
    count = 0
    for user in users:
        count += 1
        print(f"\n{count}. Username: {user['username']}")
        print(f"   User ID: {user['_id']}")
        print(f"   Created: {user.get('created_at', 'N/A')}")
    
    if count == 0:
        print("\n❌ No users found in database")
    else:
        print(f"\n✅ Total users: {count}")
    
    print("="*60 + "\n")
    return count


def delete_user_by_username(username):
    """Delete a user and all their associated data"""
    # Find the user
    user = users_collection.find_one({"username": username})
    
    if not user:
        print(f"\n❌ User '{username}' not found!\n")
        return False
    
    user_id = str(user['_id'])
    
    print(f"\n🗑️  Deleting user: {username} (ID: {user_id})")
    print("    This will delete:")
    print("    - User account")
    print("    - All contacts")
    print("    - All messages")
    print("    - All friend requests")
    
    confirm = input(f"\n⚠️  Type 'DELETE' to confirm: ")
    
    if confirm != 'DELETE':
        print("❌ Deletion cancelled\n")
        return False
    
    # Delete all related data
    print("\n🔄 Deleting user data...")
    
    # 1. Delete user document
    users_collection.delete_one({"_id": user['_id']})
    print(f"   ✓ User account deleted")
    
    # 2. Delete all contacts where user is either user_id or contact_id
    contacts_result = contacts_collection.delete_many({
        '$or': [
            {'user_id': user_id},
            {'contact_id': user_id}
        ]
    })
    print(f"   ✓ Deleted {contacts_result.deleted_count} contact entries")
    
    # 3. Delete all messages sent or received by user
    messages_result = messages_collection.delete_many({
        '$or': [
            {'sender': user_id},
            {'recipient': user_id}
        ]
    })
    print(f"   ✓ Deleted {messages_result.deleted_count} messages")
    
    # 4. Delete all friend requests
    requests_result = friend_requests_collection.delete_many({
        '$or': [
            {'sender_id': user_id},
            {'recipient_id': user_id}
        ]
    })
    print(f"   ✓ Deleted {requests_result.deleted_count} friend requests")
    
    print(f"\n✅ User '{username}' completely removed from database!\n")
    return True


def delete_all_users():
    """Delete ALL users from database (use with caution!)"""
    count = users_collection.count_documents({})
    
    if count == 0:
        print("\n❌ No users to delete\n")
        return
    
    print(f"\n⚠️  WARNING: This will delete ALL {count} users!")
    print("    This will also delete:")
    print("    - All contacts")
    print("    - All messages")
    print("    - All friend requests")
    
    confirm1 = input(f"\n⚠️  Type 'DELETE ALL' to confirm: ")
    
    if confirm1 != 'DELETE ALL':
        print("❌ Deletion cancelled\n")
        return
    
    confirm2 = input("⚠️  Are you ABSOLUTELY sure? Type 'YES': ")
    
    if confirm2 != 'YES':
        print("❌ Deletion cancelled\n")
        return
    
    print("\n🔄 Deleting all data...")
    
    users_collection.delete_many({})
    contacts_collection.delete_many({})
    messages_collection.delete_many({})
    friend_requests_collection.delete_many({})
    
    print("✅ All users and data deleted!\n")


def search_user(query):
    """Search for users by username"""
    users = users_collection.find({
        "username": {"$regex": query, "$options": "i"}
    })
    
    print(f"\n🔍 Search results for '{query}':")
    print("="*60)
    
    count = 0
    for user in users:
        count += 1
        print(f"\n{count}. Username: {user['username']}")
        print(f"   User ID: {user['_id']}")
    
    if count == 0:
        print("\n❌ No users found")
    else:
        print(f"\n✅ Found {count} user(s)")
    
    print("="*60 + "\n")


def get_user_stats(username):
    """Get statistics for a specific user"""
    user = users_collection.find_one({"username": username})
    
    if not user:
        print(f"\n❌ User '{username}' not found!\n")
        return
    
    user_id = str(user['_id'])
    
    # Count contacts
    contacts_count = contacts_collection.count_documents({'user_id': user_id})
    
    # Count messages sent
    messages_sent = messages_collection.count_documents({'sender': user_id})
    
    # Count messages received
    messages_received = messages_collection.count_documents({'recipient': user_id})
    
    # Count pending friend requests
    requests_sent = friend_requests_collection.count_documents({
        'sender_id': user_id,
        'status': 'pending'
    })
    requests_received = friend_requests_collection.count_documents({
        'recipient_id': user_id,
        'status': 'pending'
    })
    
    print(f"\n📊 Statistics for '{username}':")
    print("="*60)
    print(f"User ID: {user_id}")
    print(f"Contacts: {contacts_count}")
    print(f"Messages sent: {messages_sent}")
    print(f"Messages received: {messages_received}")
    print(f"Friend requests sent (pending): {requests_sent}")
    print(f"Friend requests received (pending): {requests_received}")
    print("="*60 + "\n")


def main_menu():
    """Display main menu"""
    while True:
        print("\n" + "="*60)
        print("🛠️  CHAT ROOM - USER MANAGEMENT")
        print("="*60)
        print("\n1. List all users")
        print("2. Delete user by username")
        print("3. Search users")
        print("4. Get user statistics")
        print("5. Delete ALL users (⚠️ DANGER)")
        print("6. Exit")
        
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == '1':
            list_all_users()
        
        elif choice == '2':
            username = input("\nEnter username to delete: ").strip()
            if username:
                delete_user_by_username(username)
        
        elif choice == '3':
            query = input("\nEnter search query: ").strip()
            if query:
                search_user(query)
        
        elif choice == '4':
            username = input("\nEnter username: ").strip()
            if username:
                get_user_stats(username)
        
        elif choice == '5':
            delete_all_users()
        
        elif choice == '6':
            print("\n👋 Goodbye!\n")
            break
        
        else:
            print("\n❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    try:
        print("\n🔌 Connecting to MongoDB...")
        # Test connection
        db.command('ping')
        print(f"✅ Connected to database: {DATABASE_NAME}\n")
        
        main_menu()
        
    except Exception as e:
        print(f"\n❌ Error connecting to database: {e}\n")
        print("💡 Make sure your .env file is configured correctly")

