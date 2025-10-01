# 💾 Chat History Feature Guide

## ✨ New Feature: Personal Chat History

Your chat room now saves messages for each username! When you rejoin with the same username, you'll see your previous messages.

---

## 🎯 How It Works

### **1. When You Send a Message:**
- Your message is broadcast to everyone
- It's also saved to your personal history
- Stored with a timestamp

### **2. When You Rejoin:**
- Use the same username
- Your last 50 messages are loaded
- See exactly what you said before!

---

## 📋 Features

### **✅ What's Saved:**
- ✅ Your messages
- ✅ Timestamps (when you sent them)
- ✅ Last 100 messages per user (to save space)

### **❌ What's NOT Saved:**
- ❌ Other people's messages to you
- ❌ Join/leave notifications
- ❌ Messages older than your last 100

---

## 💡 Use Cases

### **Scenario 1: Connection Lost**
```
1. You're chatting as "Alice"
2. WiFi disconnects
3. You reconnect as "Alice"
4. All your previous messages appear!
```

### **Scenario 2: Come Back Later**
```
1. Chat as "Bob" today
2. Close browser
3. Return tomorrow as "Bob"
4. See what you said yesterday!
```

### **Scenario 3: Multiple Sessions**
```
1. Chat on laptop as "Charlie"
2. Switch to phone as "Charlie"
3. Your message history follows you!
```

---

## 🔍 Technical Details

### **Storage:**
- **File:** `chat_history.json`
- **Format:** JSON (easy to read/backup)
- **Location:** Same folder as `web_app.py`

### **Data Structure:**
```json
{
  "Alice": [
    {
      "message": "Hello everyone!",
      "timestamp": "2025-09-30T18:10:15.123456"
    },
    {
      "message": "How are you?",
      "timestamp": "2025-09-30T18:10:20.654321"
    }
  ],
  "Bob": [
    {
      "message": "I'm good!",
      "timestamp": "2025-09-30T18:10:22.789012"
    }
  ]
}
```

### **Limits:**
- **Per-user storage:** 100 messages max
- **Display on join:** Last 50 messages
- **Auto-cleanup:** Oldest messages removed when limit hit

---

## 🎨 UI Changes

### **Welcome Messages:**

**First-time user:**
```
Welcome to the chat, Alice!
```

**Returning user:**
```
Welcome back, Alice! Loading your chat history...
[Your previous messages appear]
--- You are now connected ---
```

### **Message Display:**
```
Alice  3:15 PM
Hello everyone!

Alice  3:16 PM
How are you?
```

---

## 📁 File Management

### **Backup Your History:**
```bash
# Copy the history file
cp chat_history.json chat_history_backup.json

# Or view it
cat chat_history.json
```

### **Delete History:**
```bash
# Delete specific user
# Edit chat_history.json and remove their section

# Delete all history
rm chat_history.json
```

### **Transfer to Another Server:**
```bash
# Copy file to new location
scp chat_history.json user@server:/path/to/chatroom/
```

---

## 🔒 Privacy & Security

### **What You Should Know:**

⚠️ **Usernames are NOT passwords**
- Anyone can use any username (if not currently online)
- They'll see that username's history
- NOT secure for private data

⚠️ **Messages stored in plain text**
- `chat_history.json` is readable by anyone with file access
- Don't share sensitive information

✅ **What's Protected:**
- File is in `.gitignore` (won't commit to git)
- Only accessible on the server
- Encrypted in transit (HTTPS)

---

## 🛠️ For Developers

### **Add More Features:**

**1. Delete Your History:**
```python
@socketio.on('delete_history')
def handle_delete_history():
    username = connected_users[request.sid]
    history = load_chat_history()
    if username in history:
        del history[username]
        save_chat_history(history)
```

**2. Export History:**
```python
@socketio.on('export_history')
def handle_export():
    username = connected_users[request.sid]
    messages = get_user_messages(username, limit=1000)
    emit('history_export', {'messages': messages})
```

**3. Search Messages:**
```python
def search_messages(username, query):
    history = load_chat_history()
    user_messages = history.get(username, [])
    return [m for m in user_messages if query.lower() in m['message'].lower()]
```

---

## 🐳 Docker Considerations

### **Data Persistence:**

⚠️ **Current Setup:**
- History saved INSIDE container
- Lost when container is removed!

### **Make It Persistent:**

**Add to `docker-compose.yml`:**
```yaml
services:
  web:
    volumes:
      - ./chat_data:/app/chat_data
```

**Update `web_app.py`:**
```python
HISTORY_FILE = 'chat_data/chat_history.json'
```

**Create directory:**
```bash
mkdir chat_data
```

Now history persists even when container restarts!

---

## 📊 Example Usage

### **Testing It:**

1. **Open chat:** `https://192.168.2.103:8080`
2. **Join as "TestUser"**
3. **Send messages:**
   - "This is my first message"
   - "This is my second message"
4. **Close browser**
5. **Reopen and join as "TestUser"**
6. **See your messages appear!** ✨

---

## 🔄 Upgrading

### **From Old Version (No History):**
- No migration needed
- History starts fresh
- Old conversations not saved (they were never stored)

### **Backup Before Updating:**
```bash
# If you have chat_history.json
cp chat_history.json chat_history_backup_$(date +%Y%m%d).json
```

---

## 🐛 Troubleshooting

### **History Not Loading:**
1. Check file exists: `ls chat_history.json`
2. Check permissions: `ls -la chat_history.json`
3. Check JSON format: `python -m json.tool chat_history.json`

### **Messages Not Saving:**
1. Check disk space: `df -h`
2. Check logs: `docker logs chatroom-web`
3. Verify write permissions

### **Docker Container Issue:**
```bash
# Check if volume mounted
docker inspect chatroom-web | grep -A 10 Mounts

# Access container
docker exec -it chatroom-web ls -la /app/
```

---

## 💡 Future Enhancements

### **Could Add:**
- 🔍 Search your message history
- 📤 Export chat to text file
- 🗑️ Delete your own messages
- ⏰ Auto-delete old messages (7 days+)
- 👥 Shared room history (all messages)
- 🔐 Password-protected usernames
- 📊 Statistics (most active users, etc.)
- 💬 Private message history

---

## 🎯 Summary

**What Changed:**
- ✅ Messages now saved per username
- ✅ History loaded on rejoin
- ✅ Timestamps displayed
- ✅ Last 50 messages shown
- ✅ Max 100 messages stored per user

**Files Modified:**
- `web_app.py` - Added history functions
- `templates/index.html` - Display history
- `.gitignore` - Exclude history file

**New Files:**
- `chat_history.json` - Stores all messages

---

**Enjoy your persistent chat history!** 💬💾

