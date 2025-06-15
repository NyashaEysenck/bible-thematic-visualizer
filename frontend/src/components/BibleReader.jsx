import React, { useState, useEffect } from 'react';
import { BookOpen, ChevronDown, ChevronUp } from 'lucide-react';
import { fetchChapters, fetchVerses } from '../utils/api';
import '../styles/BibleReader.css';

const BibleReader = ({ book }) => {
  const [chapters, setChapters] = useState([]);
  const [expandedChapters, setExpandedChapters] = useState({});
  const [verses, setVerses] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load chapters when book changes
  useEffect(() => {
    const loadChapters = async () => {
      if (!book) {
        setChapters([]);
        return;
      }

      try {
        setLoading(true);
        setError(null);
        const data = await fetchChapters(book);
        setChapters(data);
        
        // Initialize expanded state for chapters
        const initialExpanded = {};
        data.forEach(chapter => {
          initialExpanded[chapter.number] = false;
        });
        setExpandedChapters(initialExpanded);
      } catch (err) {
        console.error('Failed to load chapters:', err);
        setError('Failed to load chapters. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    loadChapters();
  }, [book]);

  const toggleChapter = async (chapterNumber) => {
    // Toggle chapter expansion
    const newExpandedState = {
      ...expandedChapters,
      [chapterNumber]: !expandedChapters[chapterNumber]
    };
    setExpandedChapters(newExpandedState);

    // If expanding and we don't have verses for this chapter, load them
    if (newExpandedState[chapterNumber] && !verses[chapterNumber]) {
      try {
        const chapterVerses = await fetchVerses(book, chapterNumber);
        setVerses(prev => ({
          ...prev,
          [chapterNumber]: chapterVerses
        }));
      } catch (err) {
        console.error('Failed to load verses:', err);
        setError('Failed to load verses. Please try again.');
      }
    }
  };

  if (loading && chapters.length === 0) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading Bible content...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <p className="error-message">{error}</p>
      </div>
    );
  }

  if (!book) {
    return (
      <div className="no-content-message">
        <BookOpen size={32} className="empty-icon" />
        <p>Select a book to start reading</p>
      </div>
    );
  }

  return (
    <div className="bible-reader">
      <div className="chapters-list">
        {chapters.map(chapter => (
          <div key={chapter.number} className="chapter-container">
            <div 
              className="chapter-header"
              onClick={() => toggleChapter(chapter.number)}
            >
              <h3>Chapter {chapter.number}</h3>
              {expandedChapters[chapter.number] ? 
                <ChevronUp size={20} /> : 
                <ChevronDown size={20} />
              }
            </div>
            
            {expandedChapters[chapter.number] && (
              <div className="verses-container">
                {verses[chapter.number] ? (
                  <div className="verses-grid">
                    {verses[chapter.number].map(verse => (
                      <div key={verse.verse} className="verse">
                        <span className="verse-number">{verse.verse}.</span>
                        <span className="verse-text">{verse.text}</span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="loading-verse">Loading verses...</div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default BibleReader;
