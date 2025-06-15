import React from 'react';

const ThemeArc = ({ books, selectedTheme, connections }) => {
  if (!selectedTheme || !connections || connections.length === 0) {
    return null;
  }

  // Filter and sort connected books by their biblical order (book.id)
  const connectedBooks = books
    .filter(book => connections.some(conn => conn.bookId === book.id))
    .map(book => {
      const connection = connections.find(conn => conn.bookId === book.id);
      return { ...book, connection };
    })
    .sort((a, b) => a.id - b.id); // Sort by biblical order

  if (connectedBooks.length < 2) return null;

  // Calculate positions for each book
  const getBookPosition = (book) => {
    const bookElements = document.querySelectorAll('.book-segment');
    const bookElement = Array.from(bookElements).find(el => 
      el.getAttribute('title')?.includes(book.name)
    );
    
    if (!bookElement) return null;
    
    const rect = bookElement.getBoundingClientRect();
    const containerRect = bookElement.closest('.timeline-content').getBoundingClientRect();
    
    return {
      x: rect.left - containerRect.left + rect.width / 2,
      y: rect.top - containerRect.top + rect.height / 2
    };
  };

  // Get positions for all connected books in chronological order
  const positions = connectedBooks
    .map(book => ({ book, position: getBookPosition(book) }))
    .filter(item => item.position !== null);

  if (positions.length < 2) return null;

  // Create smooth path through points in chronological order
  const createSmoothPath = (points) => {
    if (points.length < 2) return '';

    // Use points in their chronological order (already sorted)
    let path = `M ${points[0].position.x} ${points[0].position.y}`;
    
    for (let i = 1; i < points.length; i++) {
      const current = points[i].position;
      const previous = points[i - 1].position;
      
      // Create smooth curves between consecutive points
      const dx = current.x - previous.x;
      const dy = current.y - previous.y;
      
      // Control points for smooth curves
      const controlPointOffset = Math.min(Math.abs(dx) * 0.4, 100);
      const cp1x = previous.x + (dx > 0 ? controlPointOffset : -controlPointOffset);
      const cp1y = previous.y + dy * 0.2;
      const cp2x = current.x - (dx > 0 ? controlPointOffset : -controlPointOffset);
      const cp2y = current.y - dy * 0.2;
      
      path += ` C ${cp1x} ${cp1y}, ${cp2x} ${cp2y}, ${current.x} ${current.y}`;
    }
    
    return path;
  };

  // Find testament transition point
  const oldTestamentBooks = positions.filter(p => p.book.testament === 'old');
  const newTestamentBooks = positions.filter(p => p.book.testament === 'new');
  
  // Create gradient based on testament progression
  const gradientId = `theme-gradient-${selectedTheme.id}`;
  const oldTestamentColor = selectedTheme.color;
  const newTestamentColor = selectedTheme.arcColor || '#fbbf24';
  
  // Calculate gradient stops based on testament transition
  let gradientStops = [
    { offset: "0%", color: oldTestamentColor },
    { offset: "100%", color: oldTestamentColor }
  ];
  
  if (oldTestamentBooks.length > 0 && newTestamentBooks.length > 0) {
    const transitionPoint = (oldTestamentBooks.length / positions.length) * 100;
    gradientStops = [
      { offset: "0%", color: oldTestamentColor },
      { offset: `${Math.max(transitionPoint - 10, 0)}%`, color: oldTestamentColor },
      { offset: `${Math.min(transitionPoint + 10, 100)}%`, color: newTestamentColor },
      { offset: "100%", color: newTestamentColor }
    ];
  } else if (newTestamentBooks.length > 0) {
    gradientStops = [
      { offset: "0%", color: newTestamentColor },
      { offset: "100%", color: newTestamentColor }
    ];
  }

  return (
    <svg 
      className="theme-arc-overlay"
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        pointerEvents: 'none',
        zIndex: 5
      }}
    >
      <defs>
        <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="0%">
          {gradientStops.map((stop, index) => (
            <stop 
              key={index}
              offset={stop.offset} 
              stopColor={stop.color} 
              stopOpacity="0.8" 
            />
          ))}
        </linearGradient>
        
        {/* Glow effect */}
        <filter id={`glow-${selectedTheme.id}`}>
          <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
          <feMerge> 
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
      </defs>

      {/* Main arc path connecting books in chronological order */}
      <path
        d={createSmoothPath(positions)}
        fill="none"
        stroke={`url(#${gradientId})`}
        strokeWidth="4"
        strokeLinecap="round"
        strokeLinejoin="round"
        filter={`url(#glow-${selectedTheme.id})`}
        className="theme-arc-path"
      />

      {/* Connection nodes at each book position */}
      {positions.map(({ book, position }, index) => {
        const nodeColor = book.testament === 'old' ? oldTestamentColor : newTestamentColor;
        
        return (
          <g key={book.id}>
            {/* Outer glow circle */}
            <circle
              cx={position.x}
              cy={position.y}
              r="12"
              fill={nodeColor}
              opacity="0.2"
              className="theme-node-glow"
            />
            
            {/* Main node */}
            <circle
              cx={position.x}
              cy={position.y}
              r="6"
              fill={nodeColor}
              stroke="white"
              strokeWidth="2"
              className="theme-node"
              style={{ animationDelay: `${index * 0.2}s` }}
            />
            
            {/* Prominence indicator */}
            <circle
              cx={position.x}
              cy={position.y}
              r="3"
              fill="white"
              opacity={book.connection.prominence / 5}
              className="theme-node-prominence"
              style={{ animationDelay: `${index * 0.2}s` }}
            />
          </g>
        );
      })}

      {/* Testament transition indicator - only show if we have both testaments */}
      {oldTestamentBooks.length > 0 && newTestamentBooks.length > 0 && (
        (() => {
          // Find the last OT book and first NT book in our connected sequence
          const lastOTIndex = positions.findIndex(p => p.book.testament === 'new') - 1;
          const firstNTIndex = lastOTIndex + 1;
          
          if (lastOTIndex >= 0 && firstNTIndex < positions.length) {
            const lastOT = positions[lastOTIndex];
            const firstNT = positions[firstNTIndex];
            const midX = (lastOT.position.x + firstNT.position.x) / 2;
            const midY = (lastOT.position.y + firstNT.position.y) / 2;
            
            return (
              <g className="testament-transition">
                <circle
                  cx={midX}
                  cy={midY}
                  r="8"
                  fill="none"
                  stroke={newTestamentColor}
                  strokeWidth="2"
                  strokeDasharray="4,4"
                  opacity="0.6"
                  className="testament-bridge"
                >
                  <animate
                    attributeName="stroke-dashoffset"
                    values="0;8"
                    dur="2s"
                    repeatCount="indefinite"
                  />
                </circle>
                <text
                  x={midX}
                  y={midY - 15}
                  textAnchor="middle"
                  fontSize="10"
                  fill={newTestamentColor}
                  fontWeight="600"
                  opacity="0.8"
                  className="testament-bridge"
                >
                  Fulfillment
                </text>
              </g>
            );
          }
          return null;
        })()
      )}
    </svg>
  );
};

export default ThemeArc;