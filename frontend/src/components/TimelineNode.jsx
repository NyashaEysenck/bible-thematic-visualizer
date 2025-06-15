import React from 'react';
import '../styles/TimelineNode.css';

const TimelineNode = ({ 
  book, 
  position, 
  total, 
  isConnected, 
  prominence, 
  isSelected, 
  theme,
  onClick 
}) => {
  const getNodeSize = () => {
    if (!isConnected) return 10;
    return 14 + (prominence * 3); // Size based on prominence (14-29px)
  };

  const getNodeColor = () => {
    if (isSelected) return theme?.color || '#3b82f6';
    if (!isConnected) return book.testament === 'old' ? '#93c5fd' : '#fed7aa';
    return theme?.color || '#60a5fa';
  };

  const getBorderColor = () => {
    if (isSelected) return theme?.color || '#3b82f6';
    if (!isConnected) return book.testament === 'old' ? '#3b82f6' : '#f59e0b';
    return theme?.arcColor || '#60a5fa';
  };

  return (
    <div
      className={`timeline-node ${isConnected ? 'connected' : ''} ${isSelected ? 'selected' : ''} ${book.testament}`}
      style={{
        width: `${getNodeSize()}px`,
        height: `${getNodeSize()}px`,
        backgroundColor: getNodeColor(),
        borderColor: getBorderColor(),
        zIndex: isSelected ? 20 : isConnected ? 15 : 10
      }}
      onClick={(e) => {
        e.stopPropagation();
        onClick();
      }}
      title={`${book.name} - ${book.category}${prominence ? ` (Theme Prominence: ${prominence}/5)` : ''}`}
    >
      {isConnected && (
        <div 
          className="node-pulse" 
          style={{ borderColor: theme?.arcColor || '#60a5fa' }} 
        />
      )}
      {isSelected && (
        <div 
          className="node-glow" 
          style={{ backgroundColor: theme?.color || '#3b82f6' }} 
        />
      )}
    </div>
  );
};

export default TimelineNode;