import React, { useState, useEffect } from 'react';
import { Search, Book, Crown, Heart, Shield, Star, Zap, Scale, Home, ChevronLeft, ChevronRight, AlertCircle } from 'lucide-react';
import { fetchThemes } from '../utils/api';
import '../styles/ThemeExplorer.css';

const themeIcons = {
  covenant: Book,
  kingdom: Crown,
  sacrifice: Heart,
  redemption: Shield,
  messiah: Star,
  faith: Zap,
  justice: Scale,
  temple: Home
};

const ThemeExplorer = ({ selectedTheme, onThemeSelect }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [themes, setThemes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadThemes = async () => {
      try {
        setLoading(true);
        const data = await fetchThemes();
        setThemes(data);
      } catch (err) {
        console.error('Failed to load themes:', err);
        setError('Failed to load themes. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    loadThemes();
  }, []);

  const filteredThemes = themes.filter(theme =>
    theme.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    theme.description.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading themes...</p>
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
    <div className={`theme-explorer ${isCollapsed ? 'collapsed' : ''}`}>
      <button 
        className="collapse-toggle"
        onClick={() => setIsCollapsed(!isCollapsed)}
        title={isCollapsed ? 'Expand Theme Explorer' : 'Collapse Theme Explorer'}
      >
        {isCollapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
      </button>

      <div className="theme-explorer-content">
        <div className="theme-explorer-header">
          <h2>Theme Explorer</h2>
          <p>Discover biblical themes and their narrative arcs</p>
        </div>

        <div className="search-container">
          <Search size={20} className="search-icon" />
          <input
            type="text"
            placeholder="Search themes..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>

        <div className="themes-list">
          {filteredThemes.map(theme => {
            const IconComponent = themeIcons[theme.id] || Book;
            const isSelected = selectedTheme?.id === theme.id;
            
            return (
              <div
                key={theme.id}
                className={`theme-item ${isSelected ? 'selected' : ''}`}
                onClick={() => onThemeSelect(isSelected ? null : theme)}
                style={{
                  borderLeftColor: theme.color,
                  backgroundColor: isSelected ? `${theme.color}10` : 'transparent'
                }}
              >
                <div className="theme-icon" style={{ color: theme.color }}>
                  <IconComponent size={24} />
                </div>
                <div className="theme-content">
                  <h3 className="theme-name">{theme.name}</h3>
                  <p className="theme-description">{theme.description}</p>
                </div>
                {isSelected && (
                  <div className="theme-selected-indicator" style={{ backgroundColor: theme.color }} />
                )}
              </div>
            );
          })}
        </div>

        {selectedTheme && (
          <div className="selected-theme-info">
            <div className="info-header" style={{ borderTopColor: selectedTheme.color }}>
              <h4>Active Theme</h4>
            </div>
            <div className="info-content">
              <h5>{selectedTheme.name}</h5>
              <p>{selectedTheme.description}</p>
              <button 
                className="clear-selection"
                onClick={() => onThemeSelect(null)}
              >
                Clear Selection
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ThemeExplorer;