import React, { useState, useEffect } from 'react';
import { Book, FileText, GraduationCap, AlertCircle, ChevronRight, ChevronLeft, X, Loader2 } from 'lucide-react';
import { fetchBookInsights, fetchThemeConnections, fetchEventExplanation } from '../utils/api';
import '../styles/InsightPanel.css';

const InsightPanel = ({ selectedBook, selectedTheme }) => {
  const [activeTab, setActiveTab] = useState('overview');
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [insights, setInsights] = useState(null);
  const [themeConnection, setThemeConnection] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [explanation, setExplanation] = useState(null);
  const [explanationLoading, setExplanationLoading] = useState(false);
  const [explanationError, setExplanationError] = useState(null);

  // Load book insights when selected book changes
  useEffect(() => {
    const loadInsights = async () => {
      if (!selectedBook) {
        setInsights(null);
        return;
      }

      try {
        setLoading(true);
        setError(null);
        const data = await fetchBookInsights(selectedBook.id);
        setInsights(data);
      } catch (err) {
        console.error('Failed to load book insights:', err);
        setError('Failed to load book insights. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    loadInsights();
  }, [selectedBook]);

  // Load theme connection when selected theme or book changes
  useEffect(() => {
    const loadThemeConnection = async () => {
      if (!selectedTheme || !selectedBook) {
        setThemeConnection(null);
        return;
      }

      try {
        const connections = await fetchThemeConnections(selectedTheme.id);
        const connection = connections.find(conn => conn.bookId === selectedBook.id) || null;
        setThemeConnection(connection);
      } catch (err) {
        console.error('Failed to load theme connection:', err);
        setThemeConnection(null);
      }
    };

    loadThemeConnection();
  }, [selectedTheme, selectedBook]);

  const tabs = [
    { id: 'overview', label: 'Book Overview', icon: Book },
    { id: 'scriptures', label: 'Key Scriptures', icon: FileText },
    { id: 'theology', label: 'Theological Context', icon: GraduationCap }
  ];

  const handleEventClick = async (event) => {
    if (!selectedBook || !selectedTheme) return;
    
    setSelectedEvent(event);
    setExplanationLoading(true);
    setExplanationError(null);
    
    try {
      const response = await fetchEventExplanation(
        selectedBook.name,
        event,
        selectedTheme.name
      );
      setExplanation(response.explanation);
    } catch (err) {
      console.error('Failed to fetch explanation:', err);
      setExplanationError('Failed to load explanation. Please try again.');
    } finally {
      setExplanationLoading(false);
    }
  };

  const closeExplanation = () => {
    setSelectedEvent(null);
    setExplanation(null);
    setExplanationError(null);
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading insights...</p>
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

  return (
    <div className={`insight-panel ${isCollapsed ? 'collapsed' : ''}`}>
      <button 
        className="collapse-toggle"
        onClick={() => setIsCollapsed(!isCollapsed)}
        title={isCollapsed ? 'Expand Insight Panel' : 'Collapse Insight Panel'}
      >
        {isCollapsed ? <ChevronLeft size={20} /> : <ChevronRight size={20} />}
      </button>

      <div className="insight-panel-content">
        {!selectedBook ? (
          <>
            <div className="insight-panel-header">
              <h2>Insight Panel</h2>
              <p>Select a book from the timeline to explore detailed insights</p>
            </div>
            <div className="empty-state">
              <Book size={48} className="empty-icon" />
              <h3>No Book Selected</h3>
              <p>Click on any book in the timeline to see its overview, key scriptures, and theological significance.</p>
            </div>
          </>
        ) : (
          <>
            <div className="insight-panel-header">
              <h2>{selectedBook.name}</h2>
              <div className="book-meta">
                <span className={`testament-badge ${selectedBook.testament}`}>
                  {selectedBook.testament === 'old' ? 'Old Testament' : 'New Testament'}
                </span>
                <span className="category-badge">{selectedBook.category}</span>
              </div>
              {selectedTheme && themeConnection && (
                <div className="theme-connection" style={{ borderLeftColor: selectedTheme.color }}>
                  <div className="connection-header">
                    <span className="theme-name" style={{ color: selectedTheme.color }}>
                      {selectedTheme.name}
                    </span>
                    <div className="prominence-indicator">
                      <span>Prominence: </span>
                      <div className="prominence-dots">
                        {[1, 2, 3, 4, 5].map(dot => (
                          <div
                            key={dot}
                            className={`prominence-dot ${dot <= themeConnection.prominence ? 'active' : ''}`}
                            style={{ backgroundColor: dot <= themeConnection.prominence ? selectedTheme.color : '#e5e7eb' }}
                          />
                        ))}
                      </div>
                    </div>
                  </div>
                  <div className="key-events">
                    <span>Key Events: </span>
                    <div className="event-tags">
                      {themeConnection.events.map((event, index) => (
                        <button
                          key={index}
                          className={`event-tag ${selectedEvent === event ? 'active' : ''}`}
                          onClick={() => handleEventClick(event)}
                          style={{
                            borderColor: selectedTheme.color,
                            color: selectedEvent === event ? '#fff' : selectedTheme.color,
                            backgroundColor: selectedEvent === event ? selectedTheme.color : 'transparent'
                          }}
                        >
                          {event}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>

            <div className="insight-tabs">
              {tabs.map(tab => {
                const IconComponent = tab.icon;
                return (
                  <button
                    key={tab.id}
                    className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
                    onClick={() => setActiveTab(tab.id)}
                  >
                    <IconComponent size={18} />
                    {tab.label}
                  </button>
                );
              })}
            </div>

            <div className="insight-content">
              {activeTab === 'overview' && (
                <div className="tab-content">
                  {loading ? (
                    <div className="loading-container">
                      <div className="loading-spinner"></div>
                      <p>Loading content...</p>
                    </div>
                  ) : insights ? (
                    <>
                      <h4>Book Overview</h4>
                      <p>{insights?.overview || `${selectedBook.name} is part of the ${selectedBook.category} section of the ${selectedBook.testament === 'old' ? 'Old' : 'New'} Testament.`}</p>
                    </>
                  ) : (
                    <p>Loading book overview...</p>
                  )}
                </div>
              )}

              {activeTab === 'scriptures' && (
                <div className="tab-content">
                  {loading ? (
                    <div className="loading-container">
                      <div className="loading-spinner"></div>
                      <p>Loading content...</p>
                    </div>
                  ) : insights ? (
                    <>
                      <h4>Key Scriptures</h4>
                      {insights.key_scriptures && insights.key_scriptures.length > 0 ? (
                        <div className="scripture-list">
                          {insights.key_scriptures.map((verse, index) => (
                            <div key={index} className="scripture-item">
                              <ChevronRight size={16} className="scripture-icon" />
                              <span className="scripture-reference">{verse}</span>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <p>No key scriptures available for {selectedBook.name}.</p>
                      )}
                    </>
                  ) : (
                    <p>Key scripture references for {selectedBook.name} would be displayed here based on the selected theme and theological focus.</p>
                  )}
                </div>
              )}

              {activeTab === 'theology' && (
                <div className="theology-content">
                  {insights?.theological_context || 'No theological context available for this book.'}
                </div>
              )}
            </div>

            {/* Event Explanation Modal */}
            {selectedEvent && (
              <div className="event-explanation-modal">
                <div className="event-explanation-content">
                  <div className="event-explanation-header">
                    <h3>Event Explanation: {selectedEvent}</h3>
                    <button className="close-button" onClick={closeExplanation}>
                      <X size={20} />
                    </button>
                  </div>
                  <div className="event-explanation-body">
                    {explanationLoading ? (
                      <div className="loading-container">
                        <Loader2 className="spinner" size={24} />
                        <p>Loading explanation...</p>
                      </div>
                    ) : explanationError ? (
                      <div className="error-message">
                        <AlertCircle size={20} />
                        <p>{explanationError}</p>
                      </div>
                    ) : (
                      <div className="explanation-text">
                        {explanation ? (
                          <p>{explanation}</p>
                        ) : (
                          <p>No explanation available for this event.</p>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default InsightPanel;