import { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Configure axios defaults - use current domain when deployed
  axios.defaults.baseURL = window.location.origin;
  axios.defaults.withCredentials = true;

  useEffect(() => {
    // Check if user is already logged in (session exists)
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      // Try to access a protected endpoint
      const response = await axios.get('/api/contacts');
      if (response.status === 200) {
        // User is logged in
        const username = localStorage.getItem('username');
        setUser({ username });
      }
    } catch (error) {
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const login = async (username, password) => {
    try {
      const response = await axios.post('/api/login', {
        username,
        password
      });

      
      if (response.status === 200 && response.data.message) {
        setUser({ username });
        localStorage.setItem('username', username);
        return { success: true };
      }
      
      return { success: false, error: 'Invalid credentials' };
    } catch (error) {
      console.error('Login error:', error);
      return { 
        success: false, 
        error: error.response?.data?.error || 'Invalid credentials'
      };
    }
  };

  const signup = async (username, password) => {
    try {
      const response = await axios.post('/api/signup', {
        username,
        password
      });

      if (response.status === 201 && response.data.message) {
        return { success: true };
      }
      
      return { success: false, error: 'Signup failed' };
    } catch (error) {
      console.error('Signup error:', error);
      return { 
        success: false, 
        error: error.response?.data?.error || 'Username already taken'
      };
    }
  };

  const logout = async () => {
    try {
      await axios.get('/logout');
      setUser(null);
      localStorage.removeItem('username');
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  const value = {
    user,
    loading,
    login,
    signup,
    logout
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

