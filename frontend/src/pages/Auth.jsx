import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Auth.css';

function Auth() {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const { login, signup } = useAuth();
  const navigate = useNavigate();

  // Audio context for horror sounds
  const audioContextRef = useRef(null);
  const ambienceRef = useRef(null);

  // Create eerie ambient sound using Web Audio API
  useEffect(() => {
    // Create audio context
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    const audioContext = new AudioContext();
    audioContextRef.current = audioContext;

    // Create ambient horror drone
    const createAmbience = () => {
      const oscillator1 = audioContext.createOscillator();
      const oscillator2 = audioContext.createOscillator();
      const oscillator3 = audioContext.createOscillator();
      const gainNode = audioContext.createGain();
      const filter = audioContext.createBiquadFilter();

      // Low frequency horror drone
      oscillator1.type = 'sine';
      oscillator1.frequency.setValueAtTime(55, audioContext.currentTime); // Deep A note

      oscillator2.type = 'triangle';
      oscillator2.frequency.setValueAtTime(110, audioContext.currentTime);

      oscillator3.type = 'sawtooth';
      oscillator3.frequency.setValueAtTime(73.42, audioContext.currentTime); // D note (dissonant)

      // Low pass filter for murkiness
      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(400, audioContext.currentTime);
      filter.Q.setValueAtTime(5, audioContext.currentTime);

      // Very quiet ambient volume
      gainNode.gain.setValueAtTime(0, audioContext.currentTime);
      gainNode.gain.linearRampToValueAtTime(0.03, audioContext.currentTime + 2);

      // Connect nodes
      oscillator1.connect(filter);
      oscillator2.connect(filter);
      oscillator3.connect(filter);
      filter.connect(gainNode);
      gainNode.connect(audioContext.destination);

      // Start oscillators
      oscillator1.start();
      oscillator2.start();
      oscillator3.start();

      // Slowly modulate for eerie effect
      const lfo = audioContext.createOscillator();
      const lfoGain = audioContext.createGain();
      lfo.frequency.setValueAtTime(0.1, audioContext.currentTime);
      lfoGain.gain.setValueAtTime(20, audioContext.currentTime);
      lfo.connect(lfoGain);
      lfoGain.connect(filter.frequency);
      lfo.start();

      return { oscillator1, oscillator2, oscillator3, lfo };
    };

    // Delay ambience start slightly
    const timer = setTimeout(() => {
      ambienceRef.current = createAmbience();
    }, 500);

    // Cleanup
    return () => {
      clearTimeout(timer);
      if (ambienceRef.current) {
        const { oscillator1, oscillator2, oscillator3, lfo } = ambienceRef.current;
        oscillator1.stop();
        oscillator2.stop();
        oscillator3.stop();
        lfo.stop();
      }
      if (audioContextRef.current) {
        audioContextRef.current.close();
      }
    };
  }, []);

  // Play creepy whisper sound on hover
  const playWhisper = () => {
    if (!audioContextRef.current) return;

    const audioContext = audioContextRef.current;
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    const filter = audioContext.createBiquadFilter();

    oscillator.type = 'sine';
    oscillator.frequency.setValueAtTime(200, audioContext.currentTime);

    filter.type = 'bandpass';
    filter.frequency.setValueAtTime(1000, audioContext.currentTime);
    filter.Q.setValueAtTime(10, audioContext.currentTime);

    gainNode.gain.setValueAtTime(0, audioContext.currentTime);
    gainNode.gain.linearRampToValueAtTime(0.05, audioContext.currentTime + 0.05);
    gainNode.gain.linearRampToValueAtTime(0, audioContext.currentTime + 0.2);

    oscillator.connect(filter);
    filter.connect(gainNode);
    gainNode.connect(audioContext.destination);

    oscillator.start();
    oscillator.stop(audioContext.currentTime + 0.2);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    if (!username || !password) {
      setError('Please fill in all fields');
      setLoading(false);
      return;
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters');
      setLoading(false);
      return;
    }

    try {
      let result;
      
      if (isLogin) {
        result = await login(username, password);
        if (result.success) {
          navigate('/chat');
        } else {
          setError(result.error || 'Invalid username or password');
        }
      } else {
        result = await signup(username, password);
        if (result.success) {
          setIsLogin(true);
          setError('');
          setPassword('');
          alert('Account created successfully! Please log in.');
        } else {
          setError(result.error || 'Username already taken');
        }
      }
    } catch (err) {
      setError('An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h1>Whisper</h1>
          <p>{isLogin ? 'Welcome back!' : 'Create your account'}</p>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter your username"
              autoComplete="username"
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              autoComplete={isLogin ? 'current-password' : 'new-password'}
              disabled={loading}
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <button type="submit" className="auth-button" disabled={loading}>
            {loading ? 'Processing...' : (isLogin ? 'Login' : 'Sign Up')}
          </button>
        </form>

        <div className="auth-toggle">
          {isLogin ? "Don't have an account? " : "Already have an account? "}
          <button
            type="button"
            onClick={() => {
              setIsLogin(!isLogin);
              setError('');
              setPassword('');
            }}
            disabled={loading}
          >
            {isLogin ? 'Sign Up' : 'Login'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default Auth;

