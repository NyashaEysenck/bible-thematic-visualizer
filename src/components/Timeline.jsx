import React, { useState, useEffect } from 'react';
import ThemeArc from './ThemeArc';
import { fetchBooks, fetchThemeConnections } from '../utils/api';
import { AlertCircle } from 'lucide-react';
import '../styles/Timeline.css';

const Timeline = ({ selectedTheme, onBookSelect, selectedBook }) => {
  const [books, setBooks] = useState([]);
  const [connections, setConnections] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Load books on component mount
  useEffect(() => {
    const loadBooks = async () => {
      try {
        setLoading(true);
        const data = await fetchBooks();
        setBooks(data);
      } catch (err) {
        console.error('Failed to load books:', err);
        setError('Failed to load books. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    loadBooks();
  }, []);

  // Load theme connections when theme changes
  useEffect(() => {
    const loadConnections = async () => {
      if (!selectedTheme) {
        setConnections({});
        return;
      }

      try {
        const data = await fetchThemeConnections(selectedTheme.id);
        const connectionsMap = {};
        data.forEach(conn => {
          connectionsMap[conn.bookId] = conn;
        });
        setConnections(connectionsMap);
      } catch (err) {
        console.error('Failed to load theme connections:', err);
        setError('Failed to load theme connections. Please try again later.');
      }
    };

    loadConnections();
  }, [selectedTheme]);

  const getBookConnections = (bookId, themeId) => {
    if (!themeId) return null;
    return connections[bookId] || null;
  };

  // Split books into Old and New Testament
  const oldTestamentBooks = books.filter(book => book.testament === 'old');
  const newTestamentBooks = books.filter(book => book.testament === 'new');

  if (loading && books.length === 0) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading timeline...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <AlertCircle size={24} className="error-icon" />
        <p className="error-message">{error}</p>
        <button onClick={() => window.location.reload()} className="retry-button">
          Retry
        </button>
      </div>
    );
  }

  const renderBookGrid = (books, testament) => (
    <div className="timeline-track">
      {books.map((book) => {
        const connection = getBookConnections(book.id, selectedTheme?.id);
        const isConnected = !!connection;
        const isSelected = selectedBook?.id === book.id;
        
        return (
          <div
            key={book.id}
            className={`book-segment ${book.testament} ${isConnected ? 'connected' : ''} ${isSelected ? 'selected' : ''}`}
            data-category={book.category}
            onClick={() => onBookSelect(book)}
            title={`${book.name} - ${book.category}${connection ? ` (Theme Prominence: ${connection.prominence}/5)` : ''}`}
            style={{
              '--theme-color': selectedTheme?.color || '#3b82f6',
              '--theme-arc-color': selectedTheme?.arcColor || '#60a5fa'
            }}
          >
            <div className="book-category">{book.category}</div>
            <div className="book-name">{book.name}</div>
            {isConnected && connection?.prominence && (
              <div className="prominence-indicator">
                {[1, 2, 3, 4, 5].map(dot => (
                  <div
                    key={dot}
                    className={`prominence-dot ${dot <= connection.prominence ? 'active' : ''}`}
                    style={{
                      backgroundColor: dot <= connection.prominence ? selectedTheme?.color : '#e5e7eb'
                    }}
                  />
                ))}
              </div>
            )}
            {isConnected && (
              <div 
                className="connection-indicator"
                style={{ backgroundColor: selectedTheme?.color }}
              />
            )}
          </div>
        );
      })}
    </div>
  );

  return (
    <div className="timeline-container">
      <div className="timeline-header">
        <h2>Biblical Timeline</h2>
        <div className="timeline-stats">
          <span className="book-count">66 Books</span>
          <div className="testament-labels">
            <span className="testament-label old">Old Testament (39)</span>
            <span className="testament-label new">New Testament (27)</span>
          </div>
        </div>
      </div>
      
      <div className="timeline-content">
        {/* Theme Arc Overlay */}
        {selectedTheme && (
          <ThemeArc 
            books={books}
            selectedTheme={selectedTheme}
            connections={Object.values(connections)}
          />
        )}
        
        <div className="testament-section">
          <h3 className="testament-title old">Old Testament</h3>
          {renderBookGrid(oldTestamentBooks, 'old')}
        </div>
        
        <div className="testament-divider">
          <div className="divider-line"></div>
          <div className="divider-label">Testament Divide</div>
          <div className="divider-line"></div>
        </div>
        
        <div className="testament-section">
          <h3 className="testament-title new">New Testament</h3>
          {renderBookGrid(newTestamentBooks, 'new')}
        </div>
      </div>
    </div>
  );
};

export default Timeline;