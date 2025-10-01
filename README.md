# 💬 Real-Time Chat Application with Authentication

A full-stack, real-time messaging platform built with Flask, Socket.IO, and MongoDB. Features secure user authentication, friend request system, private messaging, and persistent chat history with real-time synchronization across clients.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-brightgreen.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)
![WebSocket](https://img.shields.io/badge/WebSocket-Socket.IO-black.svg)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Security Features](#security-features)
- [Future Improvements](#future-improvements)

---

## 🎯 Overview

This is a **production-ready real-time chat application** that implements modern web development practices including WebSocket communication, NoSQL database integration, containerization, and secure authentication. The application supports user registration, friend request workflows, private messaging with persistent storage, and live updates using Socket.IO.

Built with scalability in mind, the system uses MongoDB Atlas for cloud-based data persistence, Docker for containerization, and implements RESTful API patterns alongside WebSocket event-driven architecture.

---

## ✨ Features

### Core Functionality
- 🔐 **Secure User Authentication**
  - Password hashing with bcrypt
  - Session management with Flask-Login
  - Secure cookie-based authentication
  
- 👥 **Friend Request System**
  - Send/accept/reject friend requests
  - Real-time notifications for incoming requests
  - Duplicate request prevention
  - Bidirectional contact management

- 💬 **Private Messaging**
  - One-on-one real-time chat
  - Message persistence in MongoDB
  - Chat history retrieval (last 50 messages)
  - Message read status tracking

- 🔍 **User Discovery**
  - Real-time username autocomplete
  - Debounced search (300ms delay)
  - Case-insensitive partial matching
  - MongoDB regex-based queries

- 🗑️ **Contact Management**
  - Remove contacts with confirmation
  - Automatic chat history deletion
  - Bidirectional relationship cleanup
  - Real-time UI updates on both clients

### Real-Time Features
- ⚡ **WebSocket Communication**
  - Instant message delivery
  - Live friend request notifications
  - Real-time contact list updates
  - Online/offline status indicators

- 🔔 **Toast Notifications**
  - Success/error/info alerts
  - Auto-dismiss after 3 seconds
  - Non-intrusive UI feedback
  - Event-driven notification system

### User Experience
- 📱 **Responsive Design**
  - Mobile-first approach
  - Flexbox-based layouts
  - Smooth animations and transitions
  - Modern gradient UI elements

- 🎨 **Intuitive Interface**
  - Clean sidebar navigation
  - Chat window with message bubbles
  - Contact list with status indicators
  - Autocomplete dropdown for user search

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask 3.0.0
- **Real-Time**: Flask-SocketIO 5.3.5 + Socket.IO
- **Database**: MongoDB Atlas (Cloud NoSQL)
- **ODM**: PyMongo 4.6.0
- **Auth**: Flask-Login 0.6.3
- **Security**: bcrypt 4.1.2
- **Server**: eventlet 0.33.3

### Frontend
- **HTML5** with semantic markup
- **CSS3** (Flexbox, animations)
- **JavaScript** (ES6+)
- **Socket.IO Client** 4.5.4

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **SSL/TLS**: HTTPS enabled
- **Cloud Database**: MongoDB Atlas

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.9+
- Docker & Docker Compose
- MongoDB Atlas account

### Quick Start

1. **Clone repository**
```bash
git clone <repo-url>
cd Chat-Room
```

2. **Configure environment** (create `.env`)
```env
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/
DATABASE_NAME=chatroom_db
SECRET_KEY=your-secret-key
```

3. **Generate SSL certificates**
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

4. **Run with Docker**
```bash
docker-compose up -d --build
```

5. **Access**: https://localhost:8080

---

## 📖 Usage

### Web Application
1. Register/Login at `https://localhost:8080/auth`
2. Search users and send friend requests
3. Accept requests in sidebar
4. Click contact to start chatting
5. Remove friends with 🗑️ button

### User Management
```bash
python3 manage_users.py
```

---

## 📡 API Documentation

### REST Endpoints
- `POST /auth` - Login/signup
- `GET /api/users/search?q={query}` - Search users
- `POST /api/friend-requests/send` - Send request
- `GET /api/friend-requests/pending` - Get requests
- `POST /api/friend-requests/accept` - Accept request
- `POST /api/contacts/remove` - Remove contact

### WebSocket Events
**Emit:**
- `load_conversation` - Load chat history
- `send_private_message` - Send message

**Listen:**
- `conversation_loaded` - Receive history
- `new_message` - Receive message
- `friend_request_received` - New request
- `contacts_updated` - Contact list changed

---

## 🗄️ Database Schema

### Collections

**users**
```javascript
{
    _id: ObjectId,
    username: String (unique),
    password_hash: String (bcrypt),
    created_at: Date
}
```

**messages**
```javascript
{
    sender: String (user_id),
    recipient: String (user_id),
    content: String,
    timestamp: Date,
    read: Boolean
}
```

**contacts**
```javascript
{
    user_id: String,
    contact_id: String,
    contact_username: String,
    added_at: Date
}
```

**friend_requests**
```javascript
{
    sender_id: String,
    recipient_id: String,
    status: "pending|accepted|rejected",
    sent_at: Date
}
```

---

## 🔒 Security Features

- **Password Hashing**: bcrypt (cost 12)
- **Session Management**: Flask-Login
- **HTTPS**: SSL/TLS encryption
- **Input Validation**: Server-side checks
- **XSS Prevention**: HTML escaping
- **Environment Secrets**: `.env` file

---

## 🔮 Future Improvements

### Planned Features
- [ ] Group chat rooms
- [ ] File/image sharing
- [ ] Voice/video calls (WebRTC)
- [ ] End-to-end encryption
- [ ] Push notifications
- [ ] Message reactions
- [ ] Typing indicators
- [ ] Dark mode

### Scalability
- [ ] Redis for caching/pub-sub
- [ ] Kubernetes orchestration
- [ ] Microservices architecture
- [ ] CDN integration
- [ ] Database sharding

### DevOps
- [ ] CI/CD pipeline
- [ ] Prometheus monitoring
- [ ] ELK logging stack
- [ ] Load balancing
- [ ] Auto-scaling

---

## 📂 Project Structure

```
Chat-Room/
├── app_with_auth.py      # Main Flask app
├── database.py           # MongoDB models
├── manage_users.py       # CLI management
├── requirements.txt      # Dependencies
├── docker-compose.yml    # Container config
├── templates/
│   ├── auth.html        # Login/signup
│   └── chat.html        # Chat interface
└── README.md            # Documentation
```

---

## 👤 Author

**Karl Seryani**

---

## 🙏 Acknowledgments

- Flask - Python web framework
- Socket.IO - Real-time engine
- MongoDB - NoSQL database
- Docker - Containerization

---

<div align="center">

**⭐ Star this repo if you found it useful! ⭐**

Made with ❤️ and ☕

</div>
