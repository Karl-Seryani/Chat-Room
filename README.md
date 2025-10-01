# 🌿 Nature Chat - Real-Time Messaging Platform

A beautiful, full-stack real-time messaging platform with stunning nature-themed UI, animated backgrounds, and image sharing. Built with React, Flask, Socket.IO, and MongoDB. Features secure authentication, friend request system, private messaging, persistent chat history, and real-time synchronization.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![React](https://img.shields.io/badge/React-18+-61DAFB.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-brightgreen.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)
![WebSocket](https://img.shields.io/badge/WebSocket-Socket.IO-black.svg)
![HTTPS](https://img.shields.io/badge/HTTPS-Enabled-success.svg)

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

**Nature Chat** is a **production-ready real-time messaging platform** with a breathtaking nature-themed interface featuring animated backgrounds, glass-morphism effects, and seamless image sharing. This application implements modern web development practices including React SPA architecture, WebSocket communication, NoSQL database integration, and secure authentication.

The platform features:
- 🌿 **Stunning animated nature backgrounds** with floating gradients and drifting particles
- 🪟 **Glass-morphism UI** with backdrop blur effects
- 📷 **Image sharing** with preview and size validation
- 🦋 **Real-time messaging** with Socket.IO
- 🔐 **Secure authentication** with bcrypt password hashing
- 🌐 **Public access** via ngrok tunneling

Built with scalability in mind, the system uses MongoDB Atlas for cloud persistence, Docker for containerization, React for a modern SPA experience, and implements RESTful API patterns alongside WebSocket event-driven architecture.

---

## ✨ Features

### 🎨 Visual Experience
- 🌿 **Animated Nature Backgrounds**
  - Floating gradient orbs that drift and pulse
  - Drifting particle patterns
  - Slowly shifting tree silhouettes
  - 30-second smooth background animations
  
- 🪟 **Glass-Morphism UI**
  - Frosted glass effect (backdrop-blur)
  - Translucent panels with blur
  - Modern layered design
  - Smooth shadows and highlights

- 🎭 **Nature Theme**
  - "Nature Chat" branding throughout
  - Nature emoji integration (🌿🦋🌸🌱)
  - Peaceful, organic color palette
  - Rounded corners and soft edges

### 📷 Image Sharing
- 🖼️ **Upload & Share Images**
  - Click 📷 button to select images
  - Real-time image preview before sending
  - 5MB file size limit with validation
  - Image messages with click-to-enlarge
  - Remove image option before sending

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
  - Text and image message support

- 🔍 **User Discovery**
  - Real-time username autocomplete
  - Debounced search (300ms delay)
  - Case-insensitive partial matching
  - "Search nature lovers" interface

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
  - Glass-morphism gradient UI elements

- 🎨 **Intuitive Interface**
  - React-based SPA with React Router
  - Clean sidebar navigation with glass effect
  - Chat window with image/text message bubbles
  - Contact list with online/offline status
  - Autocomplete dropdown for user search
  - Toast notifications for user feedback

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
- **Environment**: python-dotenv

### Frontend
- **Framework**: React 18+ (with Vite)
- **Routing**: React Router DOM 6+
- **State Management**: Context API
- **HTTP Client**: Axios
- **Real-Time**: Socket.IO Client 4.5+
- **CSS**: Modern CSS3 with:
  - Backdrop-filter (glass-morphism)
  - CSS animations (keyframes)
  - Flexbox layouts
  - Gradient backgrounds

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **SSL/TLS**: HTTPS enabled with self-signed certs
- **Cloud Database**: MongoDB Atlas
- **Public Access**: ngrok tunneling
- **Build Tool**: Vite (for React)

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.9+
- Node.js 18+ & npm
- Docker & Docker Compose
- MongoDB Atlas account
- ngrok (for public access)

### Quick Start

1. **Clone repository**
```bash
git clone <repo-url>
cd Chat-Room
```

2. **Configure environment** (create `.env` in Chat-Room/)
```env
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/?authSource=admin
DATABASE_NAME=chatroom_db
SECRET_KEY=your-secret-key-here
USE_SSL=false  # Set to 'true' for local HTTPS, 'false' for ngrok
```

3. **Generate SSL certificates** (optional, for local HTTPS)
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

4. **Build React frontend**
```bash
cd frontend
npm install
npm run build
cd ..
```

5. **Run with Docker**
```bash
docker-compose up -d --build
```

6. **Access locally**: http://localhost:8080

7. **Public access** (optional, using ngrok)
```bash
ngrok http 8080
# Use the https://xxxxx.ngrok-free.app URL
```

---

## 📖 Usage

### Web Application
1. **Access the app** at `http://localhost:8080` or your ngrok URL
2. **Sign up** or **login** on the nature-themed auth page 🌿
3. **Search for users** using the "Search nature lovers" box 🌸
4. **Send friend requests** by clicking the ➕ button
5. **Accept requests** from the "Friend Requests" section
6. **Click a contact** to open chat window
7. **Send messages** - type and press Enter
8. **Share images** - click 📷 button, select image, send
9. **Remove friends** - click 🗑️ button (deletes all chat history)

### Development Mode (React)
```bash
cd frontend
npm run dev  # Runs on localhost:3000 with hot reload
```

### User Management (CLI)
```bash
python3 manage_users.py
# Options: List users, delete user, change password, view stats
```

### Docker Commands
```bash
# View logs
docker-compose logs -f web

# Stop containers
docker-compose down

# Rebuild after changes
docker-compose up -d --build
```

---

## 📡 API Documentation

### REST Endpoints

#### Authentication
- `POST /api/signup` - Create new user account
- `POST /api/login` - Authenticate user
- `POST /api/logout` - End session

#### User Discovery
- `GET /api/users/search?q={query}` - Search users (autocomplete)

#### Friend Requests
- `POST /api/friend-requests/send` - Send friend request
- `GET /api/friend-requests/pending` - Get pending requests
- `POST /api/friend-requests/accept` - Accept request
- `POST /api/friend-requests/reject` - Reject request

#### Contacts & Messages
- `GET /api/contacts` - Get user's contacts
- `POST /api/contacts/remove` - Remove contact & delete history
- `POST /api/messages/image` - Upload & send image (multipart/form-data)

### WebSocket Events

#### Client → Server (Emit)
- `connect` - Establish WebSocket connection
- `load_conversation` - Load chat history with contact
- `send_private_message` - Send text message

#### Server → Client (Listen)
- `conversation_loaded` - Receive chat history (50 messages)
- `new_message` - Receive new message in real-time
- `friend_request_received` - New friend request notification
- `friend_request_accepted` - Request accepted notification
- `contacts_updated` - Contact list changed (add/remove/online status)
- `disconnect` - WebSocket disconnected

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
    content: String,  // Text content or image URL
    type: String,     // "text" or "image"
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
    online: Boolean,      // Real-time online status
    last_seen: Date,
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

- **Password Hashing**: bcrypt (cost 12) with salt
- **Session Management**: Flask-Login with secure cookies
- **HTTPS**: SSL/TLS encryption (optional, configurable)
- **Input Validation**: Server-side checks & sanitization
- **File Upload Security**: 
  - File size limits (5MB for images)
  - File type validation (images only)
  - Secure file handling
- **XSS Prevention**: HTML escaping & Content-Security-Policy
- **Environment Secrets**: `.env` file (not in git)
- **CORS**: Configured for Socket.IO security
- **Authentication**: Protected routes & API endpoints

---

## 🔮 Future Improvements

### Planned Features
- [ ] Group chat rooms
- [x] ~~File/image sharing~~ ✅ **COMPLETED**
- [ ] Voice/video calls (WebRTC)
- [ ] End-to-end encryption
- [ ] Push notifications (PWA)
- [ ] Message reactions & emojis
- [ ] Typing indicators
- [ ] Dark mode toggle
- [ ] Message editing & deletion
- [ ] File attachments (PDFs, docs)
- [ ] Voice messages
- [ ] User profiles with avatars
- [ ] Multiple image uploads
- [ ] Image gallery view

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
├── app_with_auth.py           # Main Flask application
├── database.py                # MongoDB models & operations
├── manage_users.py            # CLI user management tool
├── requirements.txt           # Python dependencies
├── docker-compose.yml         # Multi-container orchestration
├── Dockerfile.web             # Web app container config
├── cert.pem & key.pem        # SSL certificates (self-signed)
├── .env                       # Environment variables (not in git)
├── .gitignore                 # Git ignore rules
├── frontend/                  # React SPA
│   ├── src/
│   │   ├── App.jsx           # Main app component & routing
│   │   ├── App.css           # Global styles
│   │   ├── pages/
│   │   │   ├── Auth.jsx      # Login/signup page
│   │   │   ├── Auth.css      # Auth page styles (animated bg)
│   │   │   ├── Chat.jsx      # Main chat page
│   │   │   └── Chat.css      # Chat page styles (nature theme)
│   │   ├── components/
│   │   │   ├── Sidebar.jsx   # Contacts & search
│   │   │   ├── Sidebar.css   # Sidebar glass-morphism
│   │   │   ├── ChatWindow.jsx # Message display & input
│   │   │   ├── ChatWindow.css # Chat bubbles & image messages
│   │   │   ├── Toast.jsx     # Notification component
│   │   │   └── Toast.css     # Toast animations
│   │   └── context/
│   │       ├── AuthContext.jsx    # Auth state management
│   │       └── SocketContext.jsx  # WebSocket management
│   ├── package.json          # Node dependencies
│   ├── vite.config.js        # Vite build config
│   └── dist/                 # Production build (served by Flask)
└── README.md                  # This file
```

---

## 👤 Author

**Karl Seryani**

---

## 🙏 Acknowledgments

- **Flask** - Python web framework
- **React** - Modern UI library
- **Socket.IO** - Real-time bidirectional communication
- **MongoDB** - Flexible NoSQL database
- **Docker** - Containerization platform
- **Vite** - Lightning-fast build tool
- **ngrok** - Secure tunneling for public access

---

## 🎨 Design Credits

The beautiful nature theme and glass-morphism effects were inspired by:
- Modern UI/UX design trends
- Nature photography and organic aesthetics
- Glass-morphism design patterns
- Smooth CSS animations and transitions

---

## 📸 Screenshots

### 🌿 Nature-Themed Login
Beautiful animated gradient background with floating particles and glass-morphism card.

### 💬 Chat Interface
Real-time messaging with glass panels, nature emojis, and smooth animations.

### 📷 Image Sharing
Upload and share images with preview, click-to-enlarge, and automatic delivery.

---

<div align="center">

**⭐ Star this repo if you found it useful! ⭐**

Made with ❤️, ☕, and 🌿

**Built by Karl Seryani**

</div>
