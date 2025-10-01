import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useSocket } from '../context/SocketContext';
import axios from 'axios';
import Sidebar from '../components/Sidebar';
import ChatWindow from '../components/ChatWindow';
import Toast from '../components/Toast';
import './Chat.css';

function Chat() {
  const [contacts, setContacts] = useState([]);
  const [friendRequests, setFriendRequests] = useState([]);
  const [selectedContact, setSelectedContact] = useState(null);
  const [toast, setToast] = useState({ show: false, message: '', type: 'info' });
  
  const { user, logout } = useAuth();
  const { socket, connected } = useSocket();

  // Load contacts and friend requests
  useEffect(() => {
    if (user) {
      loadContacts();
      loadFriendRequests();
    }
  }, [user]);

  // Socket event listeners
  useEffect(() => {
    if (!socket) return;

    socket.on('friend_request_received', (data) => {
      showToast(`👋 Friend request from ${data.sender_username}`, 'info');
      loadFriendRequests();
    });

    socket.on('friend_request_accepted', (data) => {
      showToast(`✅ ${data.accepter_username} accepted your friend request!`, 'success');
    });

    socket.on('contacts_updated', (data) => {
      setContacts(data.contacts);
      
      // Update selected contact's online status if they're currently selected
      if (selectedContact) {
        const updatedContact = data.contacts.find(c => c.id === selectedContact.id);
        if (updatedContact) {
          setSelectedContact(updatedContact);
        } else {
          // Contact was removed
          setSelectedContact(null);
        }
      }
    });

    socket.on('contact_removed', (data) => {
      showToast(`${data.removed_by_username} removed you from their contacts`, 'info');
      
      if (selectedContact && selectedContact.id === data.removed_by_id) {
        setSelectedContact(null);
      }
    });

    return () => {
      socket.off('friend_request_received');
      socket.off('friend_request_accepted');
      socket.off('contacts_updated');
      socket.off('contact_removed');
    };
  }, [socket, selectedContact]);

  const loadContacts = async () => {
    try {
      const response = await axios.get('/api/contacts');
      setContacts(response.data.contacts);
    } catch (error) {
      console.error('Failed to load contacts:', error);
    }
  };

  const loadFriendRequests = async () => {
    try {
      const response = await axios.get('/api/friend-requests/pending');
      setFriendRequests(response.data.requests);
    } catch (error) {
      console.error('Failed to load friend requests:', error);
    }
  };

  const showToast = (message, type = 'info') => {
    setToast({ show: true, message, type });
  };

  const hideToast = () => {
    setToast({ ...toast, show: false });
  };

  return (
    <div className="chat-container">
      <Sidebar
        user={user}
        contacts={contacts}
        friendRequests={friendRequests}
        selectedContact={selectedContact}
        onSelectContact={setSelectedContact}
        onLogout={logout}
        onLoadContacts={loadContacts}
        onLoadFriendRequests={loadFriendRequests}
        onShowToast={showToast}
      />
      
      <ChatWindow
        selectedContact={selectedContact}
        onShowToast={showToast}
        onContactRemoved={() => {
          setSelectedContact(null);
          loadContacts();
        }}
      />

      {toast.show && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={hideToast}
        />
      )}
    </div>
  );
}

export default Chat;

