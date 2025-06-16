import React, { useState, useEffect } from 'react';
import { BookOpen, ChevronDown, ChevronUp, Info, X, Loader2 } from 'lucide-react';
import { fetchChapters, fetchVerses, fetchVerseExplanation } from '../utils/api';
import '../styles/BibleReader.css';

const BibleReader = ({ book }) => {
  const [chapters, setChapters] = useState([]);
  const [expandedChapters, setExpandedChapters] = useState({});
  const [verses, setVerses] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedVerse, setSelectedVerse] = useState(null);
  const [explanation, setExplanation] = useState(null);
  const [explanationLoading, setExplanationLoading] = useState(false);
  const [explanationError, setExplanationError] = useState(null);

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

  const handleVerseClick = async (chapterNumber, verseNumber) => {
    if (!book) return;
    
    setSelectedVerse({ chapter: chapterNumber, verse: verseNumber });
    setExplanationLoading(true);
    setExplanationError(null);
    
    try {
      const response = await fetchVerseExplanation(book, chapterNumber, verseNumber);
      setExplanation(response.explanation);
    } catch (err) {
      console.error('Failed to fetch explanation:', err);
      setExplanationError('Failed to load explanation. Please try again.');
    } finally {
      setExplanationLoading(false);
    }
  };

  const closeExplanation = () => {
    setSelectedVerse(null);
    setExplanation(null);
    setExplanationError(null);
  };

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
                      <div 
                        key={verse.verse} 
                        className="verse"
                        onClick={() => handleVerseClick(chapter.number, verse.verse)}
                      >
                        <div className="verse-header">
                          <span className="verse-number">{verse.verse}.</span>
                          <button 
                            className="verse-info-button"
                            onClick={(e) => {
                              e.stopPropagation();
                              handleVerseClick(chapter.number, verse.verse);
                            }}
                            aria-label="View explanation"
                          >
                            <Info size={16} />
                          </button>
                        </div>
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

      {/* Verse Explanation Modal */}
      {selectedVerse && (
        <div className="verse-explanation-modal">
          <div className="verse-explanation-content">
            <div className="verse-explanation-header">
              <h3>{book} {selectedVerse.chapter}:{selectedVerse.verse}</h3>
              <button className="close-button" onClick={closeExplanation}>
                <X size={20} />
              </button>
            </div>
            <div className="verse-explanation-body">
              {explanationLoading ? (
                <div className="loading-container">
                  <Loader2 className="spinner" size={24} />
                  <p>Loading explanation...</p>
                </div>
              ) : explanationError ? (
                <div className="error-message">
                  <AlertCircle size={16} />
                  <p>{explanationError}</p>
                </div>
              ) : (
                <div className="explanation-text" dangerouslySetInnerHTML={{ __html: explanation?.replace(/\n/g, '<br />') }} />
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default BibleReader;
