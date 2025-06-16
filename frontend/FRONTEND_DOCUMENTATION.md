# Scripture Threads - Frontend Documentation

## Overview

Scripture Threads is a modern React-based web application that provides an interactive visualization of biblical themes across scripture. The frontend is built with React 18, Vite, and modern CSS, offering a responsive and intuitive user experience for exploring biblical narratives and thematic connections.

## Table of Contents

- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Components](#components)
- [Styling System](#styling-system)
- [API Integration](#api-integration)
- [Responsive Design](#responsive-design)
- [Development Setup](#development-setup)
- [Build & Deployment](#build--deployment)

## Architecture

The application follows a modern React architecture with:

- **Component-based design**: Modular, reusable components
- **State management**: React hooks for local state management
- **API integration**: RESTful API communication with the FastAPI backend
- **Responsive layout**: CSS Grid and Flexbox for adaptive layouts
- **Modern styling**: Custom CSS with design system principles

### Core Application Flow

```
App.jsx (Root)
├── ThemeExplorer (Left Panel)
├── Timeline (Center Panel)
│   ├── ThemeArc (Overlay)
│   └── BibleReader (Expandable)
└── InsightPanel (Right Panel)
```

## Technology Stack

### Core Technologies
- **React 18.3.1**: Modern React with hooks and concurrent features
- **Vite 5.4.2**: Fast build tool and development server
- **JavaScript (ES6+)**: Modern JavaScript features

### UI & Styling
- **CSS3**: Custom CSS with modern features (Grid, Flexbox, Custom Properties)
- **Lucide React**: Modern icon library
- **Inter Font**: Professional typography

### Development Tools
- **ESLint**: Code linting and quality assurance
- **Vite Dev Server**: Hot module replacement and fast development

## Project Structure

```
frontend/
├── public/
│   └── vite.svg                    # Vite logo
├── src/
│   ├── components/                 # React components
│   │   ├── BibleReader.jsx        # Bible text reader with verse explanations
│   │   ├── InsightPanel.jsx       # Book insights and theme connections
│   │   ├── ThemeArc.jsx           # Visual theme connections overlay
│   │   ├── ThemeExplorer.jsx      # Theme selection and exploration
│   │   ├── Timeline.jsx           # Main biblical timeline visualization
│   │   └── TimelineNode.jsx       # Individual timeline nodes (legacy)
│   ├── data/                      # Static data files (legacy)
│   │   ├── biblicalBooks.js       # Bible books data
│   │   ├── bookInsights.js        # Book insights data
│   │   ├── themeConnections.js    # Theme connection mappings
│   │   └── themes.js              # Biblical themes data
│   ├── styles/                    # Component-specific CSS
│   │   ├── BibleReader.css        # Bible reader styling
│   │   ├── InsightPanel.css       # Insight panel styling
│   │   ├── ThemeExplorer.css      # Theme explorer styling
│   │   ├── Timeline.css           # Timeline visualization styling
│   │   └── TimelineNode.css       # Timeline node styling (legacy)
│   ├── utils/                     # Utility functions
│   │   └── api.js                 # API communication functions
│   ├── App.css                    # Global application styles
│   ├── App.jsx                    # Root application component
│   ├── index.css                  # Global CSS reset and utilities
│   └── main.jsx                   # Application entry point
├── eslint.config.js               # ESLint configuration
├── index.html                     # HTML template
├── package.json                   # Dependencies and scripts
└── vite.config.js                 # Vite configuration
```

## Components

### App.jsx (Root Component)
**Purpose**: Main application container and state management
**Key Features**:
- Global state management for selected theme and book
- Layout coordination between panels
- Event handling for theme and book selection

**State Management**:
```javascript
const [selectedTheme, setSelectedTheme] = useState(null);
const [selectedBook, setSelectedBook] = useState(null);
```

### ThemeExplorer.jsx
**Purpose**: Theme discovery and selection interface
**Key Features**:
- Search functionality for themes
- Theme list with descriptions and icons
- Collapsible panel design
- Active theme indication

**API Integration**:
- Fetches themes from `/api/v1/themes`
- Real-time search filtering
- Error handling and loading states

### Timeline.jsx
**Purpose**: Main biblical timeline visualization
**Key Features**:
- Grid-based book layout (Old/New Testament)
- Theme connection visualization
- Book selection handling
- Integrated Bible reader toggle
- Responsive grid system

**Visual Elements**:
- Testament sections with distinct styling
- Book prominence indicators
- Theme connection overlays
- Category-based color coding

### ThemeArc.jsx
**Purpose**: Visual theme connection overlay
**Key Features**:
- SVG-based arc rendering
- Smooth path interpolation between connected books
- Testament transition indicators
- Animated connection nodes
- Gradient color schemes

**Technical Implementation**:
- Dynamic SVG path generation
- CSS animations for visual effects
- Responsive positioning system

### InsightPanel.jsx
**Purpose**: Detailed book information and insights
**Key Features**:
- Tabbed interface (Overview, Scriptures, Theology)
- Theme connection details
- Event explanation modals
- Collapsible design

**Content Areas**:
- **Overview Tab**: Book summaries and context
- **Scriptures Tab**: Key verse references
- **Theology Tab**: Theological significance

### BibleReader.jsx
**Purpose**: Interactive Bible text reader
**Key Features**:
- Chapter/verse navigation
- Expandable chapter sections
- Verse-by-verse explanations
- AI-powered verse insights
- Modal explanation display

**User Interactions**:
- Click to expand chapters
- Click verses for explanations
- Smooth scrolling and navigation

## Styling System

### Design Principles
- **Modern Aesthetics**: Clean, professional design
- **Consistent Typography**: Inter font family throughout
- **Color System**: Semantic color usage with theme-based variations
- **Spacing System**: 8px grid-based spacing
- **Responsive Design**: Mobile-first approach

### CSS Architecture
```css
/* Global Variables */
:root {
  --color-primary: #3b82f6;
  --color-secondary: #f59e0b;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --border-radius: 8px;
  --shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
```

### Component Styling
- **Modular CSS**: Each component has its own CSS file
- **BEM-like naming**: Descriptive class names
- **Responsive breakpoints**: Mobile, tablet, desktop
- **Smooth animations**: CSS transitions and keyframes

### Key Design Features
- **Gradient backgrounds**: Subtle gradients for depth
- **Box shadows**: Layered shadow system
- **Hover effects**: Interactive feedback
- **Loading states**: Skeleton screens and spinners
- **Modal overlays**: Backdrop blur effects

## API Integration

### API Client (`utils/api.js`)
Centralized API communication with the FastAPI backend.

**Base Configuration**:
```javascript
const API_BASE_URL = import.meta.env.MODE === 'production' 
  ? '/api/v1'  // Relative URL in production
  : 'http://localhost:8000/api/v1';  // Full URL in development
```

**Core Functions**:

#### Theme Management
```javascript
fetchThemes()                    // Get all biblical themes
fetchThemeConnections(themeId)   // Get theme-book connections
```

#### Book Management
```javascript
fetchBooks()                     // Get all biblical books
fetchBookInsights(bookId)        // Get book insights and context
```

#### Bible Content
```javascript
fetchChapters(book)              // Get chapters for a book
fetchVerses(book, chapter)       // Get verses for a chapter
```

#### AI-Powered Explanations
```javascript
fetchEventExplanation(book, verse, theme)  // Get event explanations
fetchVerseExplanation(book, chapter, verse) // Get verse explanations
```

### Error Handling
- Comprehensive try-catch blocks
- User-friendly error messages
- Fallback content for failed requests
- Loading states during API calls

## Responsive Design

### Breakpoint System
```css
/* Desktop First Approach */
@media (max-width: 1199px) { /* Tablet */ }
@media (max-width: 768px)  { /* Mobile */ }
```

### Layout Adaptations

#### Desktop (1200px+)
- Three-column grid layout
- Full feature visibility
- Collapsible side panels

#### Tablet (768px - 1199px)
- Single-column stacked layout
- Maintained functionality
- Optimized touch targets

#### Mobile (< 768px)
- Compact single-column design
- Simplified navigation
- Touch-optimized interactions

### Responsive Features
- **Flexible grids**: CSS Grid with auto-fit columns
- **Scalable typography**: Responsive font sizes
- **Touch-friendly**: Larger tap targets on mobile
- **Optimized scrolling**: Custom scrollbars and smooth scrolling

## Development Setup

### Prerequisites
- Node.js 16+ and npm
- Modern web browser
- Code editor (VS Code recommended)

### Installation
```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Development Server
- **Port**: 3000 (configurable)
- **Hot Reload**: Automatic browser refresh
- **API Proxy**: Proxies `/api` requests to backend
- **Error Overlay**: Development error display

### Environment Variables
```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## Build & Deployment

### Production Build
```bash
npm run build
```

**Output**:
- `dist/` directory with optimized assets
- Minified JavaScript and CSS
- Asset fingerprinting for caching
- Source maps for debugging

### Build Optimization
- **Code splitting**: Automatic chunk splitting
- **Tree shaking**: Dead code elimination
- **Asset optimization**: Image and font optimization
- **Compression**: Gzip-ready assets

### Deployment Options
- **Static hosting**: Netlify, Vercel, GitHub Pages
- **CDN deployment**: CloudFront, CloudFlare
- **Docker**: Containerized deployment
- **Traditional hosting**: Apache, Nginx

## Performance Considerations

### Optimization Strategies
- **Lazy loading**: Components loaded on demand
- **Memoization**: React.memo for expensive components
- **Efficient re-renders**: Optimized state updates
- **Asset optimization**: Compressed images and fonts

### Bundle Analysis
```bash
npm run build -- --analyze
```

### Performance Metrics
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Cumulative Layout Shift**: < 0.1
- **First Input Delay**: < 100ms

## Browser Support

### Supported Browsers
- **Chrome**: 90+
- **Firefox**: 88+
- **Safari**: 14+
- **Edge**: 90+

### Progressive Enhancement
- Core functionality works in all modern browsers
- Enhanced features for capable browsers
- Graceful degradation for older browsers

## Accessibility

### WCAG 2.1 Compliance
- **Keyboard navigation**: Full keyboard support
- **Screen readers**: ARIA labels and roles
- **Color contrast**: WCAG AA compliance
- **Focus management**: Visible focus indicators

### Accessibility Features
- **Semantic HTML**: Proper heading hierarchy
- **Alt text**: Descriptive image alternatives
- **Form labels**: Associated form controls
- **Skip links**: Navigation shortcuts

## Future Enhancements

### Planned Features
- **Dark mode**: Theme switching capability
- **Offline support**: Service worker implementation
- **Advanced search**: Full-text search across content
- **User preferences**: Customizable interface
- **Export functionality**: PDF/print capabilities

### Technical Improvements
- **TypeScript migration**: Type safety implementation
- **State management**: Redux or Zustand integration
- **Testing suite**: Unit and integration tests
- **Performance monitoring**: Real user metrics
- **Internationalization**: Multi-language support

---

*This documentation is maintained alongside the codebase and should be updated with any significant changes to the frontend architecture or features.*