import { useState, useEffect, useRef } from 'react';
import { useSocket } from '../context/SocketContext';
import axios from 'axios';
import './ChatWindow.css';

function ChatWindow({ selectedContact, onShowToast, onContactRemoved }) {
  const [messages, setMessages] = useState([]);
  const [messageInput, setMessageInput] = useState('');
  const [selectedImage, setSelectedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);
  
  const { socket } = useSocket();

  // Load conversation when contact is selected
  useEffect(() => {
    if (selectedContact && socket) {
      socket.emit('load_conversation', { contact_id: selectedContact.id });
      setMessages([]);
    }
  }, [selectedContact, socket]);

  // Socket event listeners
  useEffect(() => {
    if (!socket) return;

    socket.on('conversation_loaded', (data) => {
      setMessages(data.messages || []);
    });

    socket.on('message_sent', (data) => {
      addMessage(data.content, true);
    });

    socket.on('new_message', (data) => {
      if (selectedContact && data.sender_id === selectedContact.id) {
        addMessage(data.content, false);
      }
    });

    return () => {
      socket.off('conversation_loaded');
      socket.off('message_sent');
      socket.off('new_message');
    };
  }, [socket, selectedContact]);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const addMessage = (content, isMine) => {
    setMessages((prev) => [
      ...prev,
      {
        content,
        is_mine: isMine,
        timestamp: new Date().toISOString()
      }
    ]);
  };

  const handleImageSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) { // 5MB limit
        onShowToast('❌ Image must be smaller than 5MB', 'error');
        return;
      }
      
      setSelectedImage(file);
      
      // Create preview
      const reader = new FileReader();
      reader.onload = (e) => setImagePreview(e.target.result);
      reader.readAsDataURL(file);
    }
  };

  const removeImage = () => {
    setSelectedImage(null);
    setImagePreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const sendMessage = async () => {
    if ((!messageInput.trim() && !selectedImage) || !selectedContact || !socket) return;

    if (selectedImage) {
      // Send image message
      const formData = new FormData();
      formData.append('image', selectedImage);
      formData.append('recipient_id', selectedContact.id);
      
      try {
        const response = await axios.post('/api/messages/image', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        
        if (response.data.success) {
          onShowToast('📷 Image sent!', 'success');
          removeImage();
        }
      } catch (error) {
        onShowToast('❌ Failed to send image', 'error');
      }
    } else {
      // Send text message
      socket.emit('send_private_message', {
        recipient_id: selectedContact.id,
        content: messageInput.trim()
      });
    }

    setMessageInput('');
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const removeContact = async () => {
    if (!selectedContact) return;

    const confirmed = window.confirm(
      `Remove ${selectedContact.username} from contacts?\n\n⚠️ This will permanently delete all chat history between you.`
    );

    if (!confirmed) return;

    try {
      const response = await axios.post('/api/contacts/remove', {
        contact_id: selectedContact.id
      });

      onShowToast(`🗑️ Removed ${selectedContact.username} and deleted all chats`, 'success');
      onContactRemoved();
    } catch (error) {
      onShowToast('❌ Failed to remove contact', 'error');
    }
  };

  if (!selectedContact) {
    return (
      <div className="chat-window">
        <div className="empty-state">
          <div className="empty-icon">💬</div>
          <h2>Select a contact to start chatting</h2>
          <p>Choose someone from your contacts list</p>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-window">
      {/* Chat Header */}
      <div className="chat-header">
        <div>
          <h3>{selectedContact.username}</h3>
          <div className={`status ${selectedContact.online ? 'online' : 'offline'}`}>
            {selectedContact.online ? '● Online' : '○ Offline'}
          </div>
        </div>
        <button className="btn-remove-contact" onClick={removeContact}>
          🗑️ Remove Friend
        </button>
      </div>

      {/* Messages Container */}
      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="no-messages">
            No messages yet. Start the conversation!
          </div>
        ) : (
          messages.map((msg, index) => (
            <div
              key={index}
              className={`message ${msg.is_mine ? 'mine' : 'theirs'}`}
            >
              <div className={`message-bubble ${msg.type === 'image' ? 'image-message' : ''}`}>
                {msg.type === 'image' ? (
                  <img 
                    src={msg.content} 
                    alt="Shared image" 
                    className="message-image"
                    onClick={() => window.open(msg.content, '_blank')}
                  />
                ) : (
                  msg.content
                )}
              </div>
              {msg.timestamp && (
                <div className="message-time">
                  {new Date(msg.timestamp).toLocaleTimeString([], {
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </div>
              )}
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Message Input */}
      <div className="message-input-container">
        <div className="input-wrapper">
          {/* Image Preview */}
          {imagePreview && (
            <div className="image-preview-container">
              <img src={imagePreview} alt="Preview" className="image-preview" />
              <button className="remove-image-btn" onClick={removeImage}>×</button>
            </div>
          )}
          
          {/* Input Row */}
          <div className="input-row">
            <button 
              className="image-upload-btn" 
              onClick={() => fileInputRef.current?.click()}
              title="Add image"
            >
              📷
            </button>
            <input
              type="text"
              placeholder="Type a message..."
              value={messageInput}
              onChange={(e) => setMessageInput(e.target.value)}
              onKeyPress={handleKeyPress}
              maxLength={500}
            />
            <button 
              onClick={sendMessage} 
              disabled={!messageInput.trim() && !selectedImage}
            >
              Send
            </button>
          </div>
        </div>
        
        {/* Hidden file input */}
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleImageSelect}
          style={{ display: 'none' }}
        />
      </div>
    </div>
  );
}

export default ChatWindow;

