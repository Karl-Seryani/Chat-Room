import { useEffect } from 'react';
import './Toast.css';

function Toast({ message, type = 'info', onClose }) {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose();
    }, 3000);

    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <div className={`toast ${type} show`}>
      <div className="toast-content">
        {type === 'success' && '✅ '}
        {type === 'error' && '❌ '}
        {type === 'info' && 'ℹ️ '}
        {message}
      </div>
      <button className="toast-close" onClick={onClose}>
        ×
      </button>
    </div>
  );
}

export default Toast;

