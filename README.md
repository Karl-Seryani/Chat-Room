# 🔒 Secure Real-Time Chat Platform

A production-ready messaging application demonstrating secure coding practices, network protocols, and cloud infrastructure management. Built with React, Flask, Socket.IO, and MongoDB Atlas. Features secure authentication, real-time communication, encrypted data transmission, and scalable containerized deployment.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![React](https://img.shields.io/badge/React-18+-61DAFB.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-brightgreen.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)
![WebSocket](https://img.shields.io/badge/WebSocket-Socket.IO-black.svg)
![ngrok](https://img.shields.io/badge/ngrok-Public%20Access-orange.svg)

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

**Secure Chat Platform** is a **production-ready real-time messaging application** demonstrating cybersecurity best practices, secure network protocols, and cloud infrastructure management. This application implements secure coding practices including encrypted authentication, WebSocket communication protocols, NoSQL database security, and containerized deployment.

The platform features:
- 🔐 **Secure Authentication**: bcrypt password hashing, session management, input validation
- 🌐 **Network Security**: WebSocket protocols, HTTPS/SSL, CORS configuration
- ☁️ **Cloud Infrastructure**: MongoDB Atlas database, Docker containerization
- 🔒 **Data Protection**: Encrypted transmission, secure file handling, environment secrets
- 📡 **Real-time Communication**: Socket.IO protocols, instant messaging, status updates

Built with security in mind, the system implements secure coding practices, network protocol management, cloud database security, containerized deployment, and secure real-time communication protocols.

---

## ✨ Technical Features

### 🔐 Security Implementation
- **Password Security**: bcrypt hashing with salt (cost factor 12) for secure password storage
- **Session Management**: Flask-Login with secure cookie-based authentication
- **Input Validation**: Server-side sanitization and validation for all user inputs
- **File Upload Security**: File type validation, size limits (5MB), and secure handling
- **Environment Security**: Protected environment variables and secrets management

### 🌐 Network & Communication
- **WebSocket Protocols**: Real-time bidirectional communication using Socket.IO
- **HTTP/HTTPS**: Configurable SSL/TLS encryption for secure data transmission
- **CORS Configuration**: Proper cross-origin resource sharing for API security
- **RESTful APIs**: Secure endpoint design with authentication middleware
- **Data Encryption**: Secure transmission of sensitive data over network protocols

### ☁️ Cloud Infrastructure
- **MongoDB Atlas**: Cloud NoSQL database with automated backups and scaling
- **Docker Containerization**: Isolated application deployment with environment consistency
- **ngrok Tunneling**: Secure public access with encrypted tunnel protocols
- **Environment Configuration**: Secure environment variable management for production deployment

### 🗄️ Database Architecture
- **NoSQL Design**: MongoDB with optimized collections and indexing for performance
- **Data Persistence**: Secure message storage with user relationship management
- **Indexing Strategy**: Compound indexes for efficient query performance
- **Connection Management**: Secure database connection with error handling and retry logic

### 🔄 Real-Time Architecture
- **Event-Driven Communication**: Socket.IO event handling for instant message delivery
- **Connection Management**: WebSocket connection lifecycle and error recovery
- **State Synchronization**: Real-time user status updates and contact management
- **Message Queuing**: Reliable message delivery with acknowledgment patterns

---

## 🛠️ Tech Stack

### Backend Technologies
- **Framework**: Flask 3.0.0 (Python web framework)
- **Real-Time**: Flask-SocketIO 5.3.5 + Socket.IO (WebSocket communication)
- **Database**: MongoDB Atlas (Cloud NoSQL with security features)
- **ODM**: PyMongo 4.6.0 (MongoDB driver with connection pooling)
- **Authentication**: Flask-Login 0.6.3 (Session management)
- **Security**: bcrypt 4.1.2 (Password hashing)
- **Server**: eventlet 0.33.3 (WSGI server for production)
- **Configuration**: python-dotenv (Environment variable management)

### Frontend Technologies
- **Framework**: React 18+ (Component-based UI)
- **Build Tool**: Vite (Fast build system and dev server)
- **State Management**: Context API (React state management)
- **HTTP Client**: Axios (Promise-based HTTP requests)
- **Real-Time**: Socket.IO Client 4.5+ (WebSocket client library)
- **Security**: CSP headers, XSS prevention, secure cookie handling

### Infrastructure & DevOps
- **Containerization**: Docker + Docker Compose (Application containerization)
- **Cloud Database**: MongoDB Atlas (Managed cloud database)
- **Public Access**: ngrok tunneling (Secure tunnel for public access)
- **Environment**: Production-ready configuration with security hardening

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
USE_SSL=false  # HTTP mode for ngrok compatibility
```

3. **Build React frontend**
```bash
cd frontend
npm install
npm run build
cd ..
```

4. **Run with Docker**
```bash
docker-compose up -d --build
```

5. **Access locally**: http://localhost:8080

6. **Public access** (using ngrok)
```bash
ngrok http 8080
# Use the https://xxxxx.ngrok-free.dev URL
```

---

## 📖 Usage

### Application Access
1. **Local Development**: Access at `http://localhost:8080`
2. **Public Access**: Use ngrok tunnel URL for external testing
3. **Authentication**: Secure login/signup with bcrypt password hashing
4. **Real-Time Features**: WebSocket connection for instant messaging
5. **API Testing**: RESTful endpoints for user management and messaging

### Development Mode (React)
```bash
cd frontend
npm run dev  # Runs on localhost:3000 with hot reload
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

## 🔒 Security Implementation

### Authentication & Authorization
- **Password Security**: bcrypt hashing with salt (cost factor 12) for secure password storage
- **Session Management**: Flask-Login with secure cookie-based authentication and session persistence
- **Protected Routes**: Middleware authentication for all sensitive API endpoints
- **Input Validation**: Server-side sanitization and validation for all user inputs and file uploads

### Network Security
- **HTTPS/SSL**: Configurable SSL/TLS encryption for secure data transmission
- **CORS Configuration**: Proper cross-origin resource sharing policies for API security
- **WebSocket Security**: Secure Socket.IO connection with authentication validation
- **Environment Security**: Protected environment variables and secrets management

### Data Protection
- **File Upload Security**: File type validation, size limits (5MB), and secure handling
- **XSS Prevention**: HTML escaping, Content-Security-Policy headers, and input sanitization
- **Database Security**: MongoDB Atlas with encrypted connections and access controls
- **Secure Transmission**: All sensitive data encrypted during network transmission

---

## 🔮 Technical Roadmap

### Security Enhancements
- [ ] End-to-end encryption for messages
- [ ] Two-factor authentication (2FA)
- [ ] Rate limiting and DDoS protection
- [ ] Advanced threat detection
- [ ] Security audit logging
- [ ] OWASP compliance implementation

### Infrastructure Scaling
- [ ] Redis for caching and pub-sub messaging
- [ ] Kubernetes orchestration for container management
- [ ] Microservices architecture decomposition
- [ ] Load balancing and auto-scaling
- [ ] Database sharding and replication

### DevOps & Monitoring
- [ ] CI/CD pipeline with automated security testing
- [ ] Prometheus monitoring and alerting
- [ ] ELK stack for centralized logging
- [ ] Container security scanning
- [ ] Infrastructure as Code (Terraform)

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

</div>
