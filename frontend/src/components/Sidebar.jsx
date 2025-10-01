import { useState, useEffect } from 'react';
import axios from 'axios';
import './Sidebar.css';

function Sidebar({ 
  user, 
  contacts, 
  friendRequests, 
  selectedContact, 
  onSelectContact, 
  onLogout,
  onLoadContacts,
  onLoadFriendRequests,
  onShowToast 
}) {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [searchTimeout, setSearchTimeout] = useState(null);

  // Debounced user search
  useEffect(() => {
    if (searchTimeout) {
      clearTimeout(searchTimeout);
    }

    if (searchQuery.length >= 2) {
      const timeout = setTimeout(async () => {
        try {
          const response = await axios.get(`/api/users/search?q=${encodeURIComponent(searchQuery)}`);
          setSearchResults(response.data.users);
          setShowDropdown(response.data.users.length > 0);
        } catch (error) {
          console.error('Search error:', error);
        }
      }, 300);

      setSearchTimeout(timeout);
    } else {
      setSearchResults([]);
      setShowDropdown(false);
    }

    return () => {
      if (searchTimeout) clearTimeout(searchTimeout);
    };
  }, [searchQuery]);

  const sendFriendRequest = async (username) => {
    try {
      const response = await axios.post('/api/friend-requests/send', { username });
      onShowToast(`✅ Friend request sent to ${username}`, 'success');
      setSearchQuery('');
      setShowDropdown(false);
    } catch (error) {
      onShowToast(`❌ ${error.response?.data?.error || 'Failed to send request'}`, 'error');
    }
  };

  const acceptFriendRequest = async (requestId, username) => {
    try {
      await axios.post('/api/friend-requests/accept', { request_id: requestId });
      onShowToast(`✅ You and ${username} are now friends!`, 'success');
      onLoadFriendRequests();
      onLoadContacts();
    } catch (error) {
      onShowToast('❌ Failed to accept request', 'error');
    }
  };

  const rejectFriendRequest = async (requestId) => {
    try {
      await axios.post('/api/friend-requests/reject', { request_id: requestId });
      onShowToast('Friend request rejected', 'info');
      onLoadFriendRequests();
    } catch (error) {
      onShowToast('❌ Failed to reject request', 'error');
    }
  };

  return (
    <div className="sidebar">
      {/* Header */}
      <div className="sidebar-header">
        <div>
          <h2>💬 Chat Room</h2>
          <div className="username">{user?.username}</div>
        </div>
        <button className="logout-btn" onClick={onLogout} title="Logout">
          🚪
        </button>
      </div>

      {/* User Search */}
      <div className="add-contact">
        <input
          type="text"
          placeholder="🔍 Search users to add..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onFocus={() => searchResults.length > 0 && setShowDropdown(true)}
          onBlur={() => setTimeout(() => setShowDropdown(false), 200)}
        />
        {showDropdown && (
          <div className="autocomplete-dropdown">
            {searchResults.map((user) => (
              <div
                key={user.id}
                className="autocomplete-item"
                onClick={() => sendFriendRequest(user.username)}
              >
                <strong>{user.username}</strong>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Friend Requests */}
      {friendRequests.length > 0 && (
        <div className="friend-requests">
          <div className="friend-requests-header">
            Friend Requests
            <span className="request-badge">{friendRequests.length}</span>
          </div>
          {friendRequests.map((request) => (
            <div key={request.id} className="request-item">
              <div className="request-username">{request.sender_username}</div>
              <div className="request-actions">
                <button
                  className="btn-accept"
                  onClick={() => acceptFriendRequest(request.id, request.sender_username)}
                  title="Accept"
                >
                  ✓
                </button>
                <button
                  className="btn-reject"
                  onClick={() => rejectFriendRequest(request.id)}
                  title="Reject"
                >
                  ✗
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Contacts List */}
      <div className="contacts-list">
        {contacts.length === 0 ? (
          <div className="empty-contacts">
            No contacts yet. Add someone to start chatting!
          </div>
        ) : (
          contacts.map((contact) => (
            <div
              key={contact.id}
              className={`contact-item ${selectedContact?.id === contact.id ? 'active' : ''}`}
              onClick={() => onSelectContact(contact)}
            >
              <div className="contact-name">{contact.username}</div>
              <div className={`contact-status ${contact.online ? 'online' : ''}`}>
                {contact.online ? 'Online' : 'Offline'}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Sidebar;

