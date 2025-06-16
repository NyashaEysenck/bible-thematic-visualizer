import React, { useState } from 'react';
import Timeline from './components/Timeline';
import ThemeExplorer from './components/ThemeExplorer';
import InsightPanel from './components/InsightPanel';
import './App.css';

function App() {
  const [selectedTheme, setSelectedTheme] = useState(null);
  const [selectedBook, setSelectedBook] = useState(null);

  const handleThemeSelect = (theme) => {
    setSelectedTheme(theme);
    // Clear book selection when changing themes for better UX
    if (!theme) {
      setSelectedBook(null);
    }
  };

  const handleBookSelect = (book) => {
    setSelectedBook(book);
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1 className="app-title">Scripture Threads</h1>
          <p className="app-subtitle">Visualize Biblical Themes Across the Sacred Timeline</p>
        </div>
      </header>
      
      <main className="app-main">
        <div className="theme-explorer-container">
          <ThemeExplorer 
            selectedTheme={selectedTheme}
            onThemeSelect={handleThemeSelect}
          />
        </div>
        
        <div className="timeline-container">
          <Timeline 
            selectedTheme={selectedTheme}
            selectedBook={selectedBook}
            onBookSelect={handleBookSelect}
          />
        </div>
        
        <div className="insight-panel-container">
          <InsightPanel 
            selectedBook={selectedBook}
            selectedTheme={selectedTheme}
          />
        </div>
      </main>
    </div>
  );
}

export default App;